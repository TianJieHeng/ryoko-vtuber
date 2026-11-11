# EXP-123 Puzzled: independent source and preparation review

**Latest update:** Native capture and MP4 evidence have now arrived. The editor-only byte rewrite was archived and exactly restored under parent direction after the UI exited. Final independent validation is **PASS, 73/73**, with **16 tests passing**. See `INDEPENDENT_NATIVE_REVIEW.md` for the subsequent pixel inspection, evidence results, restoration audit, and remaining acceptance limits. The source-stage and temporary mismatch checkpoints below are retained as review history; they are not the latest capture status.

## Decision

**Suitable only for a limited native preview; UNAPPROVED.** I found no preservation, numerical, or source-direction blocker to collecting the proposed native evidence. The raised-inner-brow / opposite-lowered-brow / uneven-lid construction is a defensible facial-only interpretation of the source. The mouth is a materially limited approximation, not a reproduction of the source's sideways, oblique pout. Whether the combined result reads as Puzzled rather than generic skepticism or displeasure remains an acceptance question requiring actual candidate pixels and normal-speed viewing.

This is not visual approval, integration approval, or a claim that the complete source intent has been achieved. If acceptance requires genuine lateral translation or the painted diagonal mouth shape, the current candidate does **not** meet that requirement.

## Inputs independently examined

- The actual 1159 × 1358 nine-panel `RYO_EXP-123_puzzled_sheet_v001.png` was opened and visually inspected, including the middle-row peak and the bottom-row release. This review did not rely solely on the authoring notes or catalogue prose.
- Sheet SHA-256: `c5e0d6af76652cc5f3ee4b60a642faf79d515f5d6fb7299fe0f67aeac0dd1d05`.
- All nine panel files match their catalogue hashes and are pixel-exact integer crops of the inspected sheet. The copied `SOURCE_CATALOGUE_ENTRY.json` is exactly the matching entry in the hash-pinned source catalogue.
- Frozen review-input SHA-256: `d715fd00b418e2f4f60e886477e95844433f1c5312460fd090bfe4d63406d6ef`. All 12 pinned files matched on the first independent pass. A concurrent launcher project rewrite was detected on the final recheck; see the final checkpoint below. The candidate, plan, source-description, and probe files remain unchanged.
- `EXP-123.json`, all eight static anchors, 121 recorded headless states, both probe sources, relevant shared control limits and geometry code, and source object pivots were read. All 39 comparison profiles were independently sampled rather than simply trusting `DISTINCTNESS_CHECK.json`.

## Source interpretation and limits

The sheet shows a relatively neutral first panel, then a questioning relationship in which the screen-left inner brow curls upward while the opposite brow lowers. The screen-left eye becomes more narrowed. The sealed mouth gathers into a smaller, skewed/oblique pout, strongest in the middle row. The head also tilts, especially in panel 5. The bottom row relaxes toward neutral.

The candidate intentionally uses fixed gaze and no head/body motion. Omitting the tilt is consistent with its declared facial-only scope, but removes a visible contributor to the source's questioning read. Suggested body references BOD-004 and BOD-030 are not implemented or validated here.

### Brows

At the held candidate peak, the screen-left inner-lift weight is 0.30, giving an additional **−7.8° rigid rotation** around the existing outer anchor after legacy motion. Its recorded pivot displacement is approximately `(0.7966, −3.0151)` source pixels. The opposite brow moves down **3.4 source pixels** and rotates **−1.92°**, with no opposite inner-lift control. Independent trigonometry from the frozen object pivots agrees with all eight static receipts within float tolerances.

This rotates the existing painted brow; it cannot locally bend the brow pigment into the source's curved inner tip. The outer anchor is preserved relative to the pre-existing tilt/translation, not fixed in absolute image coordinates. The screen-left whole-brow channel also lowers the anchor by 1.6 source pixels at peak, while the rotation raises its inner region. These are limited rigid-part controls, not anatomical brow reshaping.

### Eyes and side conventions

Peak ordinary closures are `blink_R=0.28` and `blink_L=0.11`. In this rig those correspond to **screen-left 10.08-source-pixel upper-lash travel** and **screen-right 3.96 pixels**. The independent check verifies the actual recorded screen-side geometry, avoiding the earlier authoring/test confusion between character-side blink names and screen-side brow names. At reconsideration they become 0.32 and 0.15, respectively.

That direction is consistent with the inspected sheet. It does not prove a faithful rendered eyelid contour, eye comfort, iris clipping, or gaze appearance. Ordinary auto-blink is disabled in the isolated probes. Blending with normal blink or lip sync has not been established.

### Mouth: the principal fidelity risk

At `mouth_purse=0.58` and screen-right sealed width `0.20`:

