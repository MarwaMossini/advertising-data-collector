# Batch 36: eight public X promotions

Completed on 2026-11-07 using Asia/Dhaka collection calendar dates. Original UI observations were made at 2026-11-06T18:59:18Z–19:00:02Z. GitHub collected complete media at 19:02:01Z–19:02:40Z. No login, cookies, proxy or access-control workaround was used.

The [same Drive master](https://docs.google.com/spreadsheets/d/1vzXBlvO-ckqJ6U9-ypNA-cSy3yK4BV-s/edit) now contains **776 records** in one `Ads` tab, with 49 columns. The eight additions occupy rows **770–777**. Existing 768 records, values, types, styles, widths, row dimensions, panes, views and validations were preserved. The native `IncludedAds` table and filter extend to `A1:AW777`.

## Added records

- Starbucks: two distinct single-image promotions for its February 2025 free-coffee Monday offer.
- Pokémon TCG: two complete videos and two single images promoting new trading cards and expansions.
- Xiaomi India: two single-image product promotions, for Xiaomi 18 Pro and the Mijia Smart Air Purifier 4 Compact.

All eight original posts expose numeric likes, replies, displayed reposts, bookmarks and post views. Publisher follower labels were checked on their original profiles. See [accepted record evidence](batch36_20261107_accepted.json) for post URLs, timestamps, counters, dates, file hashes and Drive IDs.

## Original media

The [Videos folder](https://drive.google.com/drive/folders/1_hn7vQgercWWNfs3j1JVJWk7XM9GdL8O) now contains **722 complete MP4s**. The [Images folder](https://drive.google.com/drive/folders/1yHwLpNE5JB5XnHbU-MFdWY2o2iNq3cLG) contains **81 images: 73 JPEGs and eight WEBPs**. Both new videos retain video and audio streams. No standalone audio was extracted.

All eight media SHA-256 hashes differ from the existing master and from each other. Both MP4s passed full decoding; all six WEBPs passed image decoding. All images and video previews at 15%, 55% and 85% were inspected. Preview frames were temporary quality checks, never dataset assets. The camera-interface graphics in one Pokémon video belong to the original creative.

All **803 asset references** in the master match one Drive file in the correct type folder. New filenames, MIME types and byte sizes match the accepted downloads. All 795 older files retain their IDs, names and sizes.

## Dates and metric meanings

Six image dates use the explicit calendar date on the original X post. The UI does not specify a timezone; the workbook and collector evidence retain that uncertainty and do not present these as UTC timestamps. Both video dates use original-platform extractor UTC timestamps; the separate original UI labels are retained.

Comments map to replies; saves map to public bookmarks; reposts use the original displayed repost counter. Extractor repost counters differ and remain separate in the private audit. Views are post views, not verified video plays or unique users. Shares, total reactions, dislikes and exact follower counts are unavailable and remain blank. Rounded profile follower labels are not ad reach or historical audience counts.

These are public brand promotions; paid distribution and targeting country are unknown. Related Starbucks Monday and Pokémon Delta Reign creatives should be grouped in later train/test splits. Offers and release claims are advertiser statements. Older records retain their previous verification statuses and have not all been freshly reverified.

LinkedIn company pages checked in this session required sign-in, so no LinkedIn entries were added.

## Reproducibility and saved verification

[Successful GitHub run 42275999189](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/42275999189) used collection commit `8eff18b4029e9d96070caff4dc4db2e33959fe8d`. Whole files were packaged in bounded artifact groups without segmenting any creative.

The collector now accepts an explicitly reviewed image date, original UI time label, observation timestamp and caption. It rejects mismatched date labels and missing observation times. Three new regression checks and the repository checks passed.

The previous 768-record workbook was backed up as Drive file `1okLsfxe5wjX3V4prsMlvgF8MB7_ypn6n`. The detailed private audit is Drive file `1pO4gu2Be6wIhIOqZmEZlrgyImEzGfVCz` in the existing backup/audit folder.

The uploaded master was downloaded again and is byte-identical to the local checked export: SHA-256 `4692cb93e5bdb3e93bb01fd11279df12c7b487f8e182c204a366558c097c674a`. Readback confirmed 776 records, one tab, 49 columns and the extended native filter.

The code processes curated links. Discovery, original-UI verification and reviewed Drive updates are not an unattended automatic pipeline.
