# Batch 27: Instagram and TikTok creator promotions, 2026-11-05

**Drive update completed.** Original Excel [Master_Ads.xlsx](https://docs.google.com/spreadsheets/d/1vzXBlvO-ckqJ6U9-ypNA-cSy3yK4BV-s/edit) increased from **608 to 616** unique advertising records. This update kept the single `Ads` tab and **49-column** structure and original Drive file ID. The eight added ads are rows **610–617**.

## Eight new original Instagram promotional posts

| ID | Advertiser | Published day, platform UTC timestamp | Likes exact | Comments exact | Direct original post |
| --- | --- | --- | --- | --- | --- |
| `IG_DVjLG_ugIuA` | Nike | 2026-03-06 | 1261 | 65 | https://www.instagram.com/p/DVjLG_ugIuA/ |
| `IG_DSOKb2PiRLa` | Nike | 2025-12-13 | 805 | 656 | https://www.instagram.com/p/DSOKb2PiRLa/ |
| `IG_Db1iwr2gAfO` | Temu | 2026-08-09 | 1086 | 94 | https://www.instagram.com/p/Db1iwr2gAfO/ |
| `IG_Db03qj8OBcU` | Temu | 2026-08-09 | 1803 | 26 | https://www.instagram.com/p/Db03qj8OBcU/ |
| `IG_Db0J_mAMUNI` | Temu | 2026-08-09 | 2101 | 1320 | https://www.instagram.com/p/Db0J_mAMUNI/ |
| `IG_DbOcRT6KyaD` | Amazon | 2026-07-25 | 11477 | 147 | https://www.instagram.com/p/DbOcRT6KyaD/ |
| `IG_DaXxOYat4rQ` | Amazon | 2026-07-04 | 3350 | 14702 | https://www.instagram.com/p/DaXxOYat4rQ/ |
| `IG_C41EB_MOfYn` | Nike | 2024-03-22 | 92352 | 126 | https://www.instagram.com/reel/C41EB_MOfYn/ |

The source videos and individual public engagement fields were extracted by `collector.py` in GitHub workflow run [42075750159](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/42075750159), and their full original MP4s were checked against archive SHA-256 and decoded fully with ffmpeg. Captions include clear product/promotion or `#ad` calls to action; source videos were reviewed with contact-frame thumbnails. Captions are retained intact in Excel.

All eight full MP4s, named `IG_<Instagram shortcode>.mp4`, are in the existing original [Google Drive media folder](https://drive.google.com/drive/folders/1QW4f9iy-tTbGaTUHSG-iYnJxEJXHrC6f). Every Drive file's name, size and correct parent folder were confirmed via Google Drive metadata. Each workbook media path matches the name.

**Provenance and uncertainty**:
- Original platform publication dates from `timestamp` in UTC, not manually reobserved in the UI.
- Likes/comments from public yt-dlp extractor on **2026-11-05 UTC** (today's same-day measurement); **not** a verified live human observation. Source recorded timestamps are preserved.
- Views, shares, saves and followers unavailable in the extractor remain **blank**. They are not zeros. Exact like/comment values are not rounded.
- The user caption `#ad` may disclose a creator arrangement. Paid media delivery/targeting is not proven; country is unknown unless sourced.
- Eight records remain **provisional** until original Instagram UI counts are independently checked.
- Group all repeated creative/campaign edits in train/test splitting to reduce leakage.

The five TikTok candidates in the same batch **failed original-page retrieval**, so **no TikTok record was added**. No bypass attempted. Use the archived run's `latest_run.json` for per-URL errors.

## Backups and audit
- Old 608-ad master preserved before modifying: [backup file](https://docs.google.com/spreadsheets/d/1zx-ZoGLfKMEOYP9Dkvp2uRl-anzOSVHg/edit).
- Full [batch 27 verification manifest](https://drive.google.com/file/d/1c1lqA76eTMGZRMnNZWIp0_yVIcia13Zr/view) in the existing Drive backup folder, includes SHA-256, media durations, source metrics and failed TikTok URLs.
- Post-upload Google Drive readback: 616 rows, 616 unique IDs, 49 columns, and all 8 uploaded MP4s with matching names/parents.
- Discovery sources: public creator sponsorship listings (CollabFeed brand pages for Nike, Temu, Amazon) and a Nike Air Max independent creator campaign example. Entries were only accepted when platform original media itself was accessible and validated.
