# Hiding a smile: unapproved review v1

EXP-153 is a data-only review candidate. Six isolated poses and a new 4.0-second timeline use the existing shared layer-assembly runtime. This package does not approve or register EXP-153 in production.

## Source evidence and limits

Source sheet: `insight_integration_work/avatar_build_assets/reference_library/assets/expressions/EXP-153_hiding-a-smile/RYO_EXP-153_hiding-a-smile_sheet_v001.png`.

- Sheet SHA-256: `e3d1d6c86522e8eaa82874a224b0d0d88a13b075ed37e4403de8ddd08875eb5c`.
- Catalogue: `insight_integration_work/avatar_build_assets/reference_library/metadata/expressions.json`.
- Catalogue SHA-256: `ded1b313c36b66daf46f3426288ef4670b04703497323314754bba18e872b2bf`.
- The exact EXP-153 metadata entry and source paths/hashes are retained in `SOURCE_REFERENCE.json`.

The actual nine-panel sheet was visually inspected. Its catalogue intent is: “Brows relax; eyes crinkle; lips press tightly while their corners keep lifting.” The middle row preserves visible amber eyes and a restrained, closed-mouth smile. The face stays forward. The catalogue labels its 1.9-second schedule `proposed_reference_timing_not_implemented_animation`; it provides no numeric control weights.

This candidate has **partial source fidelity**:

- Small, symmetric rigid inner-brow lifts and vertical offsets approximate brow relaxation. They cannot reproduce the source's painted brow curvature.
- Ordinary lids narrow to 0.38 at the peak while the eyes remain partly open. This represents narrowing, **not an actual lower-lid crinkle**. In the existing runtime, `eye_smile` values up to 0.5 only close the ordinary lids; values above 0.5 articulate the already closed crescent. That closed-eye substitute would conflict with the source's open amber eyes, so `eye_smile` remains zero.
- Existing sealed corner lift supplies the rising smile while lip pressure reaches 1.0. The latter reveals the existing inferred inner-upper-lip tissue; it is not a soft-tissue compression simulation and cannot reproduce the exact painted lip contour.

No new artwork, anatomy, shader, control, range or runtime modification was made. Mouth opening, ordinary smile/spread, purse, oral lift, kiss, independent width, gaze, blush, scoped widening/aversion/uneasy components and automatic blink remain zero. No hair, head, neck or body acting is authored. The paired full-body references are not implemented here.

## Baseline provenance

Preparation began from the fixed 25-profile `stunned_integration_work/ryoko_object_rig`. Before final headless checks, the copy was refreshed from `queasy_integration_work/ryoko_object_rig`, which contains **26 production profiles**, including EXP-090. EXP-153 and its probes are injected in memory by the harnesses, never written to the production registry.

The exact copied baseline contains **1,059 files and 184 PNGs**; all SHA-256 values are recorded in `BASELINE_FREEZE.json`. The copied rig includes the existing scoped-mouth handoff ordering fix. Its runtime and art are unchanged by this preparation.

This is a **26-profile integration snapshot**, not a claim of finalized26 release publication. At copy time, the inherited `RELEASE.json` still described 25 approved profiles. Inherited release files are preserved byte-for-byte as provenance. This preparation's own metadata, harnesses and checks use count26. Any later packaging refresh must record its own provenance and preserve the reviewed runtime/artwork.

The earlier 25-profile rig, state reports and freeze are retained under `historical_preparation/approved25/`. Its first import generated six new `.gd.uid` sidecars, recorded by that earlier integrity report as extra files; the final imported26 snapshot includes those sidecars and passes the exact-file check. The final result below, not the earlier receipt, is the current preparation evidence.

## Poses and timing

The six study poses are neutral, onset, build, hiding-smile peak, soften and exact neutral return.

