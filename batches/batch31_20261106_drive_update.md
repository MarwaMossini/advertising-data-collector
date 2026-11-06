# Facebook batch 31: UNIQLO promotions, 6 November 2026

The original [Master_Ads.xlsx](https://docs.google.com/spreadsheets/d/1vzXBlvO-ckqJ6U9-ypNA-cSy3yK4BV-s/edit?usp=drivesdk&ouid=111122819832787064775&rtpof=true&sd=true) now contains **697 unique records**, up from 675. The 22 new Facebook ads occupy rows **677–698** on the same Ads worksheet and retain its 49-column structure.

Source discovery and direct review covered 30 original public UNIQLO videos. [GitHub collection run 42167570184](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/42167570184) retrieved all 30 original full MP4s and their source metadata. Eight candidates were excluded after review; they were not appended or uploaded to the final media folder.

## Accepted content and verification

The 22 retained creatives promote AIRism, jeans, shorts, seasonal collections, knitwear, fleece, HEATTECH, kids/baby clothing, UNIQLO collaborations and a sponsored event invitation. They include television commercials, product animations, collection teasers and a collection-launch video with a concrete retail availability announcement.

One record, FB_1530672614204003, promotes an invitation for children to a UNIQLO-sponsored baseball exhibition through Ichiro POST. It is explicitly labeled as an event invitation rather than a clothing sale. Related Roger Federer and UNIQLO:C collection edits are flagged for grouped evaluation splits.

Caption languages: eight English; fourteen Japanese or mixed Japanese/English. Original captions are retained intact. English product/offer descriptions are labeled as descriptive translations where needed. Caption language does not establish targeting country.

Original Facebook posts were independently reviewed on 6 November 2026, UTC 05:17–05:20. Every accepted record has visible numeric total reactions, comments and shares. Original-platform extractor metadata provides views for all 22 and publication dates from **28 July 2024 to 27 May 2025**.

## Metric and date provenance

- Reactions, comments and shares are direct UI observations, with individual observation times in the audit.
- Views are source-extractor values, not independently observed Reel UI counts. Fifteen view values are unrounded integers and seven are rounded labels. Exact fields remain blank for rounded values.
- Facebook total reactions are distinct from likes. Separate likes and reaction breakdowns remain blank.
- The verified Uniqlo publisher page displayed 1.1M followers at 2026-11-06T05:20:57.786Z. This is a rounded current page count, not reach or historical campaign audience.
- Exact publication days use original platform timestamps in UTC. The Reel UI did not independently display exact calendar dates. First/latest collection dates use Asia/Dhaka, 6 November 2026.
- Saves, reposts and other unavailable counts remain blank. Paid media delivery and targeting geography remain unknown.

## Exclusions

Five product-related candidates had no visible numeric comment count and were excluded: FB_1074877360816644, FB_3555670758026038, FB_1065139025155440, FB_1634476153952576 and FB_1409930970409831. A missing UI count was not treated as zero.

Three others were excluded for content outside this batch's promotional scope: FB_860378996297412, a community/athlete visit story; FB_792163716274661, a past exhibition recap; and FB_864594791966365, a sports partnership thank-you and medal recap. These lacked a clear product offer or forward-looking invitation call to action.

## Media and workbook preservation

All 30 downloaded files passed archived SHA256 verification, full FFmpeg decode and visual preview review. No duplicate original post IDs or media hashes were found among the accepted records or against the original 675-record master.

All 22 accepted whole MP4s, about 8.5 minutes in total, were individually uploaded to the existing [Drive media folder](https://drive.google.com/drive/folders/1QW4f9iy-tTbGaTUHSG-iYnJxEJXHrC6f). Each filename FB_<native ID>.mp4 matches Excel. Drive readback confirmed each filename appears once and has the expected original byte size. No videos were segmented, trimmed or re-encoded.

All 675 previous records, styles, dimensions, freeze panes and validations were preserved. IncludedAds and its filter now cover **A1:AW698**. There is still one Ads worksheet.

A [675-record backup](https://docs.google.com/spreadsheets/d/1-2IscRQmn7Ifnqr9SzHj4GYhk60a9EiV/edit?usp=drivesdk&ouid=111122819832787064775&rtpof=true&sd=true) was saved before replacement. The updated Drive master was downloaded again and verified to contain 697 unique IDs, 49 columns and the correct 22 appended records. Its SHA256 is **9a0373925dd35077e93e416d6b19a99739918f33172375a8e3ef6c85971658f9** (327387 bytes).

[Full audit](https://drive.google.com/file/d/1rBCrp0seX8Yq4na02xclFkOcpJYgZwi0/view?usp=drivesdk) contains the accepted rows, original extracts, UI observations, exclusions, file checks, artifact provenance, upload receipts and workbook/Drive readback checks. The adjacent accepted manifest provides individual IDs, links, dates, display counts, caption languages and media hashes.

The 697 total includes older records whose existing verification statuses remain unchanged; it is not a claim that all 697 were independently UI-verified during this batch.
