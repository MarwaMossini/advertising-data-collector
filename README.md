# Curated public advertising collector

This repository processes a list of public post URLs that you add to `sources.json`. It does not search all of Facebook, Instagram, TikTok, or YouTube. A run can happen without you prompting ChatGPT, but it only processes URLs already in that list.

## What a run does

- Accepts one public HTTPS post URL per source from Facebook, Instagram, YouTube, or TikTok.
- Records the publisher, post text, publication date when exposed, and any public metrics the extractor returns. Missing likes, comments, shares, views, saves, or follower counts stay blank; zero is kept as zero.
- Downloads a single supported image or video when the platform exposes the original media. It skips galleries and does not split videos into frames.
- Adds one row per post to `data/ads.csv`. Each run’s metrics go to `data/engagement_snapshots.csv`, so repeated checks do not create duplicate ads.
- Marks every automated record `needs_review`. Metadata extraction does not prove the post is an advertisement or that counts match what a person sees on the platform.
- Shows the run report in the GitHub Actions summary and saves the cumulative data as an `ad-dataset` artifact.

## Add links

Edit `sources.json` and add entries like:

```json
{
  "url": "https://www.instagram.com/p/POST_ID/",
  "platform": "Instagram",
  "company": "Brand name",
  "industry": "Industry",
  "promotion_type": "Product promotion",
  "paid_status": "unknown"
}
```

Use a direct post URL, not a profile or search page. Keep each entry valid JSON. Do not add cookies, account passwords, or access tokens to this public repository. The sample source is a public Facebook URL; replace or extend it with the public posts you want checked.

## Run it

In GitHub, open **Actions → Collect curated public ads → Run workflow**. The workflow also runs when the collector, source list, tests, or workflow file changes on `main`. It is not on a daily timer yet; first check that your chosen links work reliably.

Open the run summary to see added ads, new snapshots, totals, and failures. Open the run’s **Artifacts** section and download `ad-dataset` to get the CSV files and media folder. Artifacts expire after 90 days under the current workflow, so download periodic backups. This does not create or update the Excel workbook or Google Drive folder automatically.

## Limits

Public pages can block automated requests, require sign-in, or change their page structure. In those cases the run records a failure; it does not bypass the block. Some platforms do not expose all metrics. Instagram saves, share counts, and follower counts are commonly unavailable through public extraction. An unavailable metric is not zero. Exact publication dates can also be absent.

The workflow only processes the URLs you curate. It cannot find new brands or ads on its own. A platform’s official API with approved access is the better route for dependable recurring metrics, but APIs may restrict fields, historical data, and media access. Never place credentials in a public file; if an approved API is later added, store its token in GitHub Actions Secrets.

GitHub Actions stores the output as a temporary downloadable artifact, not as a permanent Drive folder. Upload the extracted dataset to your own Drive for durable storage. Avoid committing ad media into this public repository.

## Local checks

Install Python 3.12, Node.js 22, ffmpeg/ffprobe, and dependencies:

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python collector.py --limit 25
```

The local output folder defaults to `data/` and is excluded from Git.
