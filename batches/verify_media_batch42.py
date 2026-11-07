"""Retrieve and validate the complete media set for curated public posts."""

import concurrent.futures
import subprocess
import tempfile
import hashlib
import io
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

from PIL import Image

MEDIA_HOSTS = {'pbs.twimg.com', 'video.twimg.com', 'cdn.bsky.app', 'files.mastodon.social', 'cdn.masto.host', 'social-cdn.vivaldi.net'}
MAX_BYTES = 30 * 1024 * 1024
EXTENSIONS = {'JPEG': '.jpg', 'PNG': '.png', 'WEBP': '.webp'}


def validate_media_url(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname not in MEDIA_HOSTS or parsed.username or parsed.password:
        raise ValueError('Expected an original platform media URL')


class PlatformRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file, status, message, headers, new_url):
        validate_media_url(new_url)
        return super().redirect_request(request, file, status, message, headers, new_url)


def probe_video(path, expected_ms):
    probe = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', path],
        capture_output=True, check=True, timeout=45)
    media = json.loads(probe.stdout)
    streams = media['streams']
    picture = next(stream for stream in streams if stream['codec_type'] == 'video')
    duration = float(media['format']['duration'])
    if not duration > 0 or expected_ms and abs(duration - expected_ms / 1000) > 1.2:
        raise ValueError('Video duration disagrees with the platform')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', path,
        '-map', '0:v:0', '-map', '0:a?', '-f', 'null', '-'],
        capture_output=True, check=True, timeout=100)
    return {'width': picture['width'], 'height': picture['height'], 'duration': duration,
        'has_audio': any(stream['codec_type'] == 'audio' for stream in streams)}


def collect(source, destination):
    ad_id = source['ad_id']
    try:
        if not re.fullmatch(r'(X_[0-9]+|BSKY_[a-z0-9]+|MAST_(?:mastodon\.social|floss\.social|social\.vivaldi\.net)_[0-9]+)', ad_id):
            raise ValueError('Invalid platform post identifier')
        urls = source['media_urls']
        video = source['media_kind'] == 'video'
        if not 1 <= len(urls) <= 4 or (video and len(urls) != 1):
            raise ValueError('Unexpected number of media URLs')
        files = []
        for number, url in enumerate(urls, 1):
            validate_media_url(url)
            with urllib.request.build_opener(PlatformRedirect).open(url, timeout=35) as response:
                data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError('File exceeds download limit')
            video_fields = {}
            if video:
                extension = '.mp4'
                with tempfile.NamedTemporaryFile(suffix='.mp4') as file:
                    file.write(data)
                    file.flush()
                    meta = probe_video(file.name, source.get('duration_ms'))
                    width, height = meta['width'], meta['height']
                    video_fields = {'duration_seconds': meta['duration'], 'has_audio': meta['has_audio']}
            else:
                with Image.open(io.BytesIO(data)) as image:
                    image.load()
                    extension = EXTENSIONS[image.format]
                    width, height = image.size
            filename = ad_id + (f'_{number}' if len(urls) > 1 else '') + extension
            files.append((data, {'filename': filename, 'bytes': len(data),
                'sha256': hashlib.sha256(data).hexdigest(), 'width': width, 'height': height,
                'source_url': url, **video_fields}))
        for data, metadata in files:
            (destination / metadata['filename']).write_bytes(data)
        return {'ad_id': ad_id, 'url': source['url'], 'status': 'complete',
            'assets': [metadata for _, metadata in files]}
    except Exception as error:
        return {'ad_id': ad_id, 'url': source['url'], 'status': 'failed', 'error': str(error)[:300]}


def main():
    sources = json.loads(pathlib.Path(sys.argv[1]).read_text())
    output = pathlib.Path(sys.argv[2])
    media = output / 'media'
    media.mkdir(parents=True, exist_ok=True)
    if len({source['ad_id'] for source in sources}) != len(sources):
        raise ValueError('Duplicate post ID in batch')
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as workers:
        results = list(workers.map(lambda source: collect(source, media), sources))
    (output / 'manifest.json').write_text(json.dumps(results, indent=2))
    complete = sum(result['status'] == 'complete' for result in results)
    print(f'{complete}/{len(sources)} posts have complete, decodable media sets')
    if not complete:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
