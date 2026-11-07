"""Collect first-party promotional posts and exact public engagement counters."""

import concurrent.futures
import datetime as dt
import html
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parent
OUT = Path('batch44_output')
NOW = dt.datetime.now(dt.timezone.utc)
PROMO = re.compile(
    r'\b(?:pre[ -]?order\w*|out now|now available|on sale|discount|\d+\s*%\s*off|'
    r'sale (?:ends|starts|is now|is live)|shop (?:now|the|our)|now shipping|back in stock|'
    r'grab your copy|get your copy|order now|buy now|tickets? (?:on sale|available)|'
    r'book now|available (?:now|for purchase|to buy|today)|launch discount|'
    r'pledge now|available in (?:stores|our shop)|limited edition|'
    r'précommand\w*|en vente|disponible maintenant|réduction|'
    r'pré-venda|já disponível|compre agora|\w+ em oferta|'
    r'vorbestell\w*|jetzt erhältlich|rabatt|'
    r'preventa|ya disponible|a la venta|compra ahora|descuento)\b'
    r'|予約受付|販売開始|好評発売|特価|新発売|発売中|セール', re.I)
EXCLUDE = re.compile(r'\b(?:outage|hiring|job opening|scam|vote for us|'
                     r'correction|update log|patch notes|security update)\b', re.I)
HANDLE = re.compile(r'[a-z0-9][a-z0-9.-]+\.[a-z]{2,}')

def get(url, **query):
    request = urllib.request.Request(url + '?' + urllib.parse.urlencode(query),
                                     headers={'Accept': 'application/json'})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)

def valid_caption(caption):
    plain = html.unescape(re.sub(r'<[^>]+>', ' ', caption)).strip()
    return len(plain) >= 25 and PROMO.search(plain) and not EXCLUDE.search(plain)

def metrics_valid(metrics):
    return all(type(metrics.get(k)) is int and metrics[k] >= 0
               for k in ('likes', 'replies', 'reposts'))

def valid_date(stamp):
    return dt.datetime(2021, 1, 1, tzinfo=dt.timezone.utc) <= dt.datetime.fromisoformat(stamp) <= NOW

def bluesky(handle):
    api = 'https://public.api.bsky.app/xrpc/'
    profile = get(api + 'app.bsky.actor.getProfile', actor=handle)
    cursor = None
    output = []
    for _ in range(9):
        params = {'actor': profile['did'], 'limit': 70, 'filter': 'posts_no_replies'}
        if cursor:
            params['cursor'] = cursor
        feed = get(api + 'app.bsky.feed.getAuthorFeed', **params)
        observed = dt.datetime.now(dt.timezone.utc).isoformat()
        for item in feed.get('feed', []):
            post = item['post']
            if item.get('reason') or item.get('reply') or post['author']['did'] != profile['did']:
                continue
            caption = post['record']['text']
            published = post['record']['createdAt']
            embed = post.get('embed', {})
            images = embed.get('images', [])
            metrics = {'likes': post.get('likeCount'), 'replies': post.get('replyCount'),
                       'reposts': post.get('repostCount'), 'bookmarks': post.get('bookmarkCount'),
                       'followers': profile.get('followersCount')}
            if not (1 <= len(images) <= 4 and valid_caption(caption) and
                    metrics_valid(metrics) and valid_date(published)):
                continue
            key = post['uri'].rsplit('/', 1)[-1]
            output.append({
                'ad_id': 'BSKY_' + key, 'uri': post['uri'], 'handle': handle, 'platform': 'Bluesky',
                'publisher': profile.get('displayName') or handle, 'profile_url': 'https://bsky.app/profile/' + handle,
                'url': f'https://bsky.app/profile/{handle}/post/{key}', 'caption': caption,
                'published_at_utc': published, 'observed_at_utc': observed, 'metrics': metrics,
                'alt_text': [i.get('alt') for i in images], 'media_kind': 'image',
                'media_urls': [i['fullsize'] for i in images],
            })
        cursor = feed.get('cursor')
        if not cursor:
            break
    return output

def mastodon(host, handle):
    api = f'https://{host}/api/v1/accounts/'
    profile = get(api + 'lookup', acct=handle)
    if '@' in profile['acct']:
        return []
    cursor = None
    output = []
    for _ in range(6):
        params = {'limit': 40, 'only_media': 'true', 'exclude_replies': 'true',
                  'exclude_reblogs': 'true'}
        if cursor:
            params['max_id'] = cursor
        statuses = get(api + profile['id'] + '/statuses', **params)
        observed = dt.datetime.now(dt.timezone.utc).isoformat()
        if not statuses:
            break
        for post in statuses:
            images = post.get('media_attachments', [])
            metrics = {'likes': post.get('favourites_count'), 'replies': post.get('replies_count'),
                       'reposts': post.get('reblogs_count'), 'followers': profile.get('followers_count')}
            if not (post['visibility'] == 'public' and 1 <= len(images) <= 4 and
                    all(i['type'] == 'image' for i in images) and valid_caption(post['content']) and
                    metrics_valid(metrics) and valid_date(post['created_at'])):
                continue
            output.append({
                'ad_id': f"MAST_{host}_{post['id']}", 'uri': post['uri'], 'handle': handle, 'platform': 'Mastodon',
                'publisher': profile.get('display_name') or handle, 'profile_url': profile['url'],
                'url': post['url'], 'caption': post['content'], 'published_at_utc': post['created_at'],
                'observed_at_utc': observed, 'metrics': metrics,
                'alt_text': [i.get('description') for i in images], 'media_kind': 'image',
                'media_urls': [i['url'] for i in images],
            })
        cursor = statuses[-1]['id']
    return output

def main():
    profiles = json.loads((ROOT / 'batch44_profiles.json').read_text())
    old = json.loads((ROOT / 'batch43_sources.json').read_text())
    seen_ids = {r['ad_id'] for r in old}
    seen_urls = {r['url'] for r in old}
    seen_media = {u for r in old for u in r['media_urls']}
    outputs = {}
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
        jobs = {pool.submit(bluesky, h): h for h in profiles['bluesky'] if HANDLE.fullmatch(h)}
        jobs.update({pool.submit(mastodon, host, h): f'{h}@{host}' for host, h in profiles['mastodon']})
        for job in concurrent.futures.as_completed(jobs):
            source = jobs[job]
            try:
                outputs[source] = job.result()
            except Exception as e:
                failures.append({'profile': source, 'error': str(e)})
    chosen = []
    for _ in range(24):
        for source in sorted(outputs):
            for post in outputs[source]:
                urls = set(post['media_urls'])
                if post['ad_id'] in seen_ids or post['url'] in seen_urls or urls & seen_media:
                    continue
                chosen.append(post)
                seen_ids.add(post['ad_id'])
                seen_urls.add(post['url'])
                seen_media.update(urls)
                break
        if len(chosen) >= 900:
            break
    chosen = chosen[:900]
    if not chosen:
        raise RuntimeError(f'No first-party promotions found ({len(failures)} feed errors)')
    OUT.mkdir(exist_ok=True)
    (OUT / 'candidates.json').write_text(json.dumps(chosen, ensure_ascii=False))
    (OUT / 'feed_errors.json').write_text(json.dumps(failures))
    Path('batch44_candidate_sources.json').write_text(json.dumps(chosen))
    print(f'{len(chosen)} candidates and {len(failures)} feed errors', flush=True)

if __name__ == '__main__':
    main()
