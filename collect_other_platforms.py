"""Download explicitly curated public X/LinkedIn promotional posts for review.

No login, cookies, proxies or access-control workarounds. Output is candidate
evidence, never an automatic addition to the reviewed Drive master.
"""
import argparse, hashlib, json, re, time, urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import yt_dlp

class PageMetadata(HTMLParser):
    def __init__(self):
        super().__init__(); self.active=False; self.current=''; self.schemas=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='script' and a.get('type')=='application/ld+json':
            self.active=True; self.current=''
    def handle_data(self, data):
        if self.active:self.current+=data
    def handle_endtag(self, tag):
        if tag=='script' and self.active:
            try:self.schemas.append(json.loads(self.current))
            except json.JSONDecodeError:pass
            self.active=False

def walk(v):
    if isinstance(v,dict):
        yield v
        for x in v.values():yield from walk(x)
    elif isinstance(v,list):
        for x in v:yield from walk(x)

def fetch(url, allowed, cap):
    def valid(u):
        p=urlparse(u)
        if p.scheme!='https' or p.hostname not in allowed or p.username or p.password:
            raise ValueError('URL outside explicit HTTPS first-party allowlist')
    valid(url)
    class Redirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            valid(newurl)
            return super().redirect_request(req,fp,code,msg,headers,newurl)
    req=urllib.request.Request(url,headers={'User-Agent':'AdvertisingResearchCollector/1.0 (public source research)'})
    with urllib.request.build_opener(Redirect).open(req,timeout=30) as r:
        b=r.read(cap+1)
        if len(b)>cap:raise ValueError('Response exceeds bounded file size')
        return b, r.headers.get_content_type()

def run(config,out):
    out=Path(out);(out/'media').mkdir(parents=True,exist_ok=True)
    report={'started_at_utc':datetime.now(timezone.utc).isoformat(),'events':[]}; rows=[]; stopped=set()
    opts={'quiet':True,'noplaylist':True,'socket_timeout':20,'retries':0,'fragment_retries':0,
          'format':'best[ext=mp4]/best','js_runtimes':{'node':{}},'cachedir':False,'max_filesize':150*1024*1024}
    for i,s in enumerate(config['sources']):
        if i:time.sleep(5)
        url=s['url']; platform=s['platform']; host=urlparse(url).hostname
        if platform in stopped:
            report['events'].append({'url':url,'status':'skipped','reason':'Earlier access restriction on this platform'});continue
        try:
            if host not in {'x.com','www.linkedin.com'} or urlparse(url).scheme!='https':raise ValueError('Unsupported original post URL')
            now=datetime.now(timezone.utc).isoformat();r={'source':s,'collected_at_utc':now}
            if platform=='LinkedIn':
                if host!='www.linkedin.com' or '/posts/' not in url:raise ValueError('Expected original LinkedIn post')
                page,_=fetch(url,{'www.linkedin.com','linkedin.com'},4*1024*1024)
                p=PageMetadata();p.feed(page.decode('utf-8','replace'))
                schemas=[x for z in p.schemas for x in walk(z) if x.get('datePublished') and x.get('@type') in ('SocialMediaPosting','Article','BlogPosting')]
                if not schemas:raise ValueError('No original post publication date in public page metadata')
                meta=schemas[0]; date=str(meta['datePublished']); day=datetime.fromisoformat(date.replace('Z','+00:00')).date().isoformat()
                r.update(published_date=day,publication_evidence='Original LinkedIn public JSON-LD datePublished: '+date,caption=meta.get('articleBody') or meta.get('description') or '',original_metadata=meta)
                aid='LI_'+re.search(r'activity-(\d+)',url).group(1)
            elif platform=='X':
                if host!='x.com' or not re.search(r'/status/\d+$',url):raise ValueError('Expected original X post')
                aid='X_'+url.rsplit('/',1)[-1]
                if s.get('media_url'):
                    day=s['published_date'];r.update(published_date=day,publication_evidence=s['publication_evidence'],caption=s['caption'])
                else:
                    with yt_dlp.YoutubeDL({**opts,'outtmpl':str(out/'media'/(aid+'.%(ext)s'))}) as y:info=y.extract_info(url,download=True)
                    if info.get('_type') in ('playlist','multi_video') or info.get('entries') or info.get('is_live'):raise ValueError('Not one complete original creative')
                    ts=info.get('timestamp')
                    if not isinstance(ts,(int,float)):raise ValueError('No original-platform publication timestamp')
                    day=datetime.fromtimestamp(ts,timezone.utc).date().isoformat()
                    r.update(published_date=day,publication_evidence='Original-platform extractor timestamp (UTC): '+str(ts),caption=info.get('description') or '',extractor_metadata={k:info.get(k) for k in ('id','title','uploader','timestamp','duration','like_count','comment_count','repost_count','view_count')})
            else:raise ValueError('Unsupported platform')
            if not '2021-01-01'<=day<=datetime.now(timezone.utc).date().isoformat():raise ValueError('Publication date outside scope')
            if s.get('media_url'):
                b,mime=fetch(s['media_url'],{'media.licdn.com','pbs.twimg.com'},25*1024*1024)
                ext={'image/jpeg':'.jpg','image/png':'.png','image/webp':'.webp'}.get(mime)
                if not ext:raise ValueError('Expected a public original-post image rendition')
                f=out/'media'/(aid+ext);f.write_bytes(b);media_type='image'
            else:
                fs=[f for f in (out/'media').glob(aid+'.*') if f.suffix in ('.mp4','.webm','.mkv')]
                if len(fs)!=1:raise ValueError('Expected exactly one complete video')
                f=fs[0];media_type='video'
            r.update(ad_id=aid,media_type=media_type,media_path='media/'+f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size)
            rows.append(r);report['events'].append({'url':url,'ad_id':aid,'status':'recorded'})
        except Exception as e:
            message=str(e)[:500];report['events'].append({'url':url,'status':'failed','error':message})
            if re.search(r'verify.{0,20}human|automated traffic|bot detection|captcha|sign in|login required|HTTP Error (403|429|999)',message,re.I):stopped.add(platform)
        (out/'candidates.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
        (out/'latest_run.json').write_text(json.dumps(report,indent=2))
    report.update(finished_at_utc=datetime.now(timezone.utc).isoformat(),recorded=len(rows))
    (out/'latest_run.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    run(json.loads(Path(a.config).read_text()),a.out)
