# EXP-161 Sleepy: approved review backup

The user approved this exact review video after being told that its mouth is narrower and toothier than the reference. See `APPROVAL_STATUS.json`. This branch is only a review backup based on approved36 commit `3ce98774282ad6c20dfbd7018d20838ff861b762`; it changes no production registry or main branch.

`Sleepy_review_v1.mp4`: 203,037 bytes, SHA-256 `9ee4cbb7cee2dd79549363c472dd0ff7f0234e40282951745e90f921aef38475`. H.264/yuv420p, 968 × 800, 121 frames at 30 fps, 4.033333 seconds. The exact candidate is `historical/EXP-161.json`.

## What was reviewed

Author native validator: 84/84 checks. Separate independent validator: 87/87 checks. Both fully decode all 121 video frames. All 107 Python tests passed after capture. The original operator and independent source/native reports are retained, including the temporary editor configuration rewrite, both resulting guard failures, restoration, and final passes. The independent validator's literal freeze pin and the author's separate checksum receipt remain unchanged.

The lips open into a thin tooth-visible horizontal slit, rather than the reference's softer rounded dark mouth. There is no jaw rotation or chin movement. The operator sampled normal playback; no continuous uninterrupted observation or formal native-video A/B test is claimed. Historical files keep their original UNAPPROVED/pending statements. They describe earlier stages and must not override the later approval note.

## Compact evidence and preservation

`SOURCE_MAP.json` maps every retained original to its exact bytes. Identical logs and receipts are stored once and reconstructed as aliases. `FILES.json` inventories all package files except itself. No full baseline, caches, raw frame sequences, or repeated contact sheets are copied into this backup. The original per-frame hashes, complete decode/order evidence, source-reference hashes, and original manifests are retained.

The original checksum manifests mention intentionally omitted diagnostic PNGs. These omissions are explicit in `OMITTED_ARTIFACTS.json`. The lossy MP4 cannot reconstruct the original RGBA captures. The complete historical frame-to-video validator therefore needs the original raw captures and original layout; this compact backup alone cannot repeat that pass.

## Offline baseline bootstrap

From a fresh copy of this package, with a local Git clone containing the fixed commit and all required blobs:

    python prepare_baseline.py --git /path/to/ryoko-vtuber --output /new/empty/path

The output path must not exist. Network fetching is disabled. Alternatively provide existing exact sources:

    python prepare_baseline.py --rig-source /path/to/ryoko_object_rig --reference-source /path/to/reference_library --output /new/empty/path

This verifies all 999 baseline files, 184 PNGs, the additional manifest, catalogue, sheet and nine reference panels. It reconstructs the exact historical input snapshot and checks all 47 frozen author inputs without changing either validator's pinned contract. It also prepares a distinct path-relocated replay under `reproduction/sleepy_work`, keeping the snapshot untouched.

For a new local headless numerical replay, with installed Godot 4.6.3, Python, Pillow and NumPy:

    cd /new/empty/path/reproduction/sleepy_work
    godot --headless --editor --path rig --import
    sh run_motion.sh --state
    python independent_geometry.py
    python -m unittest test_independent_geometry test_encode_preview -v

Any new native capture requires separately authorized native execution and fresh review provenance. The bootstrap does not render, open UI, install software, execute remotely, run CI, publish or alter any checkout. The historic approved39/40 comparisons are preserved, not claimed as fresh integration validation. Full original test/validator sources remain in `snapshot/` for audit; no freeze is repinned to make a relocated native audit appear historical.
