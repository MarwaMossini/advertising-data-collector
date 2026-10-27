"""Collect metadata and original media from explicitly curated public post URLs.

Automatic results are candidates. Missing metrics remain blank; review is required.
"""
import argparse, csv, hashlib, json, re, shutil, subprocess, tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

PLATFORMS = {
    'facebook.com':'Facebook','www.facebook.com':'Facebook',
    'instagram.com':'Instagram','www.instagram.com':'Instagram',
    'youtube.com':'YouTube','www.youtube.com':'YouTube','youtu.be':'YouTube',
    'tiktok.com':'TikTok','www.tiktok.com':'TikTok',
}
METRICS = ['likes','comments','shares','reposts','views','followers','saves']
AD_FIELDS = ['ad_id','platform','company','published_date','publication_date_source','industry',
 'latest_observed_at_utc'] + [m+'_exact' for m in METRICS] + ['media_type','media_path',
 'original_post_url','publisher','promotion_type','first_collected_at_utc','published_date_label',
 'verification_status','paid_status','title','caption','sha256','notes']
SNAPSHOT_FIELDS = ['ad_id','observed_at_utc'] + [x for m in METRICS for x in (m+'_exact',m+'_display')] + ['source_url','metric_source','notes']

def platform_for(url):
    u=urlparse(url)
    return PLATFORMS.get((u.hostname or '').lower()) if u.scheme=='https' else None

def read_csv(path, fields):
    if not path.exists(): return []
    with path.open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))

def save_csv(path, fields, rows):
    tmp=path.with_suffix('.tmp')
    with tmp.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
    tmp.replace(path)

def probe(path):
    d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type','-of','json',str(path)],timeout=30))
    if not any(s.get('codec_type')=='video' for s in d.get('streams',[])):raise ValueError('Downloaded file has no video stream')
    return float(d['format']['duration'])

def scalar(info,*names):
    for n in names:
        v=info.get(n)
        if isinstance(v,(int,float)) and not isinstance(v,bool) and v>=0:return v
    return ''

def publication_date(info, source):
    for key in ('timestamp','release_timestamp'):
        v=info.get(key)
        if isinstance(v,(int,float)) and not isinstance(v,bool):
            try:
                day=datetime.fromtimestamp(v,timezone.utc).date().isoformat()
                if '2021-01-01'<=day<='2026-12-31':return day,'Platform '+key+' (UTC)'
            except (ValueError,OverflowError,OSError):pass
    for key in ('upload_date','release_date'):
        value=str(info.get(key) or '')
        try:
            day=datetime.strptime(value,'%Y%m%d').date().isoformat()
            if '2021-01-01'<=day<='2026-12-31':return day,'Platform '+key+' (timezone unspecified)'
        except ValueError:pass
    value=str(source.get('published_date') or '')[:10]
    if re.fullmatch(r'202[1-6]-\d{2}-\d{2}',value) and source.get('publication_date_source'):
        try:
            datetime.strptime(value,'%Y-%m-%d')
            return value,source['publication_date_source']
        except ValueError:pass
    return '', 'Unavailable; no date inferred'

def metric_snapshot(info):
    mapping={'likes':('like_count',),'comments':('comment_count',),'shares':('share_count',),
             'reposts':('repost_count',),'views':('view_count',),
             'followers':('channel_follower_count','uploader_follower_count'),'saves':('save_count',)}
    values={m:scalar(info,*names) for m,names in mapping.items()};notes=[]
    match=re.search(r'([\d,.]+)\s*([KMB]?)\s+views',info.get('title') or '',re.I)
    if match and values['views']!='':
        raw,suffix=match.groups();scale={'':1,'K':1000,'M':1000000,'B':1000000000}[suffix.upper()]
        displayed=float(raw.replace(',',''))*scale
        if abs(displayed-values['views'])>scale*.05:
            values['views']='';notes.append('Views withheld: title display conflicts with extracted view_count.')
    return values,' '.join(notes)

def migrate_legacy(out):
    ads=read_csv(out/'ads.csv',AD_FIELDS); snaps=read_csv(out/'engagement_snapshots.csv',SNAPSHOT_FIELDS)
    known={r['ad_id'] for r in ads}
    for name in ('complete_candidates.csv','candidates.csv'):
        for old in read_csv(out/name,[]):
            aid=old.get('ad_id','')
            if not aid or aid in known:continue
            row={k:'' for k in AD_FIELDS};row.update(ad_id=aid,platform=old.get('platform',''),company=old.get('advertiser',''),
              title=old.get('title',''),caption=old.get('caption_excerpt',''),published_date=old.get('published_date',''),
              first_collected_at_utc=old.get('recorded_at_utc',''),latest_observed_at_utc=old.get('recorded_at_utc',''),
              media_type='video',media_path=old.get('media_path',''),sha256=old.get('sha256',''),original_post_url=old.get('source_url',''),
              verification_status='needs_review',paid_status='unknown',notes='Migrated from previous collector output; original evidence limits apply.')
            ads.append(row);known.add(aid)
            snap={'ad_id':aid,'observed_at_utc':old.get('recorded_at_utc',''),'source_url':old.get('source_url',''),'metric_source':old.get('metric_source','legacy extractor'),'notes':'Migrated legacy snapshot.'}
            for m in METRICS:snap[m+'_exact']=old.get(m,'');snap[m+'_display']=''
            snaps.append(snap)
    return ads,snaps