- Left endpoint moves **+8.12 source pixels**; right endpoint moves **−4.12 source pixels**.
- The nominal source span contracts from 71 to **58.76 pixels**.
- The endpoint midpoint is biased **2 source pixels to screen-right**, approximately **0.98 pixels at the 0.49 bust scale**.
- The horizontal center at source x=39.5 remains fixed. This is asymmetric contraction/width, **not a whole-mouth lateral translation**.
- The shared purse lowers the center contour by **2.32 source pixels** and both sampled outer contours by **6.96 pixels**. The vertical contour is symmetric; it does **not** produce the source's diagonal lip line. “Fixed center” here means horizontally, not a claim of zero vertical contour movement.
- Upper and lower contour offsets match, the mouth-open channel stays zero, and the independently computed horizontal map remains monotonic.

The approximately one-bust-pixel midpoint bias may be hard to read at ordinary presentation size. A detail view can expose the geometry without establishing that the cue survives at bust size. The candidate must not be described as having faithfully recreated a sideways-translated or diagonal pout merely because the numeric width channel is nonzero.

### Timing

The source is nine still references with proposed 1.9-second timing, not recovered animation. This candidate newly authors a four-second performance: brow cue before purse, held peak from 1.4–1.9 seconds, a small rechecking squint near 2.3, lip bias released before the questioning brow, then exact neutral from 3.7–4.0. That is a coherent interpretation, not source-timing fidelity.

Independent Python interpolation across all 121 records gives maximum control error **1.4879085241670253e-08**. The existing headless receipts report **1,494 static** and **8,902 motion** assertions passing, including 36 lifecycle assertions at nine interruption times. This reviewer audited those receipts and recomputed the geometry/timeline; it did not rerun Godot or infer native rendering from a headless PASS.

## Distinction assessment

All 36 frozen baseline profiles plus Mental Arithmetic, Controlled Anger, and Broad Surprise have different nonzero-control sets and nonidentical normalized-time trajectories. This demonstrates data-level nonduplication only.

- **EXP-129 Mental Arithmetic:** alternates whole-brow lifts and includes an upward glance. Puzzled holds one inner-lift side, keeps forward gaze, and uses uneven narrowing plus unilateral sealed width. The different movement pattern is stronger evidence than a small numeric weight change, but perceptual distinction is pending.
- **EXP-050 Frustrated Pout:** uses much stronger bilateral brow lowering/tilt and purse up to 1.0, without an inner-lift or unilateral width control. Puzzled has a less forceful, asymmetric brow question. Both share the same purse mechanism, so the mouth alone is not a reliable distinctness cue.
- **EXP-102 Knowing Smirk:** uses smile, spread, and an independent lifted corner. Those controls remain zero in Puzzled. The candidate is designed to remain unsmiling, but that rendered read is not yet proven.
- The nearest profile under the all-channel RMS metric is **EXP-040 Recovering Composure** (approximately 0.10990), followed by **EXP-042 Cold Glare** (0.12124). That metric includes many zero channels and is not perceptually weighted; it does not rank visual similarity. Composure uses bilateral inner lifts and smile/corner controls; Cold Glare uses symmetric lowering and narrowing without the questioning inner lift.

No side-by-side candidate pixel or normal-speed comparison has been completed. Generic skeptical/displeased overlap remains possible, particularly if the mouth bias is too subtle at bust scale.

## Preservation and baseline scope

Fresh independent hashing found all **999 pinned source files, including 184 PNGs**, unchanged in both the frozen source rig and the candidate `rig/`. The extra approved source manifest also matches in both locations. The source sheet, catalogue, and all nine panels remain exact. Both disk registries contain precisely the original 36 IDs and exclude EXP-123.

The separate native launcher matches 998 pinned files; its only pinned override is the declared project name/main-scene change in `project.godot`. Its extra approved source manifest is present and unchanged too.

The baseline is deliberately **approved36**, commit `3ce98774282ad6c20dfbd7018d20838ff861b762`. This review does not mistake that for the later approved39 integration, nor does it establish approved39 regression parity or authorize a registry change. Existing historical `UNAPPROVED` strings in some preserved comparator profiles do not override their later integration status.

## Pending evidence and exact blocker

At this review checkpoint, the candidate has no native stills, motion frames, native capture receipts, or `Puzzled_review_v1.mp4`. Native capture is **pending**, not attempted or denied by this reviewer. The parent owns any separately permitted native UI capture. No alternative renderer, display server, launch workaround, source change, or publication was performed here.

Before acceptance, the native evidence must establish:

1. Correct 568 × 800 bust/full and 400 × 360 detail captures with intact facial parts, lip seam, and iris/lash coverage.
2. Whether the unilateral brow and subtle mouth asymmetry actually read as Puzzled at bust size, without an unintended smile or generic angry read.
3. Smooth whole-performance playback, the held question/reconsideration timing, and exact neutral return. Frame math and an encoded frame-order check are not continuous observation.
4. Perceptual distinction from the relevant existing performances. The unchanged source baseline does not substitute for later integration/regression review.

