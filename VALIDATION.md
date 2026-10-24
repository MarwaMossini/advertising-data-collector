# Validation status, 2026-10-23

Five local tests passed: missing vs zero engagement, uploader mismatch, multi-video exclusion, missing date exclusion, and allowed URL hosts.

A live Facebook test attempted the previously collected Bepanthen video 853469779607288 without credentials. It failed with `CERTIFICATE_VERIFY_FAILED: self-signed certificate in certificate chain`. No certificate check was disabled. The run correctly saved zero candidates and recorded the error.

The current collector's complete live download path, YouTube discovery, cross-run artifact restoration, and GitHub scheduling have not been verified in a GitHub runner. A successful manual run is required before treating this project as operational. Earlier media downloads in this conversation used a separate collection process and are not evidence that this new workflow has passed its live test.
