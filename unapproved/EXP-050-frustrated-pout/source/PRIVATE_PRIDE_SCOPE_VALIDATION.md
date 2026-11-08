# EXP-152 Private pride: approved scope validation

Eight user-approved performances share one rig: EXP-163/005/001/006/107/007/002/152. EXP-002 is preserved from published commit 9b10e2f2c70f19fa003169502a73ee935af55480; EXP-152 includes the approved hidden-iris/down-gaze prerequisite. EXP-003/160/177 and new brow channels are excluded. See MERGED_PUBLICATION_VALIDATION.md for exact scope, source identities and focused merge checks. Earlier stage descriptions and frozen review receipts are historical.

## Source and acting interpretation

Exact catalogue 7693d1b8718c3bb1c717bd586fb472a7efc42403, v002 sheet SHA256 46d16e1eabfe7ea709252b0e3c47707613df3a8f6a41483e740981866ead6408. All 11 PNGs match Git bytes and all 9 panels are exact 418px integer crops. Proposed times 0/.15/.30/.50/.75/1.05/1.35/1.65/1.90 are interpreted as a new performance, not claimed to be an existing animation. Actual source pixels show a downward glance before a small closed smile, and mouth recovery before gaze recovery. Ordinary partial lids only; no smiling-eye closure or exhale. The shared 0.30-second entry blend is included in comparisons: at .15, gaze_y and extra each .25 yield 1.5 source pixels, not the raw key's 3 pixels. Peak 6 pixels comes from old gaze_y 1 plus extra 1. Shared release remains 0.45 seconds.

The source-specific small corner-up smile uses existing rigid lip controls. Head/body, hair, pupil scale, iris alpha, fixed UV, unit local scales, white enamel and 0.55 / 30.8px physical mouth limits remain exact. No performance artwork, runtime subclass, facial deformation, anatomy opacity blend, new FX, model, TTS or socket setup. The prerequisite's new hidden cap RGB is generated inferred support outside every protected old sampling texel, not original assembly pigment or a replacement iris/pupil/highlight.

## Complete current runtime checklist

Run Godot 4.6.3 headless with writable HOME/XDG and an imported isolated source copy. No listeners are started by these 21 suites:

- test_object_rig.gd
- test_yawn.gd
- test_teeth.gd
- test_expression_backbone.gd
- tests/test_auto_blink_lifecycle.gd
- tests/test_blush_controls.gd
- tests/test_closed_smile_contract.gd
- tests/test_corner_lift_runtime.gd
- tests/test_down_extra_runtime.gd
- tests/test_gaze_runtime.gd
- tests/test_giggle_runtime.gd
- tests/test_laughter_runtime.gd
- tests/test_oral_lift_contract.gd
- tests/test_private_pride_runtime.gd
- tests/test_purse_contract.gd
- tests/test_purse_transport.gd
- tests/test_reassurance_runtime.gd
- tests/test_relief_runtime.gd
- tests/test_smile_controls.gd
- tests/test_spread_runtime.gd
- tests/test_viewer_layout.gd

Existing suites receive only exact registry/fixture enumeration updates. Seven-prior-profile gaze defaults remain tested separately from 152's nonzero extension. Historical source guards follow an exact hash-pinned migration, not broad exclusions. tools/verify_private_pride_scope.py additionally protects every inherited runtime/art/config/profile byte and the exact capability inventory.

## Evidence and verification limits

Fresh deterministic Godot captures passed: two independent 168-tick launches at 30 fps, each with 90,238 assertions and full-bust/native views; 131 interruption/handoff/manual/release/retrigger lifecycle frames with 69,802 assertions; and 40 automatic-blink lifecycle frames with 2,890 assertions. The review MP4s contain two complete cycles, 5.6 seconds at 30 fps, including exact neutral at the end. Pixel receipts establish 336 matching view-frames between launches, 58 matching cycle ticks per view, all 18 restored blink phases identical to direct idle, and neutral/release/retrigger continuity. All 21 headless runtime suites passed 11,969,564 assertions (cumulative suite totals, not duplicate intermediate counters). All 18 source suites passed; source-check receipts identify their exact inputs and final documentation-only bridge. These external receipts accompany the scoped delta. Only sampled frames, state traces and framewise inspection support visual judgments. Normal-speed playback has not been observed. Real-socket tools/test_control_bridge.py is unrun. At review time there was no publication. No CI, paid resources, remote execution or hardware flashing is used for this approved publication.

Inherited capability evidence may be reused only for its exact frozen runtime/art/config, original six-profile inputs and unchanged state signatures. The old-domain harness enumerates the registry, so adding 152 changes a fresh default invocation; the archival 534 pairs are explicitly the old six-profile/input set, not a claim of a new seven-profile run. Fresh 152 trajectory/lifecycle pixels are required.


## Capture identity and inherited evidence

The immutable 478-file capture inventory is 7f8495bc06dc06534d70d9bf2d8f136f8ccb20788291ade5809a0edaa002405e. EXP-152 profile SHA256 is c336efc782732c73da3991fffad881e0c884425916c64a676608dd224c71117d. Final source may differ from that capture only in documentation, exact source-guard enumeration fixes and their integrity manifests. Runtime, artwork, configuration, profiles and render harnesses are byte-identical. The final source/capture bridge lists every changed path; neither frozen capability nor capture inputs are edited.

The 534 old-command paired renders and 390 new-domain samples are reused archival prerequisite evidence with pinned original control records and hashes, not freshly captured EXP-152 results. The old-domain default now sees eight registry entries; reuse is limited to its original six-profile inputs. Full-bust comparisons across different viewport widths are not claimed pixel-exact: the reviewer found one one-level blue-channel difference when comparing a 568px view with the left half of a prior 1136px view. Native neutral is exact to the capability baseline, and within-run full/native neutral returns are exact.

Final pose comparison selected ordinary peak lids 0.42 and a restrained corner lift 0.35, with no eye-smile or gape. At 1.35 seconds the mouth is exactly neutral while gaze remains 3.3 source pixels down; at 1.65 it remains 0.9 pixels down. Framewise review covers all 168 trajectory ticks and both cycles. No normal-speed observation was performed by the reviewer. The user has now approved EXP-002 and EXP-152 after preview; EXP-003 remains excluded.


The merged current checklist also includes `tests/test_affection_runtime.gd`, for22 runtime suites. Original21-suite results above are frozen152 evidence, not a fresh22-suite claim. Focused merged-source results are recorded in MERGED_PUBLICATION_VALIDATION.md.
