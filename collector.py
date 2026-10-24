"""Public video collector. Automatic results are candidates, never UI-verified ads."""
import argparse, csv, hashlib, json, re, shutil, subprocess, tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import yt_dlp

FIELDS = ['ad_id','platform','advertiser','title','caption_excerpt','published_date',
          'recorded_at_utc','likes','comments','shares','views','duration_seconds',
          'source_url','media_path','sha256','metric_source','review_status','paid_status']

def allowed(url):
    u=urlparse(url); h=(u.hostname or '').lower()
    return u.scheme=='https' and h in {'www.facebook.com','facebook.com','www.youtube.com','youtube.com','youtu.be'}

def metric_issue(info):
    for key in ('like_count', 'comment_count', 'repost_count', 'view_count'):
        value = info.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            return 'missing or invalid ' + key
    # Facebook titles can include rounded public view totals. Reject disagreement.
    match = re.search(r'([\d,.]+)\s*([KMB]?)\s+views', info.get('title', ''), re.I)
    if match:
        number, suffix = match.groups()
        scale = {'':1, 'K':1000, 'M':1000000, 'B':1000000000}[suffix.upper()]
        displayed = float(number.replace(',', '')) * scale
        tolerance = scale * 0.05 if suffix else 0
        if abs(info['view_count'] - displayed) > tolerance:
            return 'conflicting public and extracted view counts'
    return None

def classify(info, source):
    if info.get('_type') in ('playlist','multi_video') or info.get('is_live'):
        return 'not a single recorded video'
    day=info.get('upload_date')
    if not day or not re.fullmatch(r'\d{8}',day) or not ('20210101'<=day<='20261231'):
        return 'missing/out-of-range publication date'
    if not info.get('duration') or not 0 < info['duration'] <= 300:
        return 'duration outside 1–300 seconds'
    issue = metric_issue(info)
    if issue: return issue
    if not source.get('curated'):
        uploader=(info.get('uploader') or '').casefold()
        if uploader not in [x.casefold() for x in source.get('allowed_uploaders',[])]:
            return 'uploader does not match configured brand'
        text=((info.get('title') or '')+' '+(info.get('description') or '')).casefold()
        if not any(k.casefold() in text for k in source.get('promotion_keywords',[])):
            return 'no configured promotional keyword'
    return None

def probe(path):
    d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
       'format=duration:stream=codec_type,width,height','-of','json',str(path)],timeout=30))
    if not any(s.get('codec_type')=='video' for s in d.get('streams',[])):
        raise ValueError('Downloaded file has no video stream')
    return d

def read_rows(path):
    if not path.exists(): return []
    with path.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))

def save_rows(path, rows):
    tmp=path.with_suffix('.tmp')
    with tmp.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
    tmp.replace(path)

def run(config, out, limit):
    out.mkdir(parents=True,exist_ok=True);(out/'media').mkdir(exist_ok=True)
    rows=read_rows(out/'complete_candidates.csv');seen={r['ad_id'] for r in rows}
    hashes={r['sha256'] for r in rows};events=[];added=0;blocked=set()
    # No cookies, browser profile, account token, proxy or login supplied.
    opts={'quiet':True,'noplaylist':True,'socket_timeout':20,'retries':0,
          'fragment_retries':0,'format':'best[ext=mp4]/best','js_runtimes':{'node':{}},
          'max_filesize':100*1024*1024,'cachedir':False}
    def error(source, exc):
        message=str(exc)
        # Stop this platform for the remainder of the run when access is restricted.
        if any(w in message.lower() for w in ['sign in','login','log in','captcha','bot','429','403']):
            blocked.add(source['platform'])
        events.append({'source':source.get('url',source.get('query')),'status':'failed','error':message[:500]})
    for source in config['sources']:
        if added>=limit:break
        if source['platform'] in blocked:continue
        if sum(p.stat().st_size for p in (out/'media').glob('*'))>=2*1024**3:
            events.append({'status':'storage_limit','error':'2 GiB cap reached; move media to durable storage before expanding.'});break
        try:
            if 'url' in source:
                urls=[source['url']]
            else:
                with yt_dlp.YoutubeDL({**opts,'extract_flat':True}) as y:
                    found=y.extract_info('ytsearch10:'+source['query'],download=False)
                urls=[e.get('url','') for e in found.get('entries',[]) if e]
            for url in urls:
                if added>=limit or source['platform'] in blocked:break
                if not allowed(url):continue
                try:
                    with yt_dlp.YoutubeDL(opts) as y:info=y.extract_info(url,download=False)
                    observed_at=datetime.now(timezone.utc).isoformat()
                    reason=classify(info,source)
                    if reason:
                        events.append({'source':url,'status':'excluded','reason':reason});continue
                    aid=source['platform']+'-'+str(info['id'])
                    if not re.fullmatch(r'[A-Za-z0-9_-]+',aid):raise ValueError('Unsafe source ID')
                    if aid in seen:continue
                    with tempfile.TemporaryDirectory(dir=out) as staging:
                        with yt_dlp.YoutubeDL({**opts,'outtmpl':str(Path(staging)/'creative.%(ext)s')}) as y:
                            y.extract_info(url,download=True)
                        media=[p for p in Path(staging).glob('creative.*') if p.suffix in ('.mp4','.webm','.mkv')]
                        if len(media)!=1:raise ValueError('Expected exactly one complete video')
                        check=probe(media[0]);digest=hashlib.sha256(media[0].read_bytes()).hexdigest()
                        if digest in hashes:
                            events.append({'source':url,'status':'duplicate_creative'});continue
                        rel='media/'+aid+media[0].suffix;shutil.move(str(media[0]),out/rel)
                    day=info['upload_date'];record={k:'' for k in FIELDS}
                    record.update(ad_id=aid,platform=source['platform'],advertiser=info.get('uploader') or source.get('advertiser',''),
                        title=info.get('title',''),caption_excerpt=' '.join((info.get('description') or '').split()[:25]),
                        published_date=f'{day[:4]}-{day[4:6]}-{day[6:]}',recorded_at_utc=observed_at,
                        likes=info.get('like_count'),comments=info.get('comment_count'),shares=info.get('repost_count'),views=info.get('view_count'),
                        duration_seconds=float(check['format']['duration']),source_url=url,media_path=rel,sha256=digest,
                        metric_source='yt-dlp public metadata; not UI-verified',review_status='needs_review',paid_status='unknown')
                    rows.append(record);save_rows(out/'complete_candidates.csv',rows)
                    seen.add(aid);hashes.add(digest);added+=1
                except Exception as exc:error(source,exc)
        except Exception as exc:error(source,exc)
    save_rows(out/'complete_candidates.csv',rows)
    report={'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'added':added,'total_candidates':len(rows),'status':'complete_candidates_saved' if added else 'no_usable_records','events':events}
    (out/'latest_run.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'added':added,'total_candidates':len(rows),'events':len(events)}))
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--config',default='sources.json');parser.add_argument('--out',default='data');parser.add_argument('--limit',type=int,default=10)
    args=parser.parse_args();run(json.loads(Path(args.config).read_text()),Path(args.out),args.limit)

