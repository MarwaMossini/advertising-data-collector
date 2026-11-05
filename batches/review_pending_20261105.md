# 2026-11-05 collection review — batches 23 and 24, archived media audit

## Current accepted dataset

The Google Drive master had 592 rows of ads, 49 data columns and no repeated `ad_id` values at the read preceding these checks. This review does **not** append any row or modify any existing Drive asset.

## Newly attempted collection

- Batch 23: eight original promotional YouTube URLs queued at `batches/public_promotions_20261105_youtube_batch23.json`. Workflow [41894784678](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/41894784678) completed its execution, but **zero accepted media-backed records**: one private video, then an explicit YouTube sign-in/bot-verification restriction. Six later URLs skipped rather than bypassed.
- Batch 24: two public Facebook URLs queued at `batches/public_promotions_20261105_facebook_batch24.json`. Workflow [41895256232](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/41895256232) yielded **zero accepted records**. The Lumsleeshdiaries/L’Oréal video lacked a usable 2021–2026 publication date; the Saiful Express video did not yield exactly one complete original media file. Treat both as failures, not dataset samples.

## Media-backed historical candidates uncovered while deduplicating

The following older GitHub artifacts contain original full MP4 files; the listed media files' SHA-256 values matched their original CSV provenance during local inspection. These IDs were **not** in the 592-row Drive master. They **remain under review**, not accepted new records. The archived interaction counts were observed **2 November 2026**, *not* during this new review.

| Native Facebook ID | Original Facebook post | Published (platform UTC timestamp) | Public archived views (rounded) | Total reactions (exact) | Promotion rationale | Original archive |
|---|---|---|---|---:|---|---|
| `1256921419578207` | https://www.facebook.com/PUMA/videos/1256921419578207/ | 2026-05-26 | 71K | 110 | Explicit launch of PUMA Stellar NITRO Ultimate matchballs for 2026/27 | [batch 19 run 41460004517](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/41460004517) |
| `1836223834395087` | https://www.facebook.com/SonyElectronics/videos/1836223834395087/ | 2026-10-09 | 8.3K | 56 | Sony WH-1000XM6 headset placement in an NFL collaboration post | [batch 20 run 41486060782](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/41486060782) |
| `1744004273322477` | https://www.facebook.com/SonyElectronics/videos/1744004273322477/ | 2026-10-05 | 8.4K | 63 | Sony 1000X THE COLLEXION headset placement in an NFL collaboration post | [batch 20 run 41486060782](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/41486060782) |

### Important caveats

- The archived extracts provide video views and **total reactions**, not separate likes. Comment and share counts were **unavailable**, not zero. Exact view fields stay blank because the displayed view labels are rounded.
- The publication day comes from platform `timestamp` interpreted in UTC, not a manually independently witnessed Reel calendar date.
- The historical candidates may have been omitted earlier on editorial/quality grounds. They should not silently be promoted to verified ads without a deliberate quality review.
- The full MP4 files exist in GitHub run artifacts and were inspected locally. Individual videos were not uploaded to the persistent Drive media folder during this review, so **no workbook rows were added**.
- A workflow concluding `success` only means it executed and archived its report; it does not certify positive collection results.

Next step: obtain independent comment/share UI counts if publicly accessible, review the promotional content and exact media at source, and upload each accepted full MP4 to the original Drive media folder before appending an ID-matched row to the original master. Do not overwrite the original workbook or change historical observation dates without a verified compatible upload.


## Update, 5 November 2026 (Asia/Dhaka): saved to original Google Drive master

At the user's explicit request, **three** archival MP4-backed records were appended to the **same** Google Drive master, with IDs `FB_1256921419578207`, `FB_1836223834395087`, and `FB_1744004273322477`. The table now has **595 total records in 49 columns, one Ads tab**, and no duplicate ad IDs. These are **provisional media-backed records**; their Facebook UI engagement counts, comments and shares have not been independently rechecked. They are distinct from the 592 earlier records already in the master.

The full original MP4s, renamed `FB_<native_post_id>.mp4`, were uploaded to the **existing** Drive media folder. Their SHA-256 digests matched the archive records and the video/audio streams decoded. The master retains the original platform-derived UTC publication dates and **2 November 2026** metric observation dates; 5 November is recorded only for media upload/recovery. Rounded `views_display` and exact `reactions_exact` are retained, with unknown likes, comments, shares, saves, reposts and followers blank. Views exact is blank. Paid delivery and country remain unknown.

Before overwriting the original master, an exact copy of the 592-row workbook was placed in the existing `backup` folder as `Master_Ads_backup_592_ads_before_2026-11-05.xlsx` (Google Drive file ID `1Nu1oiQFMMoCKb2TbSNW1upew3kffSFU5`). The updated master kept its original file ID `1vzXBlvO-ckqJ6U9-ypNA-cSy3yK4BV-s`. Readback confirmed 595 unique IDs and three full MP4s in folder ID `1QW4f9iy-tTbGaTUHSG-iYnJxEJXHrC6f`.

Historical note: the earlier section above describes the status **before** this user-approved update; it is now superseded for these three records.
