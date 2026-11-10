# EXP-045 Irritated Side-eye: approved review backup

The user approved this exact review video after being told that the rig cannot pull one mouth corner downward. See `APPROVAL_STATUS.json`. This review-only branch starts at approved36 commit `3ce98774282ad6c20dfbd7018d20838ff861b762`; it changes no production registry or main branch. The repository's historical `unapproved/` storage category does not override current approval.

`Irritated_side_eye_review_v1.mp4`: 194,868 bytes, SHA-256 `e323bd40288f1907033a94ad7a24418ecd9ace7e8e39dd2da609e2d61357bae7`. H.264/yuv420p, 968 × 800, 121 frames at 30 fps, 4.033333 seconds. Exact candidate: `historical/EXP-045.json`, SHA-256 `53f59fc53968bc626e0f3ead5e9f66f03e24d06c1a900106e442cc04dc28180d`.

## Retained review and limitations

The author validator passed 84 checks. The independent handoff records a passing machine gate, all 121 decoded frames, 54 reviewer tests and 120 aggregate tests. Primary operator report: `historical/review_evidence/native_capture_playback_report.json`. Independent handoff: `historical/independent_review_evidence/independent_review_handoff.json`. Independent source review and both full validator implementations are retained unchanged.

Both irises shift screen-right beneath narrowed lids and unequal brows, then return to exact neutral. The independent downturned mouth corner is unavailable and omitted: every mouth control stays exactly neutral and sealed. No upward sneer or symmetric purse replaces it. This is a supported approximation, not full source fidelity. Frozen lash/hair edge artifacts remain. The operator sampled ordinary-speed playback and observed the end; continuous uninterrupted observation and a formal perceptual A/B comparison are not claimed. The independent reviewer did not observe normal-speed playback.

The Godot editor temporarily reordered a configuration section without changing settings. The original mismatch observation, failed reviewer test, partial capture record, both project configurations, restoration receipt and final passes are preserved. Original freeze SHA-256 remains `7f9e1bd006a91ff30d66b6da8231b4cb86e4b0bdd72162d9bc794401e51cc5ae`. Earlier UNAPPROVED/pending statements are historical evidence, not rewritten or presented as current approval status.

## Compact preservation

`SOURCE_MAP.json` maps all retained originals to exact bytes. Identical inputs are stored once and restored through aliases. `FILES.json` inventories the package except itself. Redundant test runs, raw PNG sequences, contact sheets, caches and a full baseline copy are excluded; `OMITTED_ARTIFACTS.json` describes the omissions. Source sheet, catalogue and nine reference-panel identities are retained and checked by the bootstrap against the fixed baseline.

Original checksum receipts mention intentionally omitted diagnostic PNGs. Lossy video cannot reconstruct their original RGBA bytes. Repeating the complete historical frame-to-video audit requires the original captures and layout; this compact package alone cannot do so. Any new native capture requires separately authorized native execution and new provenance.

## Offline baseline bootstrap

From a fresh package and a local Git clone already containing the fixed commit and all required blobs:

    python prepare_baseline.py --git /path/to/ryoko-vtuber --output /new/empty/path

Alternatively provide exact local source directories:

    python prepare_baseline.py --rig-source /path/to/ryoko_object_rig --reference-source /path/to/reference_library --output /new/empty/path

Output must not exist. Network fetching is disabled. The bootstrap validates 999 source files, 184 PNGs, the additional manifest, catalogue, sheet and nine reference panels. It reconstructs all 38 frozen author inputs without changing either validator contract. An immutable `snapshot/` is separate from path-relocated `reproduction/irritated_side_eye_work`.

For a new local headless numerical replay with installed Godot 4.6.3, Python, Pillow and NumPy:

    cd /new/empty/path/reproduction/irritated_side_eye_work
    godot --headless --editor --path rig --import
    sh run_motion.sh --state
    python independent_geometry.py
    python -m unittest test_independent_geometry test_encode_preview -v

The tested replay passed 1,582 static, 12,701 motion and 9,990 independent geometry checks plus 39 geometry/encoder tests. A fresh test run against the original work directory passed all 120 Python tests. No native renderer/UI was run for this backup. The bootstrap itself only verifies and copies files: no software installation, CI, remote execution, publication or checkout changes. The historical approved41 comparison remains historical evidence, not a fresh integration pass. Original full validators and tests remain in `snapshot/` for audit; no freeze is repinned to make relocated evidence appear historical.