def run(config,out,limit=25):
    import yt_dlp
    out=Path(out);media=out/'media';media.mkdir(parents=True,exist_ok=True)
    ads,snaps=migrate_legacy(out);byid={r['ad_id']:r for r in ads};known_snap={(r['ad_id'],r['observed_at_utc']) for r in snaps}
    report={'started_at_utc':datetime.now(timezone.utc).isoformat(),'added_ads':0,'new_snapshots':0,'events':[]}
    opts={'quiet':True,'noplaylist':True,'socket_timeout':20,'retries':1,'fragment_retries':1,'format':'best[ext=mp4]/best',
          'js_runtimes':{'node':{}},'max_filesize':250*1024*1024,'cachedir':False}
    for source in config.get('sources',[])[:limit]:
        url=source.get('url','');plat=platform_for(url)
        if not plat or source.get('platform',plat)!=plat:
            report['events'].append({'url':url,'status':'rejected','reason':'Only explicit HTTPS URLs from supported platforms are accepted.'});continue
        try:
            with yt_dlp.YoutubeDL(opts) as y:info=y.extract_info(url,download=False)
            if info.get('_type') in ('playlist','multi_video') or info.get('entries') or info.get('is_live'):
                raise ValueError('Gallery, playlist or live stream excluded; requires one original creative.')
            day,date_source=publication_date(info,source)
            if not day:raise ValueError('Publication date unavailable or outside 2021–2026; excluded from main list.')
            aid=plat+'-'+str(info.get('id') or hashlib.sha256(url.encode()).hexdigest()[:16])
            if not re.fullmatch(r'[A-Za-z0-9_-]+',aid):raise ValueError('Unexpected post identifier')
            now=datetime.now(timezone.utc).isoformat(timespec='seconds');row=byid.get(aid);is_new=row is None
            if row is None:
                row={k:'' for k in AD_FIELDS};row.update(ad_id=aid,platform=plat,company=source.get('company',''),publisher=info.get('uploader') or '',
                    industry=source.get('industry',''),promotion_type=source.get('promotion_type','brand promotion; review needed'),title=info.get('title') or '',
                    caption=info.get('description') or '',published_date=info.get('upload_date') or '',published_date_label=info.get('release_date') or '',
                    first_collected_at_utc=now,original_post_url=url,verification_status='needs_review',paid_status=source.get('paid_status','unknown'),notes='Metadata extractor output; verify against original post.')
            row['latest_observed_at_utc']=now
            row.update(published_date=day,publication_date_source=date_source,company=source.get('company') or row.get('company',''),
                       industry=source.get('industry') or row.get('industry',''),caption=info.get('description') or row.get('caption',''),
                       publisher=info.get('uploader') or row.get('publisher',''))
            metric,metric_notes=metric_snapshot(info)
            snap={'ad_id':aid,'observed_at_utc':now,'source_url':url,'metric_source':'public metadata extractor; not independently UI-verified','notes':''}
            snap['notes']=metric_notes
            for m,value in metric.items():
                snap[m+'_exact']=value;snap[m+'_display']=str(value) if value!='' else '';row[m+'_exact']=value
            if (aid,now) not in known_snap:snaps.append(snap);known_snap.add((aid,now));report['new_snapshots']+=1
            if not row.get('media_path') or not (out/row['media_path']).is_file():
                with tempfile.TemporaryDirectory(dir=out) as stage:
                    with yt_dlp.YoutubeDL({**opts,'outtmpl':str(Path(stage)/'creative.%(ext)s')}) as y:y.extract_info(url,download=True)
                    files=[p for p in Path(stage).glob('creative.*') if p.suffix.lower() in ('.mp4','.webm','.mkv','.jpg','.jpeg','.png','.webp')]
                    if len(files)!=1:raise ValueError('Could not retrieve exactly one original image or video.')
                    f=files[0]
                    if f.suffix.lower() in ('.mp4','.webm','.mkv'):probe(f);row['media_type']='video'
                    else:row['media_type']='image'
                    digest=hashlib.sha256(f.read_bytes()).hexdigest();dest=media/(aid+f.suffix.lower());shutil.move(str(f),dest)
                    row['media_path']='media/'+dest.name;row['sha256']=digest
            if is_new:
                ads.append(row);byid[aid]=row
            save_csv(out/'ads.csv',AD_FIELDS,ads);save_csv(out/'engagement_snapshots.csv',SNAPSHOT_FIELDS,snaps)
            if is_new:report['added_ads']+=1
            report['events'].append({'ad_id':aid,'url':url,'status':'recorded'})
        except Exception as e:report['events'].append({'url':url,'status':'failed','error':str(e)[:400]})
    save_csv(out/'ads.csv',AD_FIELDS,ads);save_csv(out/'engagement_snapshots.csv',SNAPSHOT_FIELDS,snaps)
    report.update(finished_at_utc=datetime.now(timezone.utc).isoformat(),total_ads=len(ads),total_snapshots=len(snaps))
    (out/'latest_run.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('added_ads','new_snapshots','total_ads','total_snapshots')}))
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',default='sources.json');p.add_argument('--out',default='data');p.add_argument('--limit',type=int,default=25);a=p.parse_args()
    run(json.loads(Path(a.config).read_text()),a.out,a.limit)
