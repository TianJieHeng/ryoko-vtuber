# EXP-104 Triumphant Grin: approved review backup

The user approved this exact review video after being told that the grin is more restrained than the reference and cannot reproduce its exact clenched-teeth shape. See `APPROVAL_STATUS.json`. This branch is only a review backup based on approved36 commit `3ce98774282ad6c20dfbd7018d20838ff861b762`; it changes no production registry or main branch.

`TriumphantGrin_review_v1.mp4`: 187,963 bytes, SHA-256 `caa4914959146c87fa371a17e829ca3c5d85b4db4a273b341f62781a8b33d17b`. H.264/yuv420p, 968 × 800, 121 frames at 30 fps, 4.033333 seconds. The exact candidate is `historical/EXP-104.json`.

## Review scope and limitations

The independent native/video validator passed 94/94 checks with no failures or pending checks, including complete decoding of all 121 video frames. Native static validation passed 1,614 assertions and native motion validation passed 13,131 assertions. The unchanged author encoder's capture validator and complete FFmpeg decode passed. The operator retained 105 passing combined Python tests both before and after capture. Original operator and independent source/native reviews are retained as primary evidence, not replaced by this summary.

The centered tooth-bearing grin is narrower and softer than the source's stronger triumphant expression. It uses the existing upper tooth arch, not an exact opposing-teeth clench, new dental anatomy, cheek deformation or jaw rotation. Existing hair/lash and tooth/lip styling remains visible. Historical native comparator anchors support limited distinctions; no formal full-video perceptual A/B pass is claimed.

Normal Play was initiated in Kdenlive from zero and the neutral endpoint was observed. Only that endpoint was sampled during playback. Further moving/peak playback observations were not completed, and no continuous uninterrupted viewing is claimed. Separate actual-pixel inspections and complete numerical/video checks do not replace continuous viewing. User approval is recorded independently of these technical limits.

The editor temporarily reordered `project.godot` sections without changing setting values. The original project bytes, rewritten bytes, exact diff, failed author source/freeze checks, failed independent review, restoration evidence and final passes remain under `historical/native_capture_audit/` or their byte-identical aliases in `SOURCE_MAP.json`. No validator or freeze was weakened. The independent validator's literal contract pin remains unchanged. Historical UNAPPROVED and pending labels describe earlier stages; only the separate current approval note supersedes their user-approval status.

## Compact evidence and preservation

`SOURCE_MAP.json` maps every retained original to exact bytes. Identical logs and receipts are stored once and reconstructed as aliases. `FILES.json` inventories all package files except itself. No full baseline, caches, raw frames, or contact sheets are copied into this backup. The original per-frame hashes, complete decode/order evidence, source-reference hashes, and original manifests remain.

Original checksum manifests mention deliberately omitted diagnostic PNGs. `OMITTED_ARTIFACTS.json` makes those omissions explicit. The lossy MP4 cannot recover original RGBA captures. Repeating the complete historical frame-to-video validator requires the original raw captures and original layout, not this compact backup alone.

## Offline baseline bootstrap

With a local Git clone containing the fixed commit and required blobs:

    python prepare_baseline.py --git /path/to/ryoko-vtuber --output /new/empty/path

The output must not exist and network fetching is disabled. Alternatively provide exact existing sources:

    python prepare_baseline.py --rig-source /path/to/ryoko_object_rig --reference-source /path/to/reference_library --output /new/empty/path

This verifies all 999 baseline files, 184 PNGs, the extra manifest, catalogue, sheet and nine reference panels. It reconstructs all 47 original frozen author inputs without changing the author contract or independent validator pin. A separate path-relocated replay is prepared under `reproduction/triumphant_grin_work`; the historical snapshot remains untouched.

For a new local headless numerical replay with installed Godot 4.6.3, Python, Pillow and NumPy:

    cd /new/empty/path/reproduction/triumphant_grin_work
    godot --headless --editor --path rig --import
    sh run_motion.sh --state
    python independent_geometry.py
    python -m unittest test_independent_geometry test_encode_preview -v

The bootstrap does not render, open UI, install software, execute remotely, run CI, publish, or alter a checkout. New native capture requires separate authorized native execution and fresh provenance. Historical approved40/41 parity is preserved evidence, not newly revalidated integration. Full original test and validator sources remain in `snapshot/` for audit; no freeze is repinned to make a relocated native audit appear historical.
