"""Re-read public native records for the surviving Batch 43 media manifest."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen
import json
import re

BASE = Path(__file__).parent
APPVIEW = 'https://public.api.bsky.app/xrpc/'
MASTODON = {'mastodon.social', 'floss.social', 'social.vivaldi.net'}

def now():
    return datetime.now(timezone.utc).isoformat()

def json_get(url, params=()):
    if params:
        url += '?' + urlencode(params)
    req = Request(url, headers={'Accept':'application/json','User-Agent':'Promotional-media-audit/1.0'})
    with urlopen(req, timeout=18) as response:
        return json.load(response)

def batches(items):
    return [items[i:i+20] for i in range(0,len(items),20)]

def handle_did(source):
    url = urlsplit(source['url'])
    m = re.fullmatch(r'/profile/([a-z0-9.-]+)/post/([a-z0-9]+)',url.path,re.I)
    if url.hostname != 'bsky.app' or not m or 'BSKY_'+m[2] != source['ad_id']:
        return None
    dids = set()
    for media in source['media_urls']:
        parts = urlsplit(media)
        match = re.search(r'/plain/(did:plc:[a-z2-7]{24})/',parts.path)
        if parts.hostname != 'cdn.bsky.app' or not match:
            return None
        dids.add(match[1])
    if len(dids)!=1:
        return None
    return next(iter(dids)),m[1],m[2]

def get_profiles(dids):
    payload = json_get(APPVIEW+'app.bsky.actor.getProfiles',[('actors',d) for d in dids])
    return {r['did']:r for r in payload.get('profiles',[])}

def bsky_posts(items, profiles):
    by_uri = {f'at://{did}/app.bsky.feed.post/{post}': (source,did,handle)
              for source,did,handle,post in items}
    payload = json_get(APPVIEW+'app.bsky.feed.getPosts',[('uris',u) for u in by_uri])
    observed = now()
    output = []
    for post in payload.get('posts',[]):
        source,did,handle = by_uri[post['uri']]
        author = post['author']
        if author['did']!=did or author['handle'].lower()!=handle.lower():
            continue
        images = post.get('embed',{}).get('images',[])
        if [m['fullsize'] for m in images]!=source['media_urls']:
            continue
        data = post['record']
        output.append({
            **source, 'platform':'Bluesky','publisher':author.get('displayName') or handle,'handle':handle,
            'published_at_utc':data['createdAt'],'observed_at_utc':observed,'caption':data.get('text',''),
            'metrics':{'likes':post.get('likeCount'),'replies':post.get('replyCount'),
                       'reposts':post.get('repostCount'),'bookmarks':post.get('bookmarkCount'),
                       'followers':profiles.get(did,{}).get('followersCount')},
            'alt_text':[m.get('alt') for m in images],
        })
    return output

def mastodon_post(source):
    url = urlsplit(source['url'])
    match = re.fullmatch(r'/@([^/]+)/([0-9]+)',url.path)
    if url.hostname not in MASTODON or not match:
        return []
    status = json_get(f'https://{url.hostname}/api/v1/statuses/{match[2]}')
    if status.get('visibility')!='public' or status.get('reblog') or status.get('url')!=source['url']:
        return []
    images = status.get('media_attachments',[])
    if [m['url'] for m in images]!=source['media_urls'] or any(m['type']!='image' for m in images):
        return []
    account = status['account']
    return [{
        **source, 'platform':'Mastodon','publisher':account.get('display_name') or account['username'],
        'handle':account['username'], 'published_at_utc':status['created_at'],
        'observed_at_utc':now(),'caption':status.get('content',''),
        'metrics':{'likes':status.get('favourites_count'),'replies':status.get('replies_count'),
                   'reposts':status.get('reblogs_count'),'followers':account.get('followers_count')},
        'alt_text':[m.get('description') for m in images],
    }]

def main():
    sources = json.loads((BASE/'batch43_sources.json').read_text())
    bsky, mastodon = [], []
    for source in sources:
        if source['ad_id'].startswith('BSKY_') and (identity:=handle_did(source)):
            bsky.append((source,*identity))
        elif source['ad_id'].startswith('MAST_'):
            mastodon.append(source)
    profiles, failures, output = {}, [], []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for job in [pool.submit(get_profiles,g) for g in batches(sorted({x[1] for x in bsky}))]:
            try:
                profiles.update(job.result())
            except (OSError,ValueError,KeyError) as error:
                failures.append('Profiles: '+str(error))
        jobs = [pool.submit(bsky_posts,g,profiles) for g in batches(bsky)]
        jobs.extend(pool.submit(mastodon_post, source) for source in mastodon)
        for job in jobs:
            try:
                output.extend(job.result())
            except (OSError,ValueError,KeyError) as error:
                failures.append(str(error))
    result = [p for p in output if all(type(p['metrics'].get(k)) is int and p['metrics'][k]>=0
                                      for k in ('likes','replies','reposts'))]
    directory = Path('recovered_metadata')
    directory.mkdir()
    (directory/'records.json').write_text(json.dumps(result,ensure_ascii=False))
    (directory/'errors.json').write_text(json.dumps(failures,ensure_ascii=False))
    print(f'{len(result)}/{len(sources)} public posts match original media URLs with exact engagement')
    if not result:
        raise RuntimeError('No complete original records returned')

if __name__=='__main__':
    main()
