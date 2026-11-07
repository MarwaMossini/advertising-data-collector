"""Retrieve and validate the complete image set for curated public posts."""

import concurrent.futures
import hashlib
import io
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

from PIL import Image

IMAGE_HOSTS = {'pbs.twimg.com', 'cdn.bsky.app'}
MAX_BYTES = 20 * 1024 * 1024
EXTENSIONS = {'JPEG': '.jpg', 'PNG': '.png', 'WEBP': '.webp'}


def validate_image_url(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname not in IMAGE_HOSTS or parsed.username or parsed.password:
        raise ValueError('Expected an original platform image URL')


class PlatformRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file, status, message, headers, new_url):
        validate_image_url(new_url)
        return super().redirect_request(request, file, status, message, headers, new_url)


def collect(source, destination):
    ad_id = source['ad_id']
    try:
        if not re.fullmatch(r'(X_[0-9]+|BSKY_[a-z0-9]+)', ad_id):
            raise ValueError('Invalid platform post identifier')
        urls = source['image_urls']
        if not 1 <= len(urls) <= 4:
            raise ValueError('Expected one to four original images')
        files = []
        for number, url in enumerate(urls, 1):
            validate_image_url(url)
            with urllib.request.build_opener(PlatformRedirect).open(url, timeout=35) as response:
                data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError('Image exceeds download limit')
            with Image.open(io.BytesIO(data)) as image:
                image.load()
                extension = EXTENSIONS[image.format]
                width, height = image.size
            filename = ad_id + (f'_{number}' if len(urls) > 1 else '') + extension
            files.append((data, {'filename': filename, 'bytes': len(data),
                'sha256': hashlib.sha256(data).hexdigest(), 'width': width, 'height': height,
                'source_url': url}))
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
    print(f'{complete}/{len(sources)} posts have complete, decodable image sets')
    if not complete:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
