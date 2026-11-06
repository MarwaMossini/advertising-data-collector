# Batch 35: twelve reviewed X promotional posts

Added 12 original public X promotions to the same Drive master: four LEGO posts, two Xbox posts, one adidas Football post, two Nike posts, one REMATCH post and two McDonald’s posts. The master now contains 768 records, with the new entries at rows 758–769 of the existing `Ads` tab. The schema remains 49 columns. Older verification statuses, including any provisional entries, are unchanged; this batch did not newly verify all historical ads.

## Collection and verification

[GitHub run 42245698918](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/42245698918) processed 14 curated original-post URLs using sequential requests with a fixed five-second gap. Twelve yielded complete media. The two Xbox image-card candidates `2118448306095350234` and `2118139219323576338` resolved through the extractor to unsupported store URLs and were excluded. Their visible counters were not enough to qualify them without the required complete media retrieval. A successful workflow does not mean every candidate was accepted.

The source run started at 2026-11-06T15:43:46.492981+00:00 and finished at 15:45:09.777382+00:00. Original X post counters were observed from 15:37:54 through 15:40:26 UTC on 2026-11-06; individual observation timestamps are retained in the master notes and detailed audit. Publisher profiles were checked during the same session. Collection calendar dates use Asia/Dhaka. Uploading or resuming a batch does not reset its source-observation timestamps.

The four media artifacts (`13516774730`, `13518670468`, `13516824843`, `13517714420`) and metadata artifact `13518365612` passed ZIP integrity and SHA256 checks against the GitHub-reported digests. Artifacts group up to three complete creatives; no video was divided into parts. Full artifact metadata and digests are retained in the audit.

All 12 accepted posts have independently checked, unrounded original X accessibility counters for likes, replies, reposts, bookmarks and post views. Replies map to `comments`, public bookmarks to `saves`, and the original displayed repost counter to `reposts`. Post views are not confirmed video plays or unique users. Extractor measurements remain separate evidence and are not mixed with UI counts. Unavailable shares and total reactions remain blank, never zero.

Original verified publisher profiles displayed these rounded current follower labels: LEGO 1M, Xbox 26.2M, adidas Football 3.8M, Nike 9.4M, REMATCH 74.3K and McDonald’s 4.5M. The labels and their observation times are preserved; `followers_exact` remains blank. These are publisher audiences, not ad reach or historical follower counts.

Publication dates range from 2024-08-15 through 2026-11-05 and come from original-platform timestamps in UTC. Original local UI date/time labels are retained separately and can show the next calendar day. All accepted captions are English and are retained from the original UI. Counts are observation-time engagement, not engagement at publication.

## Media and editorial checks

All 10 original MP4s passed checksum, positive-duration/video-stream and complete decode checks. Sampled frames at 15%, 55% and 85% were visually reviewed for promotional relevance. The videos total approximately 7.5 minutes. Both complete McDonald’s WEBP image renditions decoded and were visually inspected at 1080 × 1350. The downloaded image format and full source rendition were retained without conversion. Preview images and extracted frames were used only internally and were not uploaded as ads.

No accepted source ID or media SHA256 duplicated an existing master entry or another accepted item. The two LEGO Nightmare Before Christmas videos are different creatives: a 56.32-second product demonstration and a 43.072-second animated presentation. The two McDonald’s images also differ and represent related teaser/launch creatives. Their campaign families are noted for later grouped model evaluation. The original Nike/LEGO and REMATCH/adidas posts were retained; quote-posts of those creatives were not added separately with another publisher’s counters.

The Xbox Series X-BITE promotion is flagged as an incentivized-engagement giveaway because entry asks for follows and reposts. Its stated US/DC/PR and age restrictions are eligibility terms, not verified delivery targeting. Paid distribution and targeting country remain unknown. Product specifications, release dates, offers and performance statements remain advertiser claims. The LEGO NINJAGO trailer is identified as entertainment release promotion, and the REMATCH apparel bundle as in-game content.

## Drive update and readback

The [same Master_Ads.xlsx](https://docs.google.com/spreadsheets/d/1vzXBlvO-ckqJ6U9-ypNA-cSy3yK4BV-s/edit) contains 768 unique ad IDs, one `Ads` tab and table/filter `A1:AW769`. It is 360,906 bytes with SHA256 `d22f927c536de5e1164cd198a2a7c999d9aab2d0bea626f708b1065ca23df124`. A raw Drive download after replacement matched exactly. The 12 new rows matched the accepted manifest, while all old values, styles, dimensions, freeze panes and validations were preserved. The formula-error scan found no matches.

The [existing Media folder](https://drive.google.com/drive/folders/1QW4f9iy-tTbGaTUHSG-iYnJxEJXHrC6f) retains its type sections:

- [Videos](https://drive.google.com/drive/folders/1_hn7vQgercWWNfs3j1JVJWk7XM9GdL8O): 720 MP4 files.
- [Images](https://drive.google.com/drive/folders/1yHwLpNE5JB5XnHbU-MFdWY2o2iNq3cLG): 75 images, comprising 73 JPEGs and two WEBPs.

All 12 new filenames occur exactly once with expected byte sizes in the correct section. All 795 media references in the downloaded master match the Drive inventory. Asset counts exceed ad counts because some older records have multiple assets. There is no standalone audio collection, and sound remains inside the original videos.

A 756-record backup was created as Drive file `1BkGMmViptyVWWvL3wJdxfsL0-Kd3lEos` after confirming the master had not changed. The [detailed verification audit](https://drive.google.com/file/d/1K_Aog95mg9nQa4_ImMG69j5odX0oxTEK/view?usp=drivesdk) contains source observations, raw candidates, exclusions, artifact provenance, full-media checks, upload receipts, folder inventory, workbook checks and readback results.

Accepted records are in `batches/batch35_20261106_accepted.json`. GitHub artifacts remain candidate evidence; the reviewed Drive master is the authoritative combined dataset.
