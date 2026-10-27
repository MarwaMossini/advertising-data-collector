# Validation status, 27 October 2026

GitHub Actions run https://github.com/MarwaMossini/advertising-data-collector/actions/runs/40486589264 completed successfully using the bundled video decoder. It processed a curated queue of 47 original-platform URLs: 38 records with media were retained and nine attempts failed. The total includes earlier master records being rechecked; it is not a count of new thesis samples.

The unified master was updated separately after deduplication: nine newly discovered promotional posts and one earlier GitHub collector record were added, taking it from 54 to 64 media-backed posts. The ten additions have dates, decoded video streams and inspected previews. The full original videos were preserved. Native UI engagement was not independently rechecked.

Publication dates now prefer platform timestamps, then platform date fields, then a documented prior collection date. Missing dates are not guessed. The unified master retains three older unknown dates and flags two older source-date differences rather than silently replacing them.

Eleven local unit tests pass, covering URL hosts, missing versus zero counts, migration, date recovery, invalid dates, date provenance, conflicting views, distinct shares/reposts, and platform-title display parsing. The last display-parsing enhancement was locally tested after the successful end-to-end run; it has not had a separate full GitHub collection run.

Unsupported posts, galleries, unavailable dates, and failed media downloads remain exclusions or failures. Extracted metadata and returned title counters are source-labelled candidate observations, not independently verified UI counts. A successful workflow does not mean all queued URLs succeeded or that all metrics were available.

The GitHub output remains a temporary artifact with 90-day retention. There is no daily schedule, automatic Excel writeback or Google Drive integration. Those have not been claimed as operational.
