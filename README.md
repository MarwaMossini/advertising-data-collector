# Public promotional video collector

Prepared for Marwa's multimodal advertising thesis. This project is being deployed for its first live validation.
Daily scheduling remains disabled until a live collection run has been verified.

## What it does

- Searches YouTube using the configured brand queries and exact uploader-name filters.
- Processes explicitly listed public Facebook video URLs. It does not discover Facebook posts across the whole platform.
- Downloads single videos of 1–300 seconds published in 2021–2026, checks their video stream with ffprobe, and records available engagement metadata.
- Keeps missing values empty, deduplicates IDs and identical downloaded bytes, and saves CSV progress after each accepted video.
- Stops a platform for the current run if access errors mention sign-in, CAPTCHA, bots, 403 or 429. It supplies no Facebook/YouTube login, cookies or proxy.
- Limits collection to 10 successful videos per run and about 2 GiB of cumulative media. This initial version collects videos only; image posts and galleries are not supported.

The outputs are **candidates**, not verified advertisements. Exact uploader-name filters and keywords do not prove official ownership, promotional relevance or paid status. Inspect each candidate before merging it into the verified thesis dataset. Metadata returned by an extractor may differ from the visible page counts. The existing 26-post dataset stays separate and is not overwritten or relabelled.

## First run on GitHub

The initial workflow upload to main triggers a test collection. It can also be started manually from Actions. Check latest_run.json and the downloaded video before enabling a daily schedule. The intended schedule is 02:17 UTC (08:17 Bangladesh); it is not enabled yet.

## Results and continuity

Each successful workflow uploads `ad-dataset`, containing `candidates.csv`, `media/`, and `latest_run.json`. The next run restores the previous successful run's artifact before collecting. A restore error stops the job instead of silently starting over. The first run starts empty.

Artifacts are requested with 90-day retention, subject to repository policy. This is temporary working storage, not a permanent thesis archive. Download regular backups. If the last artifact expires or is removed, restore your backup before rerunning. GitHub storage/minute quotas can also stop runs; do not enable paid overages without reviewing them. Failed or interrupted runs may lose additions since the last successful uploaded artifact.

The schedule will not guarantee 10 new videos daily. Search results can repeat, public access can fail, the Facebook URL queue can be exhausted, and candidates may fail the filters. Repeated candidates are skipped. The run report records failures and exclusions.

## Run locally

Install Python 3.12, Node.js 22 and ffmpeg/ffprobe. Then:

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python collector.py --limit 10
```

Outputs go into `data/`, excluded from Git. The dependency is pinned to the locally tested version; update deliberately if a site's format changes.

## Data definitions

`recorded_at_utc` is the time the metadata was collected. `published_date` is the extractor's upload date, which may differ from the displayed date in another timezone. Likes, comments and views are numeric when supplied by the extractor. Shares remain blank because the current extraction route does not provide a reliable share count. The caption is only a 25-word excerpt. `sha256` identifies the downloaded file. `review_status=needs_review` must be resolved through actual review, not changed merely because a download succeeded.

## References

- https://github.com/yt-dlp/yt-dlp
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
