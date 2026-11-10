# Quiet contentment: unapproved preparation v1

EXP-003 is a **4.6-second, data-only review candidate**, prepared against the preserved approved27 rig at [commit 816d77f](https://github.com/TianJieHeng/ryoko-vtuber/commit/816d77fafb6e016dc70f0802743d444e618f7b0f). It is **not approved, registered, integrated or published**. No native static capture or movie has been rendered. The files in this directory are preparation and numerical evidence, not a visual approval.

## Reference evidence

The actual revised nine-panel sheet was visually inspected:

`avatar_build_assets/reference_library/assets/expressions/EXP-003_quiet-contentment/RYO_EXP-003_quiet-contentment_sheet_v002.png`

Its SHA-256 is `4636be0c5bf2df17302b9ea131aa498a74100a7d81062beb1c73d1f6d19e5007`, matching the catalogue. `SOURCE_REFERENCE.json` preserves the complete EXP-003 entry and hashes for all 11 source PNGs, including the lossless panel crops and peak.

The catalogue's exact facial intent is:

> Brows rest low and level; eyes half relax; lips form a barely visible symmetrical smile.

The revised source pixels add an important distinction: KP3 relaxes the upper lids, KP4 narrows the eyes to slits, and KP5–KP6 show relaxed **closed eyes**, with a small symmetrical sealed smile. The last row reopens the eyes and reduces the smile. The primary candidate follows those revised peak pixels. A separate `half_relaxed_alternative` keeps approximately 54–56% of the neutral canonical eye aperture for comparison with the catalogue wording. That alternative is a static probe only, not a second performance and not a key in the primary timeline.

The catalogue's 1.9-second schedule is explicitly `proposed_reference_timing_not_implemented_animation`; numeric rig weights are null. The 4.6-second timing and control values here are newly authored interpretations, not reconstructed source animation. The exact source contours cannot be reproduced by the existing rigid-object controls. The paired BOD-016 and BOD-026 body references are not implemented.

## Performance and bounded geometry

Readability comes from a single gentle eye-settling transition, a clearly held pose, and reopening. There is no pulse, bounce, head/body action or enlarged grin.

| Anchor | Time | Smile-eye, each | Brow vertical, each | Mouth smile | Corner lift |
| --- | --- | ---: | ---: | ---: | ---: |
| Neutral | 0.00–0.25 s | 0 | 0 | 0 | 0 |
| Eyes soften | 0.70 s | 0.12 | -0.08 | 0.02 | 0.02 |
| Settling | 1.15 s | 0.30 | -0.20 | 0.08 | 0.08 |
| Quiet contentment | 1.65–2.80 s | 0.66 | -0.28 | 0.14 | 0.15 |
| Lingering smile | 3.60 s | 0.10 | -0.08 | 0.10 | 0.10 |
| Exact neutral return | 4.25–4.60 s | 0 | 0 | 0 | 0 |

The shared cubic smoothstep player is unchanged. Six primary anchors generate nine chronological keys. The alternative uses ordinary `blink_L` and `blink_R` at 0.28 instead of the smile-eye controls, with the same brow and mouth values as the peak.

- **Brows:** Existing rigid vertical controls lower the pivots by 2.8 source pixels, or 1.372 pixels at the 0.49 bust scale. No tilt or inner-brow lift is added. “Level” means no added tilt; the preserved source brow shape is not flattened or redrawn.
- **Eyes:** The smile-eye control at 0.66 produces effective canonical closure 1.0 and existing curved closed-eye shape 0.32. The aperture estimate reaches zero. The ordinary upper-lash node moves 36 source pixels as part of the existing closure/owner handoff. This is **not** a claim that a visible lash moves the full 17.64 bust pixels: clipping and the existing closed-eye owners replace the ordinary lash as the eyes close. Actual node, visibility, rotation and shader values are checked for every preserved smiling-eye joint.
- **Mouth:** Existing `mouth_smile=0.14` and `mouth_corner_lift=0.15` raise the outer contour by 2.36 source pixels, or 1.1564 bust pixels. The center stays fixed. The upper and lower contours share the same displacement, with zero gap, widening, purse or pressure. The intentionally small mouth action must be assessed in native detail and bust captures; numerical movement does not prove perceived readability.

No anatomy, artwork, shaders, ranges, production code or production data were changed. No gaze, blush, hair, head/body motion, lip-sync or automatic blink is authored. Automatic blinking is disabled during deterministic capture; separate lifecycle checks verify that the unchanged player suspends and restores it when previously enabled.

## Baseline preservation

The actual source registry contains **27 unique profiles and no EXP-003**. All 1,124 source files and 184 PNGs were copied from `hiding_smile_integration_work/ryoko_object_rig` and SHA-256 frozen, excluding generated caches. The original source and the copied rig still match every frozen byte. One generated UID sidecar for an unchanged inherited validation script is recorded in `IMPORT_GENERATED_FILES.json`.

Static probes and the candidate timeline are injected into the registry **only in memory** by external harnesses. No EXP-003 candidate file exists inside either production rig. Both disk registries and all approved release documentation remain untouched.

## Completed checks

- Headless Godot 4.6.3 import completed, with no error lines.
- Seven static probes: **4,179 assertions passed**, covering bounded controls, actual brow/lash/smile-eye geometry, sealed lip curves, fixed body, exact resets and in-memory-only registration.
- 139 chronological samples at 30 Hz: **8,664 assertions passed**, including eight restart/release/reset probes, manual takeover, and automatic-blink suspension/restoration.
- 4,601 samples at 1 ms spacing: **316,256 assertions passed**, covering monotone settling, exact hold, monotone release, neutral bookends, bounds, excluded controls and negative definition validation.
- Seven independent geometry diagnostics passed, including pixel-center aperture estimates and cross-checks against actual Godot transforms.
- All 27 preparation integrity checks passed: source/copy hashes, registry count and IDs, source provenance, data scope, isolated candidate and script syntax.
- Encoder precondition test exited safely before any encoding because native capture is absent.

These are targeted candidate preparation checks, not the complete production release suite. An inherited caught-staring component emits a warning about direct image loading in exported builds. Export packaging and lip-sync compatibility are outside this preparation. Native clipping seams, foreground-hair occlusion, visible expression strength and continuous normal-speed playback remain unverified.

## Repeat headless checks

From the containing workspace:

```sh
python -B quiet_contentment_work/build_candidate.py
sh quiet_contentment_work/run_static.sh --state
sh quiet_contentment_work/run_motion.sh --state
sh quiet_contentment_work/run_candidate.sh
python -B quiet_contentment_work/check_geometry.py
python -B quiet_contentment_work/record_import_metadata.py
python -B quiet_contentment_work/verify_preparation.py
```

`verify_preparation.py` verifies the **pre-capture** state and deliberately records that native captures and the movie are absent. Do not rerun `prepare_baseline.py` against this completed preparation without preserving the existing evidence.

## Ready native-review commands, not yet executed

The following commands are prepared for a separate native review stage. They do not run implicitly during headless checks.

```sh
sh run_static.sh --capture
```

Inspect all seven bust/detail pairs before motion capture. Compare the primary peak and `half_relaxed_alternative`. In particular, inspect the inherited ordinary-to-smiling closed-eye handoff, lash/eyelid seams, low brow placement, tiny sealed lip curve and identity at bust scale. The existing smiling-eye shape is an approximation of the revised source, not a traced match.

```sh
sh run_motion.sh --capture
python -B encode_preview.py
```

Capture wrappers refuse to overwrite an existing native capture. The encoder never starts a renderer and requires a passing native receipt plus exactly 139 endpoint-inclusive frames per view. Expected output: `Quiet_contentment_review_v1.mp4`, H.264, 968×800, 30 fps, 139 frames, 4.633333 seconds including the final endpoint frame. It checks file dimensions, rate, frame count and duration, then fully decodes the output. No movie currently exists.

Review continuous normal-speed playback after encoding. Confirm that the eye settling reads clearly without turning into sleepiness or an exaggerated happy crescent, that the tiny smile remains symmetric and sealed, that the hold remains quiet, and that the final neutral matches the opening. Approval and integration are separate subsequent decisions.

No CI, paid resources, purchases, hardware flashing or remote-machine execution was used.
