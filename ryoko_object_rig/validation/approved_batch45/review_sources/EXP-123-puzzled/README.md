# EXP-123 Puzzled: unapproved delivered-preview backup

**Status: UNAPPROVED.** This package preserves the exact delivered preview for the user's review. It does not approve or register EXP-123, modify production, or write main. The backup branch is `review/exp123-puzzled-v1`; production integration requires a later approval.

## Exact artifact and evidence

`Puzzled_review_v1.mp4` is H.264/yuv420p, 968 × 800, 30 fps, 121 frames, 182,736 bytes and 4.033333 seconds. Its SHA-256 is `5df48deb24bc3a86084799084fd65a004bd7b4af4459ed1eea6d838225930db3`. The profile SHA-256 is `a0ebc834b361cee3352b9687de768895c4c6182cc90c343ebff0851c6037661e`. The source performance spans exactly four seconds; the final endpoint is included as a video frame.

The frozen approved36 baseline is commit `3ce98774282ad6c20dfbd7018d20838ff861b762`. All 999 pinned files including 184 PNGs remain unchanged. The production registry stays at 36 entries with Puzzled absent. Three additional profile snapshots are comparison inputs only, not an approved39 integration.

The package includes exact profile, plan, probes, encoder and tests; source catalogue/reference records; independent source and native reviews; final operator review and receipts; complete static and motion receipts; native PNG/RGBA hashes and decoded ordering evidence. Historical pending/no-publication statements describe the stage in which those records were made. They are deliberately not rewritten as current evidence.

Original headless numerical checks passed 1,494 static and 8,902 motion assertions. Native capture passed 1,526 static and 9,387 motion checks. The independent native/media validator passed 73 checks, and its independent operator rerun also passed. These checks do not constitute artistic approval.

`review_evidence/launcher_import_audit/` preserves the config-only failed validation, exact editor-rewritten project bytes, diff, and exact restoration proof. Godot reordered sections/whitespace without changing settings. The original frozen bytes were restored after editor exit, followed by a full passing check. No frozen input or validation threshold was silently relaxed. The early authoring blink-side failure and its correction are retained separately under `development_audit/`.

## Source fit and playback limits

The candidate uses a one-sided questioning brow, uneven squint, and compact sealed pout. The source's sideways diagonal mouth is only weakly approximated: endpoint-midpoint bias is two source pixels, about 0.98 bust pixels. There is no whole-mouth translation or diagonal contour. The rigid brow does not reproduce painted local curvature, and head tilt is omitted. At bust scale the result reads as restrained puzzled/skeptical; the mouth asymmetry is less obvious than the reference. Numeric differences against 39 profiles do not prove perceptual distinctness.

Supported Kdenlive playback was invoked and intermittently sampled while the playhead advanced through the pose and neutral endpoint. Continuous normal-speed observation, complete pacing review and smooth real-time engine pacing remain unverified. Body gestures, speech/lip-sync and export remain outside this review.

## Portable numerical reproduction

Keep the published evidence immutable. Make a separate fresh copy, and use an existing local Git checkout containing the exact baseline commit. No network fetch is performed:

1. `python3 prepare_baseline.py /path/to/local/checkout`
2. `python3 prepare_native_launcher.py`
3. Import `rig` and `native_launcher` headlessly with Godot 4.6.3, using a local HOME/XDG directory as in `run_motion.sh`.
4. `sh run_motion.sh --state`
5. Run headless `--check-only` for `native_launcher/static.gd`, `motion.gd` and `launcher.gd`, saving the output as `launcher_static_parse.log`, `launcher_motion_parse.log`, and `launcher_launcher_parse.log` in the reproduction root.
6. `python3 verify_reproduction.py`
7. `python3 run_portable_tests.py`

The bootstrap reads Git objects at the pinned commit, disables Git network protocols and lazy fetch, exports the rig plus the exact catalogue and all nine source panels, verifies hashes and the 36-entry registry, then creates a relocated BASELINE_FREEZE.json. It never uses the checkout's mutable working tree. `verify_reproduction.py` preserves the original numerical/source checks and only relocates the three comparison inputs and its output receipts. The original `verify_preparation.py` is archived unchanged.

All 29 historical unit tests pass in the original workspace. The unchanged historical suite initially passed 26/29 after relocation; three fixture tests require historical paths/freeze identity. That failed run is preserved under `package_tests/`. `run_portable_tests.py` adapts only the synthetic fixture builder to relocated inputs and pins each new fixture hash. It runs all 29 original assertions successfully, including the negative test that deliberately breaks the fixture freeze. This test-only adapter cannot authorize or validate a new real native capture.

The original `review_input_freeze.json` and `review_validation.py` remain exact historical evidence. The validator deliberately pins the historical freeze identity and is **not a portable validator for newly relocated native captures**. Do not overwrite that freeze, patch its expected identity, or treat old native receipts as new reproduction evidence. A fresh native capture would require its own separately frozen review and validation. This package validates portable numerical reconstruction only; it does not claim a new native render.

Requires Godot 4.6.3, Python with Pillow and NumPy, and ffmpeg/ffprobe with libx264. The encoder also uses the documented DejaVu Sans font path. It refuses existing MP4 output or incomplete/incorrect native receipts. Raw capture PNG sequences, contact sheets, duplicate baseline files and caches are omitted to keep the backup compact; their hashes and the exact MP4 are retained. The full reference art is available at the pinned baseline commit.

No CI, new UI use, paid resources, hardware flashing or remote-machine execution is part of this backup. Source, profile, video, frozen probes and historical receipts remain unchanged.
