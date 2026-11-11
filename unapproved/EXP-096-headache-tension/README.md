# EXP-096 Headache Tension: approved review backup

The user approved this exact review video after the accompanying explanation that it is a restrained tense pause because the rig cannot create central brow furrows. See `APPROVAL_STATUS.json`. This review-only branch starts at approved36 commit `3ce98774282ad6c20dfbd7018d20838ff861b762`. It changes no production registry or main branch. The repository's historical `unapproved/` storage category does not override current user approval.

`Headache_tension_review_v1.mp4`: 197,614 bytes, SHA-256 `2b410146ed28ec4d6240e3e47c6b6f27d9c33b1a8087c101941da9a6a2d58716`. H.264/yuv420p, 968 × 800, 121 frames at 30 fps, 4.033333 seconds. Exact profile: `historical/EXP-096.json`, SHA-256 `21ba5c4393ed672a5496ed28577068bd4b56e3b8ff5d7ac4f9674df03badf1fe`.

## Primary review and qualifications

Primary operator report: `historical/NATIVE_CAPTURE_REVIEW.md`. Independent reports: `historical/INDEPENDENT_SOURCE_REVIEW.md` and `historical/INDEPENDENT_NATIVE_REVIEW.md`. Final author evidence passed 84 checks and final independent evidence passed 96. Both validators completely decoded all 121 frames. Historical native capture receipts report 1,838 static and 16,745 motion checks; all 146 combined unit tests passed after exact restoration.

This is restrained tense closure followed by still-closed softening and then reopening. The mouth remains sealed. True central furrows, horizontal brow convergence and independent downturned mouth corners are unavailable. The supported brow lowering/rotation and slight lip pressure/purse do not make an unmistakable headache/pain grimace. Calm, concentration or tired irritation remain possible interpretations. Existing fine lash/hair edge artifacts remain. The operator sampled ordinary-speed Play and Loop Zone playback; continuous uninterrupted observation is not claimed. The independent reviewer inspected actual native and decoded pixels but did not operate playback.

The independent report compares actual Silent Fury and Sleepy Annoyance peaks and a verified historical Meditative Calm closed-arrival anchor. The Calm comparison is not a new current render, an all-frame comparison or normal-speed playback. Its historical receipt did not include a capture-time profile-hash field. Exact comparator PNG/RGBA hashes, the verified current source-profile identity and limitations remain in `historical/independent_native_review_evidence/meditative_comparator_verification.json`. Small original harness and receipt files are retained under `comparator_support/`, mapped by `COMPARATOR_SUPPORT.json`; comparator PNGs are omitted.

## Preserve failures and history

The native editor reordered the `[editor]` section before `[rendering]` without changing values. The original and rewritten project configurations, exact diff, failed freeze guard, failed author guard, seven intermediate unit-test failures, restoration receipts and final passing results remain unchanged under `historical/native_session_evidence/`. Identical records may be stored once through `SOURCE_MAP.json` aliases. No historical failure or status label is rewritten.

The 38-file author freeze remains SHA-256 `6f076e4127e9c07d4083c6a26560ce32dfcb25a9d9c7981ad0401d291a509520`. Earlier UNAPPROVED/pending statements are historical checkpoints. Only the separate current approval record supersedes their approval status; it does not upgrade technical or visual claims.

## Compact preservation

`SOURCE_MAP.json` maps 82 exact original files to 68 unique stored files and reconstructs 14 byte-identical aliases. `FILES.json` inventories the package except itself. Raw PNG sequences, contact sheets, caches, full baseline copies and redundant passing test logs are excluded. Failed intermediate and definitive restored test evidence are retained. `OMITTED_ARTIFACTS.json` records these limits.

Historical checksum receipts refer to deliberately omitted diagnostic images. A lossy MP4 cannot restore their original RGBA bytes. Repeating complete historical frame-to-video validation requires original native captures and layout; this package alone cannot do so. Any new native capture requires separate authorization and fresh provenance. Full source sheet, catalogue and nine panel identities are preserved and checked against the fixed baseline by the bootstrap.

## Offline baseline bootstrap

With a local Git clone already containing the fixed commit and all required blobs:

    python prepare_baseline.py --git /path/to/ryoko-vtuber --output /new/empty/path

Or provide exact local source directories:

    python prepare_baseline.py --rig-source /path/to/ryoko_object_rig --reference-source /path/to/reference_library --output /new/empty/path

Output must not exist. Network fetching is disabled. The bootstrap validates 999 baseline files, 184 PNGs, the extra source manifest, catalogue, sheet and nine reference panels. It reconstructs all 38 frozen author inputs and preserves both original validator contracts. An immutable `snapshot/` is separate from path-relocated `reproduction/headache_tension_work`.

For a local headless numerical replay with installed Godot 4.6.3, Python, Pillow and NumPy:

    cd /new/empty/path/reproduction/headache_tension_work
    godot --headless --editor --path rig --import
    sh run_motion.sh --state
    python independent_geometry.py
    python -m unittest test_independent_geometry test_encode_preview -v

The tested reconstruction passed 1,806 static, 16,260 motion and 10,338 independent geometry checks, plus 46 portable geometry/encoder tests. A fresh test run against the untouched original work directory passed all 146 Python tests. The Git extraction route is implemented but not exercised here; the exact-source-directory route was tested. Historical approved41 parity remains historical evidence, not a new production integration pass. Full validators/tests remain in `snapshot/` for audit, without repinning the freeze to make relocated evidence appear historical.

No native renderer/UI, CI, remote-machine execution, paid resource, production integration or main write was used for this backup. Bootstrap only verifies and copies local inputs; it performs no installation, checkout modification or publication.
