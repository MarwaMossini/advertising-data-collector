# Instagram batches 28/29: completed review and Drive update, 6 November 2026

The original [Master_Ads.xlsx](https://docs.google.com/spreadsheets/d/1vzXBlvO-ckqJ6U9-ypNA-cSy3yK4BV-s/edit?usp=drivesdk&ouid=111122819832787064775&rtpof=true&sd=true) now contains **645 unique records**, up from 616. The 29 new Instagram records occupy rows **618–646** on the existing single Ads worksheet with 49 columns.

## Verification and media

All 34 pending originals were opened on Instagram on 6 November 2026, UTC 04:12–04:15. The caption, creator, visible like/comment counts and publication calendar label were reviewed. All 34 original MP4s were checked against their archived SHA256 and byte sizes, fully decoded with FFmpeg, and reviewed with sampled visual previews. Twenty-nine clear promotional videos with visible numeric likes and comments were accepted.

Accepted advertiser counts: Nike 4; Temu 1; Amazon 1; Sephora 2; Garnier 4; SHEGLAM 8; Neutrogena 5; Coca-Cola 4. Captions include English, Polish, French, Spanish, Italian, Portuguese and Albanian, as well as a post containing mainly hashtags/brand mentions. Language notes describe captions, not an independently transcribed spoken language.

Each of the 29 accepted whole MP4s was uploaded individually to the original [media folder](https://drive.google.com/drive/folders/1QW4f9iy-tTbGaTUHSG-iYnJxEJXHrC6f) under its matching IG_<shortcode>.mp4 name. Folder readback confirmed each filename appears once with its expected original byte size.

## Counts, dates and exclusions

- The current workbook measurements come from the visible Instagram UI. Exact integers are stored numerically. Rounded K labels are retained as text, with exact fields blank. Historical extractor counts remain in the audit.
- No numeric shares, saves, reposts, video views or creator follower counts were observed. Those fields remain blank; a Share or Save button is not a count.
- Published date retains the platform UTC timestamp convention. The literal Instagram calendar label is recorded separately. Where UI and UTC calendar days differ, both are retained with a timezone-unknown note. Observation dates in Excel use Asia/Dhaka, 6 November 2026.
- Four records were excluded because likes were hidden/non-numeric: IG_Daf_0azRrvg, IG_DRiFMt2CY9t, IG_DbwGGD4OQC2, IG_DZnRg-ooYdy. Their suspect extracted value of 3 likes was not accepted.
- IG_DZQHtuLMtaQ was excluded as a general trophy-tour recap without a clear product/offer call to action.
- Likes for IG_DbcBLbJt75i were 834 in the current UI, versus 835 in the earlier extract. Both observations are preserved in provenance.
- Contest engagement and solicited shopping-link comments are flagged in notes. Paid delivery and targeting country remain unknown. Related creatives should be grouped for train/test splitting.

## Workbook preservation and readback

All 616 previous records and their cell styles, dimensions, freeze panes and validations were preserved. The existing IncludedAds table stopped at row596 and omitted 21 existing records; its range and filter now cover **A1:AW646**. No extra worksheet was added.

A [616-record backup](https://docs.google.com/spreadsheets/d/1qQKfG4juo3ekblN6_ja1dWgAGAbA3LOr/edit?usp=drivesdk&ouid=111122819832787064775&rtpof=true&sd=true) was saved before replacement. Downloading the updated master from Drive reproduced the exported SHA256 **e6e770395d1c928334e3d417e9765b36d8b7db61b33b0fd2de336998a6347b6c** (302836 bytes), and verified 645 unique IDs, 49 columns, one Ads tab and all 29 new records.

[Full audit](https://drive.google.com/file/d/1qV-ioRQOsh7_clsvFCCIJn0mTHlr8VCM/view?usp=drivesdk) contains original source extracts, current UI measurements/timestamps, exclusions, media checks, upload receipts and workbook verification. Source collection was already run through GitHub in runs 42081829513 and 42084897765, followed by integrity run 42086652672. This update completes their pending review/import; it does not represent a new scrape.

The 645 total includes older records whose existing verification statuses remain unchanged. It should not be described as 645 independently UI-verified ads.
