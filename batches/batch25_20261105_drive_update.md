# Batch 25: archival promotional-video recovery, 2026-11-05 (Bangladesh)

**Completed:** eight original full MP4s recovered, checked, uploaded, and appended to the same Drive master. The existing 595 ads were preserved, making **603 rows of ads, 49 columns, one `Ads` tab**. Each ID is unique. No new observation was made at the time of this recovery.

## New rows

| Native post ID (Excel ad_id) | Publisher | Published date (platform UTC metadata) | Last metrics observation (Asia/Dhaka) | Views display | Total reactions display (not likes) | Original post |
| --- | --- | --- | --- | --- | --- | --- |
| `FB_1296950852422686` | PUMA | 2026-06-17 | 2026-11-02 | 129K | 257 | https://www.facebook.com/PUMA/videos/1296950852422686/ |
| `FB_1036260941889124` | PUMA | 2025-03-21 | 2026-11-02 | 209K | 348 | https://www.facebook.com/PUMA/videos/1036260941889124/ |
| `FB_755791296094617` | PUMA | 2023-04-06 | 2026-11-02 | 25K | 493 | https://www.facebook.com/PUMA/videos/755791296094617/ |
| `FB_153363310155861` | PUMA | 2021-08-03 | 2026-11-02 | 34K | 692 | https://www.facebook.com/PUMA/videos/153363310155861/ |
| `FB_2013912125954380` | Sony Electronics | 2026-10-01 | 2026-11-02 | 5.6K | 50 | https://www.facebook.com/SonyElectronics/videos/2013912125954380/ |
| `FB_28157849083885335` | Sony Electronics | 2026-09-16 | 2026-11-02 | 10K | 48 | https://www.facebook.com/SonyElectronics/videos/28157849083885335/ |
| `FB_1026015493817647` | Emirates | 2026-09-09 | 2026-11-01 | 223K | 5K | https://www.facebook.com/Emirates/videos/1026015493817647/ |
| `FB_2351638912310802` | Emirates | 2026-08-18 | 2026-11-01 | 201K | 5.2K | https://www.facebook.com/Emirates/videos/2351638912310802/ |

## Verification and provenance

- Candidate source archives: GitHub run [41460004517](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/41460004517) (PUMA, original observation 2 Nov), [41486060782](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/41486060782) (Sony, original observation 2 Nov), and [41230585697](https://github.com/MarwaMossini/advertising-data-collector/actions/runs/41230585697) (Emirates, original observation Oct 31 UTC / Nov 1 Bangladesh).
- All eight MP4s were extracted from original GitHub artifacts, SHA-256 verified against `ads.csv`, checked against existing 595 master ad IDs and SHA-256 values, verified with ffprobe, and **fully decoded using ffmpeg**. Media size total: 54,119,025 bytes.
- The new media were uploaded as individual complete `media/FB_<native_post_id>.mp4` files to the original Drive folder [media](https://drive.google.com/drive/folders/1QW4f9iy-tTbGaTUHSG-iYnJxEJXHrC6f); all eight filenames, file sizes, and folder parent IDs were checked after upload. No frames or segmented clips substituted for the full videos.
- Existing master [Master_Ads.xlsx](https://docs.google.com/spreadsheets/d/1vzXBlvO-ckqJ6U9-ypNA-cSy3yK4BV-s/edit) was modified in place, retaining file ID and 49-column schema. Readback showed 603 ads and 603 distinct ad IDs, with rows 597–604 containing this batch. A local before/after comparison confirmed that earlier 595 rows' values were unchanged.
- A separate prior-master backup [595-ad master](https://docs.google.com/spreadsheets/d/1TXzuJdqcRZWL7xIO07AFhF-j1ZhMWiK1/edit) was created in the existing Drive `backup` folder. The [verification manifest](https://drive.google.com/file/d/1xzdqB5wmGV0hTpVzBcYtsNAnpeUBL7oW/view) lists source URLs, source timestamps, checksums, video lengths, and media filenames.
- Displayed labels `129K`, `5.6K`, `223K`, etc. remain rounded *display* values, with view exact-value fields blank. Only clearly integer reaction displays are retained as `reactions_exact`. The rounded Emirates reaction labels `5K` and `5.2K` do not become exact numbers.
- Facebook reactions are **not** treated as likes. Comments, shares, follower counts, reaction breakdowns, saves and reposts were unavailable in these archived extracts and remain blank. Publication calendar dates come from platform UTC timestamps, not a separately checked UI date.
- **Verification status is provisional** on all eight rows. The archived source data, original post URLs, and full media were checked, but the original Facebook UI engagement counts were not independently re-observed. This distinction is preserved in `verification_status` and `notes`.
- Paid-ad delivery and targeting location remain unknown. Content qualifies as brand promotional material, not proven paid placement. Group related campaigns/creatives when splitting the machine-learning dataset to avoid leakage.

The 19 unused archival MP4 candidates were screened, but incidental recipes, ordinary BTS posts, sponsorship celebrations without a clear promotional argument, and sources with only one engagement metric were not automatically added. 
