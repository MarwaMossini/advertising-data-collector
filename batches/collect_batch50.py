"""Collect first-party promotional posts and exact public engagement counters."""

import concurrent.futures
import datetime as dt
import html
import json
from functools import lru_cache
from pathlib import Path
from steam_promotions import steam_posts
from collections import Counter
import re
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parent
OUT = Path('batch50_output')
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
    r'|予約受付|予約開始|販売開始|好評発売|特価|新発売|発売中|セール|本日発売|発売記念|ご予約', re.I)
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

@lru_cache(maxsize=256)
def pds_endpoint(did):
    if not re.fullmatch(r'did:plc:[a-z2-7]{24}', did):
        return None
    request = urllib.request.Request(f'https://plc.directory/{did}', headers={'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            document = json.load(response)
    except (OSError, ValueError):
        return None
    for service in document.get('service', []):
        if service.get('type') == 'AtprotoPersonalDataServer':
            endpoint = service.get('serviceEndpoint', '').rstrip('/')
            if re.fullmatch(r'https://(?:[a-z0-9.-]+\.bsky\.network|bsky\.social)', endpoint):
                return endpoint
    return None


def bluesky_video(post, did):
    video = post['record'].get('embed', {}).get('video', {})
    cid = video.get('ref', {}).get('$link', '')
    if not re.fullmatch(r'b[a-z2-7]{30,100}', cid):
        return None
    size = video.get('size')
    if type(size) is not int or not 1 <= size <= 7 * 1024 * 1024:
        return None
    endpoint = pds_endpoint(did)
    if endpoint:
        query = urllib.parse.urlencode({'did': did, 'cid': cid})
        return endpoint + '/xrpc/com.atproto.sync.getBlob?' + query, size
    return None


def bluesky(handle):
    api = 'https://public.api.bsky.app/xrpc/'
    profile = get(api + 'app.bsky.actor.getProfile', actor=handle)
    cursor = None
    output = []
    for _ in range(17):
        params = {'actor': profile['did'], 'limit': 70, 'filter': 'posts_no_replies'}
        if cursor:
            params['cursor'] = cursor
        try:
            feed = get(api + 'app.bsky.feed.getAuthorFeed', **params)
        except OSError:
            if not output:
                raise
            break
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
            if not (valid_caption(caption) and metrics_valid(metrics) and valid_date(published)):
                continue
            is_video = embed.get('$type') == 'app.bsky.embed.video#view'
            if is_video:
                video = bluesky_video(post, profile['did'])
                if not video:
                    continue
                url, expected_bytes = video
                alt = [embed.get('alt')]
                urls = [url]
            else:
                if not 1 <= len(images) <= 4:
                    continue
                expected_bytes = None
                alt = [i.get('alt') for i in images]
                urls = [i['fullsize'] for i in images]
            key = post['uri'].rsplit('/', 1)[-1]
            output.append({
                'ad_id': 'BSKY_' + key, 'uri': post['uri'], 'handle': handle, 'platform': 'Bluesky',
                'publisher': profile.get('displayName') or handle, 'profile_url': 'https://bsky.app/profile/' + handle,
                'url': f'https://bsky.app/profile/{handle}/post/{key}', 'caption': caption,
                'published_at_utc': published, 'observed_at_utc': observed, 'metrics': metrics,
                'alt_text': alt, 'media_kind': 'video' if is_video else 'image',
                'media_urls': urls, 'expected_bytes': expected_bytes,
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
    for _ in range(17):
        params = {'limit': 40, 'only_media': 'true', 'exclude_replies': 'true',
                  'exclude_reblogs': 'true'}
        if cursor:
            params['max_id'] = cursor
        try:
            statuses = get(api + profile['id'] + '/statuses', **params)
        except OSError:
            if not output:
                raise
            break
        observed = dt.datetime.now(dt.timezone.utc).isoformat()
        if not statuses:
            break
        for post in statuses:
            images = post.get('media_attachments', [])
            metrics = {'likes': post.get('favourites_count'), 'replies': post.get('replies_count'),
                       'reposts': post.get('reblogs_count'), 'followers': profile.get('followers_count')}
            if not (post['visibility'] == 'public' and 1 <= len(images) <= 4 and
                    (all(i['type'] == 'image' for i in images) or len(images) == 1 and images[0]['type'] == 'video') and valid_caption(post['content']) and
                    metrics_valid(metrics) and valid_date(post['created_at'])):
                continue
            output.append({
                'ad_id': f"MAST_{host}_{post['id']}", 'uri': post['uri'], 'handle': handle, 'platform': 'Mastodon',
                'publisher': profile.get('display_name') or handle, 'profile_url': profile['url'],
                'url': post['url'], 'caption': post['content'], 'published_at_utc': post['created_at'],
                'observed_at_utc': observed, 'metrics': metrics,
                'alt_text': [i.get('description') for i in images],
                'media_kind': 'video' if images[0]['type'] == 'video' else 'image',
                'duration_ms': round(images[0].get('meta', {}).get('original', {}).get('duration', 0)*1000) if images[0]['type'] == 'video' else None,
                'media_urls': [i['url'] for i in images],
            })
        cursor = statuses[-1]['id']
    return output

def main():
    profiles = json.loads((ROOT / 'batch50_profiles.json').read_text())
    old = json.loads((ROOT / 'batch43_sources.json').read_text())
    past_ids = set(profiles['past_ids'])
    seen_ids = {r['ad_id'] for r in old} | past_ids
    seen_urls = {r['url'] for r in old}
    seen_media = {u for r in old for u in r['media_urls']}
    outputs = {}
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=9) as pool:
        jobs = {pool.submit(bluesky, h): h for h in profiles['bluesky'] if HANDLE.fullmatch(h)}
        jobs.update({pool.submit(mastodon, host, h): f'{h}@{host}' for host, h in profiles['mastodon']})
        jobs.update({pool.submit(steam_posts, appid, get, valid_date): f'steam:{appid}' for appid in profiles['steam_apps']})
        for job in concurrent.futures.as_completed(jobs):
            source = jobs[job]
            try:
                outputs[source] = job.result()
            except Exception as e:
                failures.append({'profile': source, 'error': str(e)})
    chosen = []
    targets = {'image': 1090, 'video': 64}
    counts = {'image': 0, 'video': 0}
    for _ in range(75):
        for source in sorted(outputs, key=lambda name: (not ('@' in name or name.startswith('steam:')), name not in profiles['priority'], name)):
            for post in outputs[source]:
                kind = post['media_kind']
                if counts[kind] >= targets[kind]:
                    continue
                urls = set(post['media_urls'])
                if post['ad_id'] in seen_ids or post['url'] in seen_urls or urls & seen_media:
                    continue
                chosen.append(post)
                counts[kind] += 1
                seen_ids.add(post['ad_id'])
                seen_urls.add(post['url'])
                seen_media.update(urls)
                break
        if counts == targets:
            break
    if not chosen:
        raise RuntimeError(f'No first-party promotions found ({len(failures)} feed errors)')
    images = [p for p in chosen if p['media_kind'] == 'image']
    groups = (images[::2], images[1::2], [p for p in chosen if p['media_kind'] == 'video'])
    OUT.mkdir(exist_ok=True)
    for i, group in enumerate(groups):
        output = OUT / str(i)
        output.mkdir()
        (output / 'candidates.json').write_text(json.dumps(group, ensure_ascii=False))
        (output / 'feed_errors.json').write_text(json.dumps(failures))
    print('Candidates by platform', dict(Counter(post['platform'] for post in chosen)), flush=True)
    print('Media counts', counts, flush=True)
    print(f'{len(chosen)} candidates and {len(failures)} feed errors', flush=True)

if __name__ == '__main__':
    main()
