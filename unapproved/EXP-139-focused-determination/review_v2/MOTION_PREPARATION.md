# Focused determination v2: selected C and refocusing blink

**Unapproved review candidate.** This is the current motion-preparation record. `README.md` records the earlier static comparison stage with a later completion-status amendment. All A/B/C pose data and captures remain unchanged.

The native comparison passed 600 checks. C was selected for the next animation study: ten source pixels of symmetric brow lowering, opposing eight-degree brow tilts, five source pixels of sealed-mouth outward travel per side, and lip pressure 1.0. Selection for a candidate is not user approval or production integration.

## Clearer onset and readable hold

V1's movement was too subtle in review. V2 introduces a short refocusing blink and reaches the visibly stronger selected pose earlier, instead of only extending a slow drift. The blink is **newly authored timing, not recovered source animation**. The source catalogue permits normal blinking and requires open eyes at the focused peak.

| Time | Beat |
| --- | --- |
| 0.00–0.24 s | Exact neutral hold |
| 0.36 s | Early gathering: brows down 2 px, ±2° tilt, mouth sides 1 px outward, lip pressure 0.20; eyes still open |
| 0.48 s | Blink fully closed; brows down 7.5 px, ±6.8° tilt, mouth sides 4 px outward, pressure 0.85 |
| 0.48–0.54 s | Brief complete closure |
| 0.70 s | Eyes fully reopened; brows down 9.5 px, ±8° tilt, mouth sides 5 px outward, pressure 1.0 |
| 0.78–2.40 s | Exact selected C with fully open eyes, held for 1.62 s |
| 3.00 s | Softened recovery: brows down 3.5 px, ±3.2° tilt, mouth sides 1.6 px outward, pressure 0.35 |
| 3.65–4.00 s | Exact neutral finish |

The blink occupies only 0.36–0.70 seconds: 0.12 seconds closing, 0.06 seconds fully closed and 0.16 seconds reopening. Peak and recovery use zero lid closure, not a sustained squint. The selected face arrives 0.54 seconds after the initial neutral hold. All eleven keys use the unchanged cubic smoothstep sampler. No easing or runtime code was altered.

Ordinary `blink_L` and `blink_R` are the only additional controls compared with selected C. They remain symmetric. No smiling-eye crescent, gaze, smile, corner lift, opening, purse, blush, head/body acting or new anatomy is introduced. The existing no-horizontal-brow-convergence and inferred-lip-pressure limitations remain as described in the static study.

## Preserved evidence and isolation

- Original six-pose alternatives, native captures, static scripts and reports are unchanged. `STATIC_ALTERNATIVES_FREEZE.json` records the historical checkpoint. Of its 28 files, 27 remain byte-identical; `README.md` was later amended to reflect completed motion review. `PUBLICATION_INVENTORY.json` records the final difference.
- New static onset poses and captures live in `onset_study/`.
- New candidate data, motion harness, encoder and motion outputs live in `motion_study/`.
- Both studies use the same frozen `rig/`. All 1,112 baseline files and 184 PNGs remain unchanged, including every approved profile. EXP-139 is injected only in memory.
- The actual baseline registry contains 27 profiles. Inherited release metadata remains the unmodified26 provenance described in the earlier study.

## Executed preparation checks

- Six onset poses: **580 headless checks passed**, including the half-blink, full closure, reopened pose, exact selected C, sealed mouth, measured geometry and exact reset.
- Motion: **63,705 checks passed**, covering 4,001 dense millisecond timeline samples, 121 chronological 30 Hz samples, exact C throughout the hold, blink confinement to onset, fully reopened peak/recovery, restart/release continuity and exact neutral reset/endpoints.
- Full baseline and original static evidence hash verification passed. No approved files changed.
- Python/shell syntax and candidate timing/control restrictions passed.

These checks do not establish whether the blink looks natural or the motion is perceptible at normal speed. Native onset review, v2 motion capture and encoding have since completed; see REVIEW.md and REVIEW_RESULT.json. User approval remains pending. The inherited exported-image warning remains unchanged; exported packaging is not tested.

## Native onset capture

```sh
python -B /workspace/scratch/42f2baf55663/focused_determination_v2_work/onset_study/run_gate.py --rig /workspace/scratch/42f2baf55663/focused_determination_v2_work/rig --capture
```

This writes only `onset_study/capture/`: neutral, half blink, full blink, reopened face, selected C and neutral return, in detail and bust views. The original `capture/` is untouched. Inspect lid closure, reopening, brow/lid spacing and the sealed-mouth transitions before proceeding.

## Motion capture and encoding

After onset visual review:

```sh
sh /workspace/scratch/42f2baf55663/focused_determination_v2_work/motion_study/run_motion.sh --capture
python -B /workspace/scratch/42f2baf55663/focused_determination_v2_work/motion_study/encode_preview.py
```

The encoder requires a successful native result and 121 captured frames per view. It produces `motion_study/Focused_determination_review_v2.mp4`, expected 968×800 H.264, 30 fps, 4.033333 seconds including the final endpoint. It never launches a renderer. Capture and encoding refuse to overwrite existing outputs.

Headless reproduction:

```sh
python -B focused_determination_v2_work/motion_study/build_candidate.py
python -B focused_determination_v2_work/onset_study/run_gate.py --rig focused_determination_v2_work/rig
sh focused_determination_v2_work/motion_study/run_motion.sh --state
python -B focused_determination_v2_work/motion_study/verify_preparation.py
```

No CI, paid resources, purchases, hardware flashing or remote-machine execution was used.
