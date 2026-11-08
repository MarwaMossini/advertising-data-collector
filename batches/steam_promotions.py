"""Collect public Steam partner announcements with complete static creative sets."""

from datetime import datetime, timezone
import html
import json
import re
from urllib.parse import urlsplit

STORE = 'https://store.steampowered.com'
CLAN_CDN = 'https://clan.cloudflare.steamstatic.com/images'
MEDIA_HOSTS = {
    'clan.cloudflare.steamstatic.com', 'clan.akamai.steamstatic.com',
    'shared.cloudflare.steamstatic.com', 'shared.akamai.steamstatic.com',
    'cdn.cloudflare.steamstatic.com', 'cdn.akamai.steamstatic.com',
    'cdn.fastly.steamstatic.com', 'steamcdn-a.akamaihd.net',
}
OFFER = re.compile(
    r'\b(?:pre[- ]?(?:order|purchase)|launch (?:discount|sale)|on sale|now available|'
    r'available now|out now|discount(?:ed)?|\d+\s*%\s*off|free weekend|'
    r'play (?:for )?free|available (?:today|for purchase)|get it now|'
    r'official launch|released today|buy now)\b', re.I)
PATCH = re.compile(r'\b(?:patch notes|hotfix|maintenance|bug fixes|known issues)\b', re.I)
IMAGE = re.compile(r'\[img(?:\s[^\]]+)?\](.*?)\[/img\]', re.I | re.S)
VIDEO = re.compile(r'\[(?:previewyoutube|youtube|video|webm|hls|looping_media)\b|\.(?:webm|mp4|gif)(?:\b|\?)', re.I)
ASSET = re.compile(r'[0-9a-f]{40}\.(?:jpg|jpeg|png|webp)', re.I)


def source_images(event, body, language):
    if VIDEO.search(body):
        return []
    clan = event['announcement_body']['clanid']
    if not str(clan).isdecimal():
        return []
    metadata = json.loads(event['jsondata'])
    urls = []
    for field in ('localized_capsule_image', 'localized_title_image'):
        values = metadata.get(field, [])
        if not isinstance(values, list):
            continue
        asset = (values[language] if language < len(values) else None) or (values[0] if values else None)
        if asset:
            if not ASSET.fullmatch(asset):
                return []
            urls.append(f'{CLAN_CDN}/{clan}/{asset}')
    for item in IMAGE.findall(body):
        url = html.unescape(item.strip()).replace('{STEAM_CLAN_IMAGE}', CLAN_CDN)
        parts = urlsplit(url)
        if (parts.scheme != 'https' or parts.hostname not in MEDIA_HOSTS or parts.username
                or parts.password or not re.search(r'\.(?:png|jpe?g|webp)$', parts.path, re.I)):
            return []
        urls.append(url)
    unique = {}
    for url in urls:
        filename = urlsplit(url).path.rsplit('/', 1)[-1]
        unique.setdefault(filename, url)
    return list(unique.values()) if 1 <= len(unique) <= 4 else []


def steam_posts(appid, get, valid_date):
    details = get(STORE + '/api/appdetails', appids=appid, l='english').get(str(appid), {})
    info = details.get('data', {})
    publishers = info.get('publishers', [])
    if not details.get('success') or info.get('type') != 'game' or not publishers:
        return []
    if {3, 4}.intersection(info.get('content_descriptors', {}).get('ids', [])):
        return []
    output = []
    for offset in range(0, 96, 24):
        result = get(STORE + '/events/ajaxgetpartnereventspageable/', appid=appid,
                     count=24, offset=offset, l='english')
        events = result.get('events', [])
        observed = datetime.now(timezone.utc).isoformat()
        for event in events:
            announcement = event.get('announcement_body') or {}
            if (event.get('appid') != appid or event.get('published') != 1 or event.get('hidden')
                    or event.get('unlisted') or announcement.get('hidden') or announcement.get('banned')
                    or event.get('event_type') in (12, 14) or 'patchnotes' in announcement.get('tags', [])):
                continue
            gid = str(event.get('gid', ''))
            if not gid.isdecimal() or str(announcement.get('event_gid')) != gid:
                continue
            headline = announcement.get('headline') or event.get('event_name') or ''
            body = announcement.get('body') or ''
            if PATCH.search(headline) or len(body) > 15000 or not OFFER.search(headline + '\n' + body[:2400]):
                continue
            likes = announcement.get('voteupcount')
            replies = announcement.get('commentcount')
            dislikes = announcement.get('votedowncount')
            if not all(type(n) is int and n >= 0 for n in (likes, replies)):
                continue
            stamp = announcement.get('posttime')
            if type(stamp) is not int or not 1609459200 <= stamp <= 2147483647:
                continue
            published = datetime.fromtimestamp(stamp, timezone.utc).isoformat()
            if not valid_date(published):
                continue
            try:
                images = source_images(event, body, announcement.get('language', 0) or 0)
            except (TypeError, ValueError, KeyError):
                continue
            if not images:
                continue
            body_clean = re.sub(r'\[img(?:\s[^\]]+)?\].*?\[/img\]', '', body, flags=re.I | re.S)
            body_clean = re.sub(r'\[url=([^\]]+)\]([^\[]*)\[/url\]', r'\2 (\1)', body_clean, flags=re.I)
            body_clean = re.sub(r'\[/?(?:[a-z][a-z0-9_]*)(?:=[^\]]*)?\]|\[\*\]', '', body_clean, flags=re.I)
            url = f'{STORE}/news/app/{appid}/view/{gid}'
            output.append({
                'ad_id': 'STEAM_' + gid, 'uri': url, 'handle': str(appid), 'platform': 'Steam',
                'publisher': ' / '.join(publishers), 'profile_url': f'{STORE}/news/app/{appid}',
                'url': url, 'caption': html.unescape(headline + '\n\n' + body_clean.strip()),
                'published_at_utc': published, 'observed_at_utc': observed,
                'metrics': {'likes': likes, 'replies': replies, 'dislikes': dislikes},
                'media_kind': 'image', 'media_urls': images, 'alt_text': [None] * len(images),
            })
        if len(events) < 24:
            break
    return output
