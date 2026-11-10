# EXP-081 Mild Disgust: approved exact-review backup

The user approved this exact version with “good,” after saying “if i say its good its approved” and after the skeptical-smirk/upper-lip limitation was disclosed. `APPROVAL_STATUS.json` records that subsequent approval. The original profile, reports and receipts retain their review-time **UNAPPROVED** and pending language unchanged. Those historical statements do not supersede the later approval.

This branch is `review/exp081-mild-disgust-v1`. It archives the reviewed candidate only. It does not change main, the production rig or the 36-entry baseline registry. Production integration is separate.

## Exact version and verified evidence

- Video: `Mild_disgust_review_v1.mp4`, 188,969 bytes, H.264/yuv420p, 968 × 800, 30 fps, 121 frames, 4.033333 seconds. SHA-256: `71bf7075205155776165e147b06ae5ada1c1158f2a0401dcc8be94d39babbc6f`.
- Profile SHA-256: `4a6783b9232217ed468f626dc36e5c4c43dc0a5a284108a210ef1975496e1dd9`.
- Approved36 baseline: `3ce98774282ad6c20dfbd7018d20838ff861b762`. All 999 pinned files, including 184 PNGs, and the extra manifest remain exact. The candidate is absent from that baseline's 36-profile registry.
- Headless checks: 1,526 static, 11,330 motion, including 36 interruption/lifecycle assertions, and 8,421 independent Python geometry/timeline assertions. All nine reference panels are exact lossless crops.
- Native evidence: 1,558 static and 11,815 motion checks; 16 static and 242 motion PNGs; complete per-frame pixel hashes and MP4 decoding/order evidence. Independent technical review passed **79/79**, and a publication-time read-only rerun also passed 79/79.
- Operator's final report: `native_capture_audit/CAPTURE_PLAYBACK_REPORT.json`. Independent source/native reports, probes, encoder, reference catalogue/observations, tests, original frozen inputs, and preparation/development audit evidence are included.

Godot's editor rewrote only section order/spacing in the launcher config. Both exact versions, the before-restoration failed freeze guard, after-restoration pass, a diff, and an independently recomputed settings/restoration receipt are preserved. After editor exit, the exact original config bytes were restored. No frozen input or validation threshold was relaxed.

## Artistic and playback limitations

The peak reads as a restrained smirk or skeptical objection rather than convincing upper-lip disgust. The corner control moves both upper and lower lip contours together. It does not create independent upper-lip curl/lift, nose wrinkle, head recoil or new anatomy. The user approved with this limitation disclosed. Technical checks and numerical differences from 41 profiles do not establish source faithfulness or perceptual distinctness.

Kdenlive normal-speed playback was initiated and sampled as the playhead advanced. Continuous observation and complete real-time pacing review were not established. Body gestures, speech and lip-sync are outside this facial review.

## Verify and reproduce locally

First verify the untouched archive with `python3 verify_package.py`. Keep it immutable; use a **separate fresh copy** for reproduction. Requires Godot 4.6.3, Python with Pillow/NumPy, and ffmpeg/ffprobe with libx264.

1. `python3 prepare_baseline.py /path/to/local/git/checkout`
2. `python3 prepare_native_launcher.py`
3. Import `rig` and `native_launcher` headlessly with Godot, using an isolated local HOME/XDG directory as in `run_motion.sh`.
4. `sh run_motion.sh --state`
5. Run Godot headless `--check-only` for `native_launcher/static.gd`, `motion.gd`, and `launcher.gd`; save logs as `launcher_static_parse.log`, `launcher_motion_parse.log`, and `launcher_launcher_parse.log`.
6. `python3 verify_reproduction.py`
7. `python3 independent_geometry.py`
8. `python3 run_portable_tests.py`

The bootstrap reads Git objects only, disables network protocols and lazy fetching, and never uses a checkout's mutable working tree. The local object store must already contain approved36 and approved39 commit `419450d2302d471aa009557289ad509ffb413349` plus their required trees/blobs. It exports the approved36 rig, exact catalogue and nine-panel source; it separately checks 993 common runtime/artwork files from approved39. It does not import that later registry. Five isolated profile snapshots serve only as numerical comparison inputs.

`verify_reproduction.py` differs from the historical verifier only in comparison paths and output receipt names. The original verifier is retained. `run_portable_tests.py` runs all 63 original assertions, adapting only isolated synthetic fixture construction to relocated inputs and that fixture's new hash. The negative frozen-identity test still must fail correctly. No real capture is relabeled or approved by that adapter.

Original `review_input_freeze.json`, `REVIEW_FREEZE.sha256` and `review_validation.py` are historical evidence. Original baseline/README and five launcher inputs are under `historical_inputs/`, with a complete exact-source provenance map. The validator deliberately pins the original freeze identity: it is **not a validator for newly relocated native captures**. Never rewrite its expected identity or treat old receipts as new native evidence. A fresh capture needs its own separately frozen review. This package claims portable numerical reconstruction, not a new render or video.

Raw PNG sequences, contact sheets, duplicate baseline source and caches are omitted for compactness. Their hashes and exact MP4 are included; source art is recoverable at the pinned commit. No CI, new UI, paid resources, purchases, hardware flashing or remote-machine execution is part of this backup.