| Pose | Ordinary lids, each | Brow offset, each | Inner-brow lift, each | Bilateral corner lift | Lip press |
| --- | ---: | ---: | ---: | ---: | ---: |
| Neutral / return | 0 | 0 | 0 | 0 | 0 |
| Onset | 0.08 | 0.02 | 0.03 | 0.08 | 0.35 |
| Build | 0.24 | 0.04 | 0.08 | 0.22 | 0.85 |
| Hiding smile | 0.38 | 0.04 | 0.10 | 0.50 | 1.00 |
| Soften | 0.16 | 0.02 | 0.04 | 0.20 | 0.50 |

The nine keys are neutral at 0.00 and 0.20 seconds, onset at 0.55, build at 0.95, peak at 1.40, peak held through 2.05, soften at 2.70, exact neutral at 3.75 and the final neutral endpoint at 4.00. Pressure rises ahead of the final corner lift so the smile appears contained rather than opening into a grin. This is newly authored timing, not recovered source animation. The shared cubic smoothstep sampler, displayed-pose restart and release are unchanged.

## Executed preparation checks

- Headless Godot 4.6.3 import: passed, no import error lines.
- Six-pose headless gate: **360 checks passed**, no failures.
- 121 chronological 30 Hz state samples plus restart, release and reset: **3,293 checks passed**, no failures. Every tested interruption returns to exact object neutral.
- Native six-pose capture: **372 checks passed**, no failures. The peak was visually reviewed as a coherent restrained closed smile with half-lidded amber eyes. This does not eliminate the disclosed lower-lid crinkle approximation.
- Frozen-file comparison after import/tests: **all 1,059 files and 184 PNGs unchanged**, production registry unchanged, no extra files outside generated caches.
- Python source syntax, shell syntax, source hashes, candidate timeline/plan correspondence, control allowlist, exact neutral bookends and candidate isolation: passed.

These are preparation checks, not a rerun of the entire production release suite. Static native capture and a peak-pose visual inspection are complete. Native timeline capture, encoded playback review, continuous normal-speed observation, user approval and publication remain pending. The inherited caught-staring component emits an image-loading warning for exported builds; this local preparation does not validate exported packaging.

## Reproduce

From `/workspace/scratch/42f2baf55663`:

```sh
python -B hiding_smile_work/build_candidate.py
python -B hiding_smile_work/run_gate.py --rig hiding_smile_work/rig
sh hiding_smile_work/run_motion.sh --state
python -B hiding_smile_work/verify_preparation.py
```

Exact static capture command, for a native renderer session:

```sh
python -B /workspace/scratch/42f2baf55663/hiding_smile_work/run_gate.py --rig /workspace/scratch/42f2baf55663/hiding_smile_work/rig --capture
```

Native timeline capture, then encode only after it completes:

```sh
sh /workspace/scratch/42f2baf55663/hiding_smile_work/run_motion.sh --capture
python -B /workspace/scratch/42f2baf55663/hiding_smile_work/encode_preview.py
```

The wrappers default to headless checks. Native capture is explicit, and both wrappers refuse to overwrite an existing capture. The encoder never starts a renderer. It requires 121 captured endpoint-inclusive frames per view and a passing native result, producing `Hiding_a_smile_review_v1.mp4`: 968×800 H.264 at 30 fps, expected duration 4.033333 seconds including the final endpoint frame. Native timeline capture and encoding completed. The MP4 fully decodes: 121 frames, 968x800, 30 fps, 4.033333 seconds, 188,875 bytes. Native motion checks passed 3,536 assertions. See REVIEW.md and REVIEW_RESULT.json for evidence and limitations.

`prepare_baseline.py` supports a deliberate baseline refresh from a ready 25- or 26-profile source, archives the earlier copy and receipts, then creates and verifies a new full-file freeze. It does not import, capture, approve or rewrite production files. Re-import the copied Godot project, rebuild the candidate and rerun checks after a refresh.

No CI, paid resources, purchases, hardware flashing or remote-machine execution was used.
