# Queasy: unapproved preparation v1

EXP-090 is a data-only review candidate. The six-pose study and new 4.0-second timeline use the existing shared layer-assembly runtime. This preparation does not approve or register EXP-090 in production.

## Source and scope

Source: `insight_integration_work/avatar_build_assets/reference_library/assets/expressions/EXP-090_queasy/RYO_EXP-090_queasy_sheet_v001.png`.

Sheet SHA-256: `785b45abad9297a18294d4a3fbf93ab52d8577e05556fc2279cbd223a7d2c4ce`.

Catalogue SHA-256: `ded1b313c36b66daf46f3426288ef4670b04703497323314754bba18e872b2bf`.

The source sheet was visually inspected. Its intent is rising inner brows, heavy narrowed lids, forward-pressed lips and tense cheeks. The existing rig **does have** independent rigid outer-anchor inner-brow controls, so the candidate uses them rather than substituting a whole-brow vertical raise. Those rigid rotations cannot reproduce the source's curved painted brows. The existing sealed purse and lip-pressure controls approximate the lip contour; there is no forward-depth deformation. Cheek tension/deformation is unsupported and is not added or claimed. No new anatomy, art, shaders or runtime changes were made.

No gaze, smile, blush, automatic blink, hair, head, neck or body acting is authored. Mouth opening, kiss, custom uneasy component, eye-widening and aversion remain zero. The existing ordinary lids supply the heavy-lid narrowing.

## Baseline provenance

Preparation started against approved24. It was refreshed from `stunned_integration_work/ryoko_object_rig` after EXP-063 was included, before the final headless tests. The working copy has **25 production profiles**, including EXP-063, and no EXP-090 on disk. The exact 990-file/184-PNG source snapshot is recorded in `BASELINE_FREEZE.json`; the earlier approved24 copy and receipt are preserved under `historical_preparation/`.

This is a **25-profile integration snapshot**, not a claim of finalized25 release publication. At copy time the source's inherited RELEASE, integration manifests and repository-specific guard still described approved24. They are retained byte-exact as inherited provenance rather than rewritten to fabricate a release receipt. Queasy's own harnesses, profile metadata and checks use count25. A later finalized25 packaging refresh must keep the rendered runtime/artwork unchanged and record its new provenance explicitly.

## Poses and timing

The six poses are neutral, onset, build, queasy, soften and neutral return. Peak uses ordinary lids 0.44/0.44, rigid inner-brow lifts 0.68/0.60, small whole-brow lowering -0.08/-0.08, sealed purse 0.72 and lip press 1.0. Everything else is zero.

The nine-key timeline is neutral at 0 and 0.25 seconds, onset at 0.55, build at 0.95, peak at 1.30, peak hold through 2.00, soften at 2.65, exact neutral at 3.75 and a final neutral endpoint at 4.00. It uses the unchanged shared smoothstep sampler and displayed-pose restart/release. The catalogue's 1.9-second schedule is an unimplemented reference proposal, not recovered animation.

## Executed preparation checks

- Headless Godot 4.6.3 import: passed.
- Six-pose headless gate: **360 checks passed**, no failures.
- 121 chronological 30 Hz state samples plus restart, release and reset: **3,293 checks passed**, no failures. Exact object neutral returned at the endpoint and after tested interruptions.
- Frozen-file comparison after import/tests: **all 990 source files and 184 PNGs unchanged**, including the production registry; no extra files outside the generated cache.
- Python source syntax and shell wrapper syntax: passed.
- Supplementary inherited `tools/verify_approved_integration.py`: not a valid standalone-copy gate. Its invocation failed because it requires the original Git checkout layout, and its retained source still asserts approved24. This is not reported as a passed release/integration guard.

The existing caught-staring component emits a warning about loading an image file in exported builds. It is inherited and unchanged; this local preparation does not validate packaged exports.

The six-pose native capture passed **372 checks**. The peak is a restrained Queasy pose with heavy lids, sealed pursed lips and subtle rigid brow motion. Completed native timeline evidence is summarized below. No continuous normal-speed observation or live pacing claim is made.

## Reproduce

All paths below are local. `run_motion.sh` defaults to headless checks and requires explicit `--capture` for native capture. Both capture wrappers refuse to overwrite existing output; preserve earlier captures before another pass. Neither harness writes a definition or probe to the rig's disk registry.

```sh
python -B queasy_work/build_candidate.py
python -B queasy_work/run_gate.py --rig queasy_work/rig
sh queasy_work/run_motion.sh --state
python -B queasy_work/verify_preparation.py
```

Static capture command:

```sh
python -B /workspace/scratch/42f2baf55663/queasy_work/run_gate.py --rig /workspace/scratch/42f2baf55663/queasy_work/rig --capture
```

Native timeline capture, then encode only after it finishes:

```sh
sh /workspace/scratch/42f2baf55663/queasy_work/run_motion.sh --capture
python -B /workspace/scratch/42f2baf55663/queasy_work/encode_preview.py
```

The encoder expects 121 endpoint-inclusive frames in each view, producing a 968×800 H.264 review video at 30 fps, 4.033333 seconds including the final neutral endpoint frame. It never starts the renderer and fails clearly if native capture is missing. No CI, paid resources, remote-machine execution or hardware action was used.

## Completed native review

Native timeline capture passed 3,536 checks. The four-second profile yielded 121 endpoint-inclusive frames at 30 fps. Queasy_review_v1.mp4 is H.264, 968x800, 4.033333 seconds, 198,488 bytes, and fully decodes. Independent review verified every native-frame hash, exact neutral bookends, frozen body/outside-face pixels, and encoded frame ordering. See REVIEW.md and REVIEW_RESULT.json. This is ready for user review, not approved.

During separate EXP-063 integration, a scoped-to-sealed mouth transition ordering defect was identified and a minimal shared bridge ordering fix prepared. This Queasy capture used the frozen pre-fix snapshot described above. Its neutral-start one-shot does not exercise that transition. Neither this capture nor the independent review claims whole-production or cross-profile sign-off.
