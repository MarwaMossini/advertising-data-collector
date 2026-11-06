# Curated public advertising collector

This repository processes a list of public post URLs that you add to `sources.json`. It does not search all of Facebook, Instagram, TikTok, or YouTube. A run can happen without you prompting ChatGPT, but it only processes URLs already in that list.


## Current reviewed Drive dataset

After batch 37 on 2026-11-07, the [same master workbook](https://docs.google.com/spreadsheets/d/1vzXBlvO-ckqJ6U9-ypNA-cSy3yK4BV-s/edit) has 786 records in one `Ads` tab. See the [batch 37 verification report](batches/batch37_20261107_drive_update.md) for source evidence and limitations. Older verification statuses remain unchanged.

The [Media folder](https://drive.google.com/drive/folders/1QW4f9iy-tTbGaTUHSG-iYnJxEJXHrC6f) contains [Videos](https://drive.google.com/drive/folders/1_hn7vQgercWWNfs3j1JVJWk7XM9GdL8O) (724 MP4s) and [Images](https://drive.google.com/drive/folders/1yHwLpNE5JB5XnHbU-MFdWY2o2iNq3cLG) (89 images: 73 JPEGs and 16 WEBPs). All 813 asset references in the workbook match these sections. Original ad-ID filenames and existing Drive file IDs are preserved. Audio stays inside videos; there is no standalone audio collection yet. Asset counts differ from ad counts because some older records have multiple assets.

The additional `collect_other_platforms.py` workflow handles explicitly curated public X videos and source-verified images, plus LinkedIn publisher images. Run it with `python collect_other_platforms.py --config batches/public_promotions_20261107_batch37.json --out public_promotions_batch37`, or select **Verify public promotions batch thirty-seven 2026-11-07** in Actions. It writes `candidates.json`, `latest_run.json` and complete media. Images must be verified on their original publisher post before source URLs are curated. Their date may use an explicit original UI calendar label with a recorded observation timestamp and caption; its unspecified timezone is retained. Otherwise publication dates require original-platform metadata. These are candidates requiring original-platform UI and media review, not automatic Drive additions. Missing counters stay blank. The workflow does not discover new links itself or bypass access restrictions.

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
