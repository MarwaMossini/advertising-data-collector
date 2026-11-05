# Batch 26 — five media-backed promotional videos added on 2026-11-05

## Result
Five previously collected promotional Facebook video posts, absent from the existing master, were recovered from historical GitHub workflow artifacts, inspected and added to the **same** Excel master in Google Drive. The master increased from **603 to 608 records**, retaining **49 columns and one `Ads` tab**. Existing 603 records were byte-for-byte equal at the cell-value level in an export/re-import validation. The 608 ad IDs were unique.

## New original posts and saved metadata

| Ad ID | Brand and promotion | Published date, platform UTC timestamp | Observation date, Bangladesh | Video views | Total reactions (not likes) | Comments | Original link |
|---|---|---|---|---|---|---|---|
| `FB_2277306369475333` | Dyson, Unveiled 2026 event teaser | 2026-09-08 | 2026-11-02 | 2,598 exact metadata scalar | 29 | 24, sourced from returned original-platform title | https://www.facebook.com/Dyson/videos/2277306369475333/ |
| `FB_1568342178317563` | Dyson, Clean+Wash roller maintenance product demonstration | 2026-07-19 | 2026-11-02 | 41K display | 22 | unavailable | https://www.facebook.com/Dyson/videos/1568342178317563/ |
| `FB_28572699819052775` | Dyson, Clean+Wash ten-step maintenance demo | 2026-07-18 | 2026-11-02 | 47K display | 25 | unavailable | https://www.facebook.com/Dyson/videos/28572699819052775/ |
| `FB_1781109092963352` | Ninja Kitchen, 15% off Crispi Glass Air Fryer | 2026-10-11 | 2026-11-02 | 23K display | 104 | unavailable | https://www.facebook.com/ninjakitchen/videos/1781109092963352/ |
| `FB_1177934569375525` | PUMA, Only See Great athlete brand campaign | 2021-08-12 | 2026-11-02 | 15K display | 713 | unavailable | https://www.facebook.com/PUMA/videos/1177934569375525/ |

The 24 Dyson comments are *not* a fresh page-interface observation; they appeared explicitly as an integer in the archived platform-returned title ("29 reactions · 24 comments"). The earlier collector left its comments column blank, so this addition recovers that archived value with labeled provenance. It should still be checked independently against the original post.

## Verification and storage

- Source media artifacts: old GitHub workflow batch 15 (Dyson), batch 21 (Ninja Kitchen), and batch 19 (PUMA).
- All five files checked against archived SHA-256 digests; none matched a pre-existing master SHA-256. Distinct native post IDs and original URLs were absent from prior 603 rows.
- Full source MP4s extracted unchanged, ffprobe validated a video stream, and ffmpeg decoded complete video streams. This is not a collection of video frames.
- Five original MP4s, named `FB_<native_id>.mp4`, uploaded to the existing [Drive media folder](https://drive.google.com/drive/folders/1QW4f9iy-tTbGaTUHSG-iYnJxEJXHrC6f). Google Drive readback verified all five filenames, sizes and folder parents.
- Original existing [Master_Ads.xlsx](https://docs.google.com/spreadsheets/d/1vzXBlvO-ckqJ6U9-ypNA-cSy3yK4BV-s/edit) updated in place, with the same file ID. New Excel rows are **605–609**; dates/observations retained. Imported workbook readback 608 rows of ads / 49 columns.
- A prior-master backup [603-row pre-batch26 version](https://docs.google.com/spreadsheets/d/1XU4eKVNiZskwQKPnDoBkFxW4mXVfnsLl/edit) was placed in the original Drive `backup` folder **before** any master replacement.
- Detailed [source, SHA, media length and metric manifest](https://drive.google.com/file/d/1pkcB7M_u9AiHULIo_dtgKqXg8rK-bplf/view) saved to the same backup folder.

## Limitations

All five new records remain **provisional**. Independent Facebook UI verification of counts and publication-day display is pending. Total Facebook reactions must not be treated as likes. The rounded views labels `41K`, `47K`, `23K` and `15K` are kept as display values with exact fields empty; `2,598` is a metadata-derived exact count. Comments, shares, reposts, saves, follower/subscriber data, or geographic targeting remain unknown except for the 24 title-displayed comments. An unavailable field is blank, not zero. Paid status remains unknown. Related Dyson product demonstrations should be grouped by creative/campaign in ML splits to prevent leakage.

The other archival candidates were not automatically promoted: some lacked engagement measures, were generic brand entertainment without explicit product/campaign purpose, or had contradictory campaign dates. New source discovery using public web search returned several Meta Ad Library creative pages but no qualifying original-platform video URLs that could be validated with media and public engagement in this pass.
