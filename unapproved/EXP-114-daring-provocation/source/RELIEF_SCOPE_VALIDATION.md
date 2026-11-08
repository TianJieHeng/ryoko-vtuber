# Scoped EXP-007 relieved smile

User-approved release on exact approved parent `35a7ddc615e7501a9a814ca02d722ddb40f200c9`, project tree `a2d6c440b73f0a241d73b7bb50c3028fa7ef385c`. No new artwork. Runtime/shader changes add only the generic rigid purse channel. One shared registry/player/app, six data-defined performances. All 182 PNGs and five prior profiles are byte-identical.

## Reference and interpretation

Original source commit `7693d1b8718c3bb1c717bd586fb472a7efc42403`, path `avatar_build_assets/reference_library/assets/expressions/EXP-007_relieved-smile/RYO_EXP-007_relieved-smile_sheet_v001.png`, SHA256 `906ddfe017b15ad415d3ffc44ec930cab6ebf8c377da970259a1125bfb9bf2ad`. All nine panel hashes and exact integer crops are independently verified. KP05 is the published peak. This is relieved smile, not teasing grin.

Nine keys at 0, .25, .55, .90, 1.30, 1.65, 2.10, 2.65 and 3.20 seconds preserve source pose order: neutral, raised-inner-end worried tension, parted exhale, exhale release, open relieved smile, closed follow-through, lingering smile, settle, neutral. This is a new 3.2-second timing interpretation. The catalogue's 1.9-second timing is explicitly proposed reference timing, not existing animation.

Eyes remain open with at most .09 ordinary lid closure. Laugh-eye shape, gaze, hair and blush channels remain zero. Rigid brow rotation approximates the reference's upward inner hook; it cannot repaint curvature. Existing canonical lips approximate the upper-lip bow. No head, shoulders, chest, hand or BOD-037 body acting is performed. No new expression texture, anatomy opacity crossfade, UV/mesh deformation, scale animation or inferred art is introduced. Fixed head/neck width and registration and central white enamel at (533,626) remain. Public mouth_open is 0–1 with physical multiplier .55 and per-column aperture at most 30.8 source pixels.

## Reusable purse mechanism

Original assembly O and U images were inspected as contour references only. They contain flattened mouth anatomy and are not used as replacement sprites. The existing approved lip pigment supplies independent upper/lower strips and corner owners. Purse translates them inward and rotates them into a smaller rounded aperture; fixed native UV and unit scale are retained. Current and zero-purse neighbor boundary lines let each strip clip only additional geometric overlap. Oriented normal-distance comparisons divide by the fixed edge length rather than its vertical span, so clipping stays finite when an extreme manual pose makes a boundary horizontal or reverses its direction. Shared mouth, enamel, continuation and pressure shaders use the same bounded purse contour. Existing independent cavity, white enamel and oral surface remain separate. No new PNG is introduced.

The v6 authored keys prepare lip pressure while still closed, then use moderate purse .72/.62 for KP03/04 before returning purse to zero for the broader smile. This avoids substituting an open smile for the defining exhale. Larger manual purse at closed mouth intentionally forms a pursed/downturned contour and is not authored as a new expression.

## Reproducible checks

Clean-source Python checks: `verify_relief_scope.py`, `verify_reassurance_scope.py`, `verify_giggle_scope.py`, `verify_welcome_scope.py`, `verify_closed_smile_support.py`, `verify_blush_source.py`, and `sha256sum -c SOURCE_FILES.sha256`. Run builders and source-art checks only in a separate rebuild copy: build_object_face, verify_object_base, verify_yawn, verify_teeth, verify_gaze_assets, verify_gaze_coverage, verify_lid_handoff, verify_smile_support, verify_spread_support, verify_closed_smile_support and verify_blush_source.

Godot 4.6.3 headless import and all eighteen runtime suites: four top-level tests (object rig, yawn, teeth, expression backbone), plus gaze, viewer layout, smile controls, laughter, spread, giggle, corner lift, closed smile, blush, oral lift, reassurance, relief, purse transport and purse geometry contract tests. Use writable HOME/XDG. Final-source execution results are recorded separately from historical receipts.

Real-render evidence uses the existing supported graphical desktop, Compatibility OpenGL/Mesa, two complete 30-fps cycles, a repeated independent capture, native and full-bust views, and exact reference comparisons. Rendering tests rewrite controls after presentation-scale changes. All five prior profiles and gaze require old-state and actual-pixel parity. Runtime lifecycle checks include completion, interruption, retrigger, release, reset, manual takeover and incoming laughing-eye restoration.

Auto-blink behavior is inherited intentionally: performance/release disables it and does not silently restore it on completion; reset leaves it disabled. The manual control can re-enable it. Incoming visible auto-blink closure must be continuous at trigger. No new auto-blink restoration promise is made.

## Limits

No actual AI/TTS connection or tracking. The local bridge is preparation only. Sandbox socket restrictions prevent fresh real-process transport validation; source/callable checks only. Normal-speed audiovisual playback is not claimed without a specific receipt. Existing faint fringe traces under nonzero manual hair_sway are inherited; EXP-007 authors zero sway. The rig is not claimed artifact-free. Canonical source style differs from the reference, and the rigid brow hook / upper-lip bow remain approximations. EXP-007 is user-approved for publication. Current status is recorded in `RELEASE.json`; frozen review receipts retain their pre-approval wording. Publication changes only live documentation and release metadata, plus their inventory hashes.
