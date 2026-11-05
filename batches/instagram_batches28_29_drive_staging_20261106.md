# Instagram promotional collection and Drive staging, 6 November 2026 (Bangladesh)

## Status

- Original master [Master_Ads.xlsx](https://docs.google.com/spreadsheets/d/1vzXBlvO-ckqJ6U9-ypNA-cSy3yK4BV-s/edit) remains **616 records** (49 columns, one Ads worksheet) because the 34 new posts are pending independent editorial/Instagram-UI engagement review and individual-media import.
- New source discovery: **40 Instagram creator promotional URLs** from eight brands; batches 28 and 29 attempted all 40. Collector yielded **34 intact original MP4-backed posts**; six failures excluded (4 in batch 28, 2 in batch 29). No platform restriction bypass attempted.
- Full GitHub verification workflow [run 42086652672](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/42086652672) reported **34 of 34 media integrity passes**: SHA256 against archived extract, FFmpeg entire video decode, date in 2021–2026, no duplicate post IDs / media hashes against source 616-record master, and at least one nonempty exact engagement measure.
- **All 34 have extracted exact likes and comments**. No views were exposed by this collector; do not infer view count from reactions or engagement. Counts are source-extractor values not independently observed in Instagram UI.
- Four videos have suspect low extracted likes (3 likes), including two with substantially more comments than likes, and were flagged in individual manifest rows. Do not train with these counts without cross-checking.
- Brands: Nike 4; Temu 1; Amazon 2; Sephora 3; Garnier 4; SHEGLAM 9; Neutrogena 5; Coca-Cola 6.
- Source collection timestamp was **5 November 2026 UTC (18:11–18:32)**, which is **6 November 2026 Asia/Dhaka**, so the local observation date must be 2026-11-06. The source publication calendar days are platform-derived, not independent UI date observations.
- All collection files are **provisional** until the original creator post and promotion content and visible counters are manually reviewed. Paid status and locations are unknown unless sourced.

## Permanent media backup in existing Google Drive

Original full MP4s plus `ads.csv`, `engagement_snapshots.csv`, and a provenance README were repackaged into five archives, each below 100 MiB, through [GitHub staging run 42088030024](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/42088030024).

The five ZIP files were successfully uploaded into the **existing** Drive project `Advertising Thesis Dataset/backup/`:

| Package | Number of MP4 files | Drive link |
|---|---:|---|
| part01 | 11 | https://drive.google.com/file/d/1IY1Jv2IdU91kCen8_wTanp1t79IBcLbS/view |
| part02 | 5 | https://drive.google.com/file/d/10UpwJTtU8ZtH6Xhyf4B_p9P8tEc_A4Zm/view |
| part03 | 12 | https://drive.google.com/file/d/1EPQVv7UFMCGzLCN_ICA8gUac6TyxI2AW/view |
| part04 | 4 | https://drive.google.com/file/d/1fTf127f9C7AavvsUvmdOzoYhcW_vOywj/view |
| part05 | 2 | https://drive.google.com/file/d/1F9OGuorDXoII1MCwqpmj6U6BU2pDG0Cb/view |

Metadata readback verified each name and parent folder ID `1QT-C_KSxh866i8V3VSUECgttJNhZ9b5q`. These are ZIP **backups**, not individual files in the final `media/` folder. Do not mark a candidate's `media_status` as uploaded to `media/` on the basis of its ZIP presence.

## Audit and original-post links

Individual original links, captions, publication evidence, observation UTC/local date, SHA256, video sizes, exact extractor likes/comments, suspect-count flags:

[Pending review manifest](https://github.com/MarwaMossini/advertising-data-collector/blob/main/batches/instagram_batches28_29_pending_review_20261106.json)

Additional provenance:
- [Batch 28 collection run](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/42081829513)
- [Batch 29 collection run](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/42084897765)
- [Full decode / SHA / dedup audit](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/42086652672)

## Follow-through required before main-master append

The local file-processing environment was unavailable during this work. Accordingly, no unsafe or partial write was made to original master. The next successful file-backed session should (1) download/extract the five ZIPs into 34 whole MP4s; (2) inspect promotional creative and manually cross-check visible Instagram counters, especially suspect 3-likes cases; (3) copy accepted individual `IG_<shortcode>.mp4` files into original Drive `media/` folder and verify them; (4) make a timestamped backup of master; (5) append rows in its existing one-sheet 49-column XLSX, retaining 2026-11-06 metric observation date, fields for missing counts blank, never fabricating views; (6) re-read workbook to confirm no duplicate IDs and exact physical media mapping. Preserve all previously accepted 616 records.
