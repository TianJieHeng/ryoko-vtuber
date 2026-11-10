# Focused determination v2: static alternatives

**Unapproved review revision.** C was selected and a motion preview was captured after the static study described here. User approval and production integration remain pending. V1 was too subtle in review. This study preserves v1 and compares its exact peak against three stronger alternatives using the same approved27 runtime and artwork.

## What changed

V1 lowered each brow pivot only 2.5 source pixels and rotated the brows by opposing 4.8-degree angles. Its maximum lip-pressure control did not visibly change much of the mouth. V2 materially increases brow motion and tests existing sealed-mouth width as a separate tension cue.

| Study | Each brow lowered | Opposing brow rotation | Sealed-mouth side travel | Lip pressure |
| --- | ---: | ---: | ---: | ---: |
| V1 peak reference | 2.5 px | ±4.8° | 0 px | 1.0 |
| A: lowered focus | 6.5 px | ±6.4° | 0 px | 1.0 |
| B: firm line | 8.5 px | ±8.0° | 2.4 px outward per side | 1.0 |
| C: strongest open | 10.0 px | ±8.0° | 5.0 px outward per side | 1.0 |

These are measured runtime transform values, not estimates based only on control weights. `state_checks.json` records every actual brow-pivot delta, angle and mouth-side displacement. The normalized values are in `plan.json`:

- Brow vertical: A -0.65, B -0.85, C -1.0 on both sides; allowed range [-1, 1], mapped to ten source pixels.
- Brow tilt: A +0.80/-0.80, B and C +1.0/-1.0; allowed range [-1, 1], mapped to eight degrees.
- Independent sealed-mouth width: A 0, B 0.12, C 0.25 on both sides; allowed range [0, 1], up to twenty source pixels outward per side. Because mouth opening, spread and smile are zero, the tested side displacements are exactly 0, 2.4 and 5 pixels.
- Lip pressure remains 1.0, its existing upper bound. It reveals existing inner-upper-lip material; there is no new pressure range or new anatomy.

Both eyes retain the fully open neutral lid state. Opening, smile, corner lifts, purse, oral lift, kiss, gaze, blush, scoped eye/mouth components, hair and automatic blink remain zero. Head and body remain fixed. Tests confirm the outer lip pivots do not move vertically, so the width study does not introduce a commanded smile or pout. Whether the rendered contour reads as purposeful tension still requires visual review.

## Source and limits

The inspected EXP-139 nine-panel sheet and its peak describe: “Brows converge firmly; eyes stay open rather than glaring; lips press into a purposeful line.” The source peak shows stronger inward-sloping brows with open amber eyes and a closed mouth.

Source sheet: `insight_integration_work/avatar_build_assets/reference_library/assets/expressions/EXP-139_focused-determination/RYO_EXP-139_focused-determination_sheet_v001.png`.

SHA-256: `a10a347e6d949606d346e65bd07b11cd9546f7e2e96944a8ded6be00fa8258b1`.

`SOURCE_REFERENCE.json` preserves the exact catalogue entry. Numeric source weights are not available. The catalogue's 1.9-second schedule is proposed reference timing, not implemented animation.

The existing rig has no inward horizontal brow translation or local brow squeeze. Its lowering and rigid rotation approximate convergence but cannot reshape the painted brow. The stronger B/C brow settings reach the existing tilt limit; C also reaches the lowering limit. They must be rejected if the native result looks angry, obscures the eyes, collides with the eyelids or departs from the intended open-eyed focus.

B and C test slight horizontal tension using the already supported closed-mouth width controls. They are not asserted to match exact source width. If either reads as a smile, pout or stretched mouth, select A or reduce width before authoring motion. No new artwork, runtime, shaders, anatomy, controls or bounds were introduced.

## Preservation and isolation

The rig was copied from the exact v1 review rig without `.godot` or Python caches. All **1,112 frozen files and 184 PNGs** remain byte-exact. This includes v1's recorded Godot UID sidecar and the existing EXP-116 profile. The actual registry has 27 entries, including EXP-153 but not EXP-139. Inherited release metadata still describes 26; it remains untouched provenance, not a v2 release claim.

`BASELINE_FREEZE.json` records every copied hash and links the original v1 freeze by hash. `V1_PROVENANCE.json` records the v1 files at the start of this study. No v1 files, approved profiles or production registry entries were edited.

The six static study poses are neutral, the exact v1 peak, A, B, C and neutral return. Temporary probe timelines exist only in memory to hold each pose for capture. At the static comparison checkpoint, no final `EXP-139.json`, motion harness, animation or video had been created. The subsequent selected-C candidate, motion harness and preview are in `motion_study/`; see `REVIEW.md` for the completed review and `PUBLICATION.md` for the backup scope and reproduction instructions.

## Checks and completed native review

- Headless Godot import passed.
- **588 static checks passed**, including actual geometry, supported domains, open eyes, zero smile/pout/opening, fixed head/body and exact reset.
- Integrity passed: **1,112 baseline files unchanged**, no missing or extra files outside caches, production registry unchanged.
- Python syntax, source hash, exact v1 comparison pose, materially stronger bounded brow controls and symmetric sealed-width values passed.
- Native selection chose C. New onset capture passed 592 checks; motion capture passed 63,948 checks. The MP4 fully decodes. Normal-speed desktop playback was sampled visually; continuous viewing or live engine pacing is not certified. User approval and integration remain pending. See REVIEW.md and REVIEW_RESULT.json.

The inherited caught-staring component emits its existing exported-image warning; exported packaging is not validated here.

Headless reproduction:

```sh
python -B /workspace/scratch/42f2baf55663/focused_determination_v2_work/run_gate.py --rig /workspace/scratch/42f2baf55663/focused_determination_v2_work/rig
python -B /workspace/scratch/42f2baf55663/focused_determination_v2_work/verify_preparation.py
```

Exact native static capture command:

```sh
python -B /workspace/scratch/42f2baf55663/focused_determination_v2_work/run_gate.py --rig /workspace/scratch/42f2baf55663/focused_determination_v2_work/rig --capture
```

The native command produces bust and detail views for all six poses and refuses to overwrite an existing capture. Compare each alternative against both `neutral` and `v1_peak_reference` before selecting a pose for motion.

No CI, paid resources, purchases, hardware flashing or remote-machine execution was used.
