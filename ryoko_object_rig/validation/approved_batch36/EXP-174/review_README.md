# Sleepy annoyance: unapproved review v1

EXP-174 is a data-only, four-second review candidate. It combines heavy open lids, a sharp lowering of the brows, and a compact sealed pout using existing bounded controls. It is **not approved and is not registered in production**. Native static capture and the review MP4 have since completed; see REVIEW.md and REVIEW_RESULT.json.

## Reference and interpretation

The actual nine-panel source sheet was visually inspected. Its middle row shows lower inward-sloping brows over narrowed but visible amber eyes, with a small downturned closed mouth. The catalogue intent is:

> Brows lower sharply despite heavy lids; eyes narrow; lower lip pushes forward.

The sheet is `avatar_build_assets/reference_library/assets/expressions/EXP-174_sleepy-annoyance/RYO_EXP-174_sleepy-annoyance_sheet_v001.png`, SHA-256 `cd149911dfd8c7309f25ed828772e739f6a79f859e824b69c98a0c87281cfcca`.

`SOURCE_REFERENCE.json` preserves the exact EXP-174 catalogue entry, source paths and hashes. The catalogue's 1.9-second schedule is explicitly `proposed_reference_timing_not_implemented_animation`; its numeric control weights are null. This candidate's timing and weights are newly authored, not recovered source animation.

### Supported controls and limits

- **Brows:** Both existing vertical controls reach -1.0, lowering each brow pivot by 10 source pixels. Opposing +1.0/-1.0 rigid tilts rotate the brows by +8/-8 degrees, lowering their inner ends. There is no inward horizontal brow translation or local brow-knit control. The source's localized brow shape is approximated by rigid lowering and tilt. Inner-brow lift remains zero because it raises the inner ends.
- **Heavy lids:** The ordinary closure controls reach 0.40 symmetrically. The actual upper-lash nodes descend 14.4 source pixels; the unchanged canonical aperture shader clips the eye interior with the same closure. No smile-eye control, gaze shift or full blink is added. Source-pixel-center aperture estimates retain about 38.1% of the neutral screen-left aperture and 36.3% of the screen-right aperture. These are numerical estimates, not native image measurements.
- **Pout:** Existing sealed `mouth_purse` reaches 0.75. The existing contour moves inward by 10.5 source pixels on each side, narrowing by 21 pixels total. Its center descends 3 pixels and the side contours descend 9 pixels. Both upper and lower contours receive the same displacement. **There is no lower-lip projection, independent lower-lip push, depth control or newly authored lip shape.** The compact whole-mouth purse only approximates that part of the source intent; it must not be described as reproducing the projected lower lip.

No artwork, anatomy, shader, runtime, control or range was changed. Mouth opening, lip pressure, smile, width, corner lift, oral lift, kiss, gaze, blush, hair, head and body controls stay zero. The separately paired BOD-019 and BOD-038 references are not implemented. Lip-sync compatibility and exported-build packaging are not tested.

## Bust-scale geometry

The study deliberately uses the full existing brow-lowering and rigid-tilt ranges instead of relying on subtle parameter changes. At the existing 0.49 bust scale, the peak has:

| Feature | Source geometry | Bust-scale travel |
| --- | ---: | ---: |
| Brow pivot lowering | 10 px | 4.90 px |
| Brow tilt | +8 / -8 degrees | Same angles |
| Upper-lash lowering | 14.4 px | 7.06 px |
| Total mouth-width reduction | 21 px | 10.29 px |

`state_checks.json` records actual Godot node transforms, shader closure inputs and mouth geometry. `geometry_checks.json` independently evaluates the preserved source aperture profiles at pixel centers. Native filtering, lashes, foreground hair occlusion, visible expression strength and identity still need review in the actual capture. Geometry alone cannot establish visual fidelity.

## Poses and timing

| Anchor | Time | Lid closure, each | Brow vertical, each | Left / right tilt | Mouth purse |
| --- | --- | ---: | ---: | ---: | ---: |
| Neutral | 0.00–0.20 s | 0 | 0 | 0 / 0 | 0 |
| Drowsy onset | 0.52 s | 0.25 | -0.12 | +0.12 / -0.12 | 0.16 |
| Annoyed build | 0.82 s | 0.36 | -0.75 | +0.85 / -0.85 | 0.55 |
| Sleepy annoyance | 1.12–2.20 s | 0.40 | -1.00 | +1.00 / -1.00 | 0.75 |
| Soften | 2.95 s | 0.22 | -0.35 | +0.35 / -0.35 | 0.25 |
| Exact neutral return | 3.70–4.00 s | 0 | 0 | 0 / 0 | 0 |