A source-fidelity acceptance requiring a true translated/diagonal pout remains blocked by the disclosed rig limitation, even if every numeric and encoding check passes.

## Independent read-only validator

Prepared `review_validation.py`, adapted from the Broad Surprise validator with EXP-123-specific identities, sheet dimensions, receipt counts, side conventions, anchored-brow/lash/mouth geometry, timeline assertions, and grid-aligned anchor matching. Run:

```text
python puzzled_work/review_validation.py
python -m unittest discover -s puzzled_work -p test_review_validation.py -v
```

The validator never starts Godot, a UI, renderer, encoder, or publication. It reads frozen inputs and captured evidence, invokes only `ffprobe`/`ffmpeg` decoding when a video is present, and writes reports/contact sheets to `--output` or `review_evidence/`.

The native stage checks all 16 stills and 242 motion PNGs, dimensions, RGBA hashes, exact ordered names, input-linked receipts, all 121 poses, body pixels outside the bounded face box, all peak-hold frames, neutral holds, and exact static/motion identity only at true grid-aligned anchors. Half-frame anchors such as 0.55 and 0.95 seconds are deliberately not compared with nearby samples as though equal.

The MP4 stage checks the expected 968 × 800 layout, 30 fps timestamps, 121-frame clean decode, H.264/yuv420p encoding and duration, same-index native panel similarity, and nearest-frame face errors. It exports selected decoded frames for inspection. Lossy encoding makes identical/near-identical holds ambiguous; this cannot prove unique ordering within indistinguishable holds or replace normal-speed viewing.

Initial execution: **exit 2 / PENDING**, **30 available checks passed**, no failures. It explicitly lists 17 missing static inputs, 243 missing motion inputs, and the absent MP4. `independent_checks_pass`, continuous-observation, and perceptual-proof flags remain false.

**16 validator tests pass**, including timeline math, exact interpolation, malformed ordering, nonfinite/forbidden controls, blink-side inversion, brow/mouth geometry mutations, dimensions/mode guards, static-grid alignment, pending-without-native behavior, changed-freeze rejection, and failed receipts with missing frames. Test fixtures are isolated synthetic inputs, not native evidence. The full successful native/MP4 path is implemented but has not yet been exercised against EXP-123 captures.

Deliverables: this report, `review_validation.py`, `test_review_validation.py`, and `review_evidence/{review_checks.json,partial_review.json,validator_unit_tests.log}`. Candidate/probes, rig/runtime/shaders, source art, and frozen inputs were not modified.

## Intermediate checkpoint: concurrent launcher rewrite detected (resolved later)

The final hash check detected `native_launcher/project.godot` changed from `021475e8c28f882460ca070520dcdb7f2b1f5e3fe919aec354d9105ed99d5dfd` to `e319ef9543ecb2a3e4c6ae63d96c22cab1b212e93532b3f9519ed0127b18ac14` while this review was in progress. The exact original was reconstructed in memory from the frozen rig plus the documented launcher-only name/main-scene substitutions; its hash matches the frozen value.

The actual difference only moves the existing `[editor]` section ahead of `[rendering]` and changes blank-line formatting. No project setting value changed. This is consistent with an editor save, but the reviewer did not perform that save. `review_evidence/launcher_rewrite_review.json` preserves the exact diff and both hashes.

**Validator result at this intermediate checkpoint: exit 1 / FAIL**, specifically `reviewed_candidate_and_capture_inputs_unchanged`, with the same three pending native/video groups. Twenty-nine of the 30 available checks pass. This is an evidence-identity blocker, not a discovered expression or renderer defect. The parent must reconcile the observed project rewrite with an explicitly audited new freeze or restore the exact prepared identity before final evidence acceptance. The validator deliberately does not silently forgive the mismatch.

The source rig, candidate rig, art, candidate profile, static plan, and probes remain unchanged. The 16 unit tests passed before this concurrent rewrite; their successful log is retained, and the isolated pending-path test is expected to flag a changed fixture input until reconciliation. No native captures or MP4 existed at this final checkpoint.

## Resolution and subsequent native review

The parent confirmed the permitted Godot import caused the serialization-only change and directed an archived, exact config restoration after capture and editor exit. That restoration is complete, the original review-input freeze is unchanged, and final validation is **exit 0 / PASS with all 73 checks passing**. All 16 tests were rerun successfully after restoration. Native/decoded pixels were subsequently inspected; the limited skeptical/questioning read is visible, while the sideways/diagonal pout limitation remains. Continuous normal-speed observation and approval are still not claimed by this reviewer. See `INDEPENDENT_NATIVE_REVIEW.md` and `review_evidence/launcher_import_audit/restoration_receipt.json`.
