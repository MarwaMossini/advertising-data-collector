# Facebook batch 30: KitchenAid promotions, 6 November 2026

The original [Master_Ads.xlsx](https://docs.google.com/spreadsheets/d/1vzXBlvO-ckqJ6U9-ypNA-cSy3yK4BV-s/edit?usp=drivesdk&ouid=111122819832787064775&rtpof=true&sd=true) now contains **675 unique records**, up from 645. The 30 new Facebook ads occupy rows **647–676** on the same Ads worksheet, with the existing 49 columns.

All 30 original public KitchenAid posts were reviewed directly on Facebook, UTC 04:29–04:32 on 6 November. Each has independently observed total reactions, comments and shares. Original-page video views and publication dates were retrieved by the source extractor in [GitHub collection run 42162818408](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/42162818408). No record was excluded from this batch.

The ads promote stand mixers, mixer bowls/attachments, espresso machines, cordless food preparation appliances, rice cookers and cookware. They include product launches and Jennifer Garner cooking demonstrations. Publication dates range from 27 February 2023 to 20 May 2025, interpreted from original platform timestamps in UTC. English captions are retained intact. The Reel UI did not independently display exact calendar dates.

## Engagement provenance

- Reactions, comments and shares are original UI measurements, with individual observation timestamps in the audit.
- Views are original-platform extractor measurements at each recorded extraction time, not independently observed live UI counts. Twenty-nine view values are unrounded integers; one original view label is rounded 19K and its exact field remains blank.
- Facebook total reactions are not separate likes. Likes and individual reaction breakdowns remain blank.
- The verified publisher page displayed 1M followers at 2026-11-06T04:32:03.415Z. This is a rounded current page-level audience count, not historical audience or ad reach.
- Saves, reposts and other unavailable metrics remain blank. Paid delivery and targeting country are unknown.
- Related campaign/color-launch edits and the Jennifer Garner demonstration series are flagged for grouped training/evaluation splits.

## Original media and workbook checks

All 30 whole original MP4s passed their archived SHA256 check and complete FFmpeg decode, and visual previews were inspected. They total about 35.6 minutes. No original post ID or media hash duplicates were found against the 645-record master or within the batch.

The original artifact exceeded the connector transfer limit. [Packaging run 42163430537](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/42163430537) divided only the archive into five smaller packages. No advertisement was segmented, trimmed or re-encoded. All transfer artifact digests and inner package hashes were verified.

All 30 MP4s were individually uploaded to the existing [Drive media folder](https://drive.google.com/drive/folders/1QW4f9iy-tTbGaTUHSG-iYnJxEJXHrC6f), with filenames FB_<native ID>.mp4 matching Excel. Drive folder readback confirmed one matching filename and expected byte size for every new ad.

All 645 previous records, cell styles, dimensions, freeze panes and validations were preserved. IncludedAds and its filter now cover A1:AW676. There is still one Ads worksheet.

A [645-record backup](https://docs.google.com/spreadsheets/d/1L-GLH3DzSWggLHvcucWUG1iMActIviyw/edit?usp=drivesdk&ouid=111122819832787064775&rtpof=true&sd=true) was saved before replacement. The updated Drive master was downloaded again and verified as 675 unique IDs, 49 columns, 675 data records and the same new row values. SHA256 **4c3953db5d511ce163b5c3381885572f6356787415da581a3cbc849694df4a4d**, 316138 bytes.

[Full audit](https://drive.google.com/file/d/1ZwAxYjXcUAHs5d3RQTLi1OcD-Eq_O0nz/view?usp=drivesdk) contains source extracts, UI observations, local media checks, artifact/package checks, upload receipts and workbook/Drive readback checks. The adjacent accepted manifest lists the 30 new IDs, dates, metric display values, links and media hashes.

The 675 total includes older records whose verification statuses remain unchanged. It is not a claim that all 675 were independently UI-verified in this session.
