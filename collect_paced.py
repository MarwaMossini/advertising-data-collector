"""Collect explicit public links sequentially with fixed spacing and no access-control workarounds."""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from collector import run

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--limit', type=int, default=40)
    parser.add_argument('--interval-seconds', type=float, default=5)
    args = parser.parse_args()
    if not 5 <= args.interval_seconds <= 60:
        parser.error('interval-seconds must be between 5 and 60')
    config = json.loads(Path(args.config).read_text(encoding='utf-8'))
    sources = config.get('sources', [])[:args.limit]
    summary = {'started_at_utc': datetime.now(timezone.utc).isoformat(),
               'request_spacing_seconds': args.interval_seconds,
               'added_ads': 0, 'new_snapshots': 0, 'events': []}
    for index, source in enumerate(sources):
        if index:
            time.sleep(args.interval_seconds)
        report = run({'sources': [source]}, args.out, limit=1)
        summary['added_ads'] += report['added_ads']
        summary['new_snapshots'] += report['new_snapshots']
        summary['events'].extend(report['events'])
        summary['total_ads'] = report['total_ads']
        summary['total_snapshots'] = report['total_snapshots']
        errors = ' '.join(event.get('error', '') for event in report['events']).lower()
        if any(signal in errors for signal in ('not a bot', 'verify you are human', 'automated traffic')):
            summary['stopped_reason'] = 'Explicit platform bot-verification restriction; no bypass attempted.'
            for remaining in sources[index + 1:]:
                summary['events'].append({'url': remaining.get('url', ''), 'status': 'skipped',
                                          'reason': summary['stopped_reason']})
            break
    summary['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    Path(args.out).mkdir(parents=True, exist_ok=True)
    (Path(args.out) / 'latest_run.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary))

if __name__ == '__main__':
    main()
