# Batch 33: ASUS promotional Facebook videos

Added 23 distinct ASUS promotional posts to the existing Drive master. The master now contains 748 data records, with the new records at rows 727–749 of the same `Ads` tab (49 columns). The previous 725 records, including their verification statuses, remain unchanged. This is not a claim that all older records were newly verified.

## Collection and review

- [GitHub collection run 42227918913](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/42227918913) succeeded for 30 public original Facebook posts using the existing collector, sequential requests and a fixed five-second interval. No account login or access-control bypass was used.
- Artifact `13507221058`, `public-promotions-20261106-batch33`, was 103,457,159 bytes. Archive integrity and SHA256 matched `6bb4ba874267210e024d050e2c3b3b0fd6ea09654685601945a09e3336050987`.
- Extraction ran on 2026-11-06 from 13:44:31.576859 to 13:48:33.694851 UTC. Original-platform UI review occurred during the same period. Individual timestamps are retained in the audit and notes. Collection calendar dates use Asia/Dhaka.
- The verified ASUS page displayed `25M` followers, observed at 2026-11-06T13:48:44.331Z. This rounded current publisher audience is not ad reach or a historical audience count.
- Accepted posts were published from 2026-10-12 through 2026-11-04, using the platform UTC timestamp. The exact calendar date was not separately displayed in the Reel UI. All accepted captions are English.
- All 23 accepted posts have independently visible numeric total reactions, comments and shares. Video views are original-platform extractor measurements, not separately verified Reel UI observations. One view count is unrounded; 22 retain rounded display labels. Rounded counts never become fabricated exact values. Separate likes, reaction breakdown, saves and reposts remain blank where unavailable. Unknown country and paid delivery remain unknown.
- All 30 downloaded original MP4s passed file checksum, positive duration, video-stream and complete decode checks. Preview frames at 15%, 55% and 85% were inspected for promotional relevance. The 23 accepted complete videos total approximately 11.8 minutes; no segments or preview frames were added as dataset media.

## Exclusions and source qualifications

Six posts had a comment button without a numeric comment count: `FB_3669667533189516`, `FB_1679415043574031`, `FB_1476528694386361`, `FB_1659000029008182`, `FB_1109750168467484` and `FB_1992117514796427`. These were excluded; missing comments were not interpreted as zero.

`FB_1389911800876312` repeated the creative retained as `FB_1740881426981209`. File hashes differed because of encoding differences, but both had the same caption, 20.137375-second duration, resolution and frame rate. Six paired frames were identical or nearly identical; normalized mono 16 kHz audio was identical (SHA256 `3a0b3094e5f7330db8ef354409a2d870aea2121e9b0e8ab3e5979f215d75550f`). The repeat was excluded. No excluded media were uploaded into the final media folder.

Related Zenbook, ProArt and ExpertBook edits are identified in notes for later grouped model evaluation. Distinct product creatives can share footage. Giveaways are identified as incentivized-engagement promotions. Product specifications, performance, software features, pricing and giveaway values remain advertiser claims. In `FB_2508845936270971`, the original caption states 12.9 mm/99.9 Wh while the inspected P14 panel states 13.9 mm/90 Wh; both source forms and their discrepancy are preserved without claiming validated specifications.

## Drive update and verification

- [Same master workbook](https://docs.google.com/spreadsheets/d/1vzXBlvO-ckqJ6U9-ypNA-cSy3yK4BV-s/edit): 748 unique ad IDs, one `Ads` tab, table/filter `A1:AW749`, 349,519 bytes.
- Master SHA256: `54ecfcf313a7c756861f360c849ba2df20b27bed1a84335d43cbb02a592fe580`. Raw download after replacement matched exactly, with the expected record count and schema.
- Old cell values/styles, row heights, column widths, freeze panes and validations were preserved and checked. The 23 new rows matched the accepted manifest.
- [Existing media folder](https://drive.google.com/drive/folders/1QW4f9iy-tTbGaTUHSG-iYnJxEJXHrC6f): each of the 23 matching `FB_<id>.mp4` files exists exactly once and has the expected byte size. The folder contains 775 files in total, including earlier media.
- [725-record pre-update backup](https://docs.google.com/spreadsheets/d/1PYdUNBGSgVgsFvgvdsJeabaUharhK3xq/edit) was created before replacing the master. The original master modification time and size were rechecked to avoid overwriting unseen updates.
- [Detailed verification audit](https://drive.google.com/file/d/1gP3IpAny-xZ3k8I2hX6cg9d_Cv5566ut/view) includes source observations, exclusions, media checks, upload receipts, workbook checks and readback results.

The accepted manifest is `batches/batch33_20261106_accepted.json`. Raw candidates remain collection evidence, not additional accepted dataset records.