Heavy lids arrive before the strongest brow lowering. The brow action then builds more sharply over 0.60 seconds, followed by a 1.08-second exact peak hold and a gradual release. The unchanged shared cubic smoothstep, displayed-pose restart and release handle all interpolation. Six static anchors produce nine timeline keys. Automatic blinking is disabled for these deterministic review captures.

## Baseline preservation

The source is the published 27-profile rig at [commit 816d77f](https://github.com/TianJieHeng/ryoko-vtuber/commit/816d77fafb6e016dc70f0802743d444e618f7b0f), copied from `hiding_smile_integration_work/ryoko_object_rig`.

The actual registry was inspected before preparation: it contains 27 unique profiles, including EXP-153 and EXP-116, and no EXP-174. All **1,124 source files and 184 PNGs** were copied and hashed, excluding generated caches. Both the original source and copied rig still match every frozen file. Godot generated one UID sidecar for an unchanged inherited validation script; its exact contents and hash are recorded in `IMPORT_GENERATED_FILES.json`.

The six static probe profiles and EXP-174 timeline are loaded only into memory by external harnesses. No candidate JSON is written inside the copied rig, and neither production registry is modified. The baseline release documentation remains unchanged.

## Completed checks

- Headless Godot import completed without error lines.
- Six static pose, actual geometry, bounded-control, fixed-body and exact-reset probes: **672 checks passed**, no failures.
- 121 chronological 30 Hz samples, scoped and bounded controls, exact final neutral, plus restart/release/reset probes at eight times: **7,299 checks passed**, no failures.
- Geometry diagnostics: all five checks passed. The reduced aperture stays open, while the planned brow, lash and mouth travel exceed the documented bust-scale thresholds.
- Source and copied-rig integrity, 27-profile registry preservation, source hashes, candidate scope, Python syntax and shell syntax: passed.

The initial harness rejected float32 rounding of `0.40` to `0.400000005960464` and 1.2-pixel brow travel to `1.20001220703125`. Those diagnostic logs and results are preserved under `validation_history/initial_float_tolerance/`. The assertions were corrected to a 0.000001 closure tolerance and a 0.0001-source-pixel travel tolerance. Authored weights and runtime/API bounds were not changed. The final results above are the rerun after those harness corrections.

These are targeted preparation checks, not a rerun of the full production release suite. An inherited caught-staring component warns about direct image loading in exported builds; exported packaging is outside this study.

## Reproduce headless checks

From `/workspace/scratch/42f2baf55663`, using the already imported copied rig:

```sh
python -B sleepy_annoyance_work/build_candidate.py
python -B sleepy_annoyance_work/run_gate.py --rig sleepy_annoyance_work/rig
sh sleepy_annoyance_work/run_motion.sh --state
python -B sleepy_annoyance_work/check_geometry.py
python -B sleepy_annoyance_work/record_import_metadata.py
python -B sleepy_annoyance_work/verify_preparation.py
```

## Native capture and encoding

These stages have not been run for this candidate. Exact static capture command in a native renderer session:

```sh
python -B /workspace/scratch/42f2baf55663/sleepy_annoyance_work/run_gate.py --rig /workspace/scratch/42f2baf55663/sleepy_annoyance_work/rig --capture
```

Inspect the neutral, drowsy onset, build, peak, soften and neutral-return bust/detail pairs before continuing. Check that visible irises remain, the brows do not merge into eyelids or expose holes, and the pursed lip edges remain connected with no unintended opening.

Then capture the timeline and encode only after the native checks pass:

```sh
sh /workspace/scratch/42f2baf55663/sleepy_annoyance_work/run_motion.sh --capture
python -B /workspace/scratch/42f2baf55663/sleepy_annoyance_work/encode_preview.py
```

The wrappers default to headless checks and require an explicit capture flag. They refuse to overwrite an existing native capture. The encoder never starts a renderer and requires a passing native result plus exactly 121 endpoint-inclusive frames for each view. Its output is `Sleepy_annoyance_review_v1.mp4`, 968×800 H.264 at 30 fps, expected duration 4.033333 seconds including the final endpoint frame. It probes the finished file and checks a full decode.

The MP4 fully decodes: H.264, 968x800, 30 fps, 121 frames, 4.033333 seconds, 196,718 bytes. Native static and motion checks passed 684 and 7,542 assertions. Continuous normal-speed observation, user approval and production integration remain pending. No CI, paid resources, purchases, hardware flashing or remote-machine execution was used.
