# Batch 34: LinkedIn and X promotions, plus media organization

Added eight reviewed public promotional posts: two Samsung Mobile LinkedIn image posts and six X videos from Samsung Mobile, Nintendo of America and PlayStation. The same Drive master now contains 756 records, with the new entries in rows 750–757 of the existing `Ads` tab. The 49-column schema remains unchanged. Older verification statuses, including any provisional entries, were preserved; this batch did not newly verify every historical ad.

## Collection and source verification

[Collection run 42232219457](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/42232219457) processed nine explicitly curated original-platform links. Eight yielded complete media. Nintendo post `2110355190935151081` did not yield exactly one usable complete video and was excluded. A successful workflow does not mean every candidate was accepted.

Artifact `13510691336`, `public-promotions-20261106-batch34`, was 109,747,939 bytes. ZIP integrity passed and the archive SHA256 matched `401e0ebb16d6f6925ae6078596f644839120bb3035085120671eff878b269a5a`. Extraction ran from 2026-11-06T14:15:09.290004+00:00 through 14:15:55.568483+00:00. Requests were sequential with a fixed five-second gap. No login, cookies, proxies or access-control workarounds were used.

Original X UI counters were checked at 14:20:50–14:20:55 UTC and LinkedIn counters at 14:21:23–14:21:24 UTC on 2026-11-06. Exact individual timestamps are retained in the master notes and audit. Collection calendar dates use Asia/Dhaka.

The six X posts have unrounded public accessibility counters for likes, replies, reposts, bookmarks and post views. Replies map to `comments`, bookmarks to `saves`, and the original displayed repost counter to `reposts`. Post views are not confirmed video plays or unique users. UI counts and extractor measurements are kept as separate observations; they are not combined. Shares and total reactions remain blank where unavailable. Rounded profile followers are preserved as display text: Samsung Mobile 10.7M, Nintendo of America 15.7M and PlayStation 44.4M, observed on the original verified profiles on 2026-11-06.

The two LinkedIn posts show total reactions/comments of 50/5 and 44/11. Samsung Mobile displayed 654,749 followers. Total reactions are not separate likes. Unavailable numeric reposts, shares, saves and views remain blank. These are organic B2B product/content-marketing promotions with a blog call to action and Galaxy/Knox context. Downloaded images belong to the original publisher posts, not comments. Original JSON-LD articleBody text was retained rather than LinkedIn's AI-generated page heading.

Publication dates span 2026-09-22 through 2026-11-05 and come from original-platform metadata: LinkedIn JSON-LD `datePublished` and X extractor timestamps in UTC. The guest LinkedIn UI showed only relative dates. X's local date/time labels are retained separately; the two early-morning November 5 UI labels correspond to November 4 UTC dates. The post status ID defines each X ad ID; an extractor metadata ID may instead refer to an attached video.

All eight media checksums matched. Both complete JPEG renditions decoded and were visually inspected. All six original MP4s passed duration/video-stream checks, complete decode and sampled preview review. Short native videos were kept whole; no video was segmented and no preview frames were uploaded as ads. No accepted source ID or media hash duplicated an existing master entry. Product, release and performance statements remain advertiser claims. Related advertiser/product/campaign creatives should be grouped during later model evaluation. The Samsung X post displayed a Made with AI label, which is recorded in notes.

## Media folder organization

The existing [Media folder](https://drive.google.com/drive/folders/1QW4f9iy-tTbGaTUHSG-iYnJxEJXHrC6f) now contains only two sections:

- [Videos](https://drive.google.com/drive/folders/1_hn7vQgercWWNfs3j1JVJWk7XM9GdL8O): 710 complete MP4 files.
- [Images](https://drive.google.com/drive/folders/1yHwLpNE5JB5XnHbU-MFdWY2o2iNq3cLG): 73 JPEG files.

All 775 existing media files were moved by MIME type, preserving their IDs, filenames, byte sizes and individual sharing settings. Eight new files were uploaded into the appropriate section. Folder listings verified all 783 files exactly once. There is no standalone audio in the collected assets, so no empty Audio folder was created. Sound remains inside the original videos; no audio extraction was performed.

All 748 old master `media_path` cells were updated to the new `media/Videos/...` or `media/Images/...` paths, including multi-asset cells. Every one of the 783 resulting asset references matches a file in its expected Drive section. File counts exceed ad counts because some older ads have more than one asset.

## Master update and checks

The [same Master_Ads.xlsx](https://docs.google.com/spreadsheets/d/1vzXBlvO-ckqJ6U9-ypNA-cSy3yK4BV-s/edit) contains 756 unique ad IDs, one `Ads` tab and table/filter `A1:AW757`. It is 354,817 bytes with SHA256 `ad07c37b25f54d4a3b2e62d7e6da7c75977b8561a0228f55d842c2d113c839a8`. A raw Drive download after replacement matched exactly. New rows matched the accepted manifest. Old values outside `media_path`, cell styles, dimensions, freeze panes and validations were preserved and checked; the formula-error scan returned no matches.

A 748-record pre-update backup was created as Drive file `1qAFJPCyKVn_zB0XcTP5emr_VThzgYBZf` after rechecking the master modification time and size. The [detailed audit](https://drive.google.com/file/d/1spIGYyv6n9SZVZlN6Atqbi8RFxtBdM1r/view?usp=drivesdk) retains source observations, raw candidate metadata, the exclusion, complete-media checks, upload/move receipts, old/new path mapping, final folder inventory and workbook readback checks.

The accepted records are in `batches/batch34_20261106_accepted.json`. GitHub artifacts are candidate evidence; the reviewed Drive master remains the authoritative combined dataset.
