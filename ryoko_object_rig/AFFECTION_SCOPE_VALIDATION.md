# Scoped EXP-002 affectionate warmth

User-approved publication on exact approved parent `8c349e29fb1e742231918260d7db56026492a6c9`, project tree `f22619f290309fb37ad47c459efec4c1a1b5cba2`. One shared registry/player/application, seven data-only performances. All 450 parent paths remain; all 182 PNGs, six prior profiles, runtime assembly/player/viewer/bridge code and shaders are byte-identical. EXP-003 is not included. The parent contains the published auto-blink preference restoration; this expression delta does not alter it.

## Exact reference and interpretation

Original catalogue commit `7693d1b8718c3bb1c717bd586fb472a7efc42403`, exact path `avatar_build_assets/reference_library/assets/expressions/EXP-002_affectionate-warmth/RYO_EXP-002_affectionate-warmth_sheet_v001.png`, SHA256 `76ab1be9b8e3dc12447dd9045e9356452da12182be70700b5f06eac2faff9efd`, native1254x1254. All nine independently retrieved panels match their metadata hashes and are pixel-exact integer crops of the sheet. KP05 is the published peak byte-copy. Full expression metadata is retained verbatim as parsed JSON in `source_references/EXP-002_reference_metadata.json`. The original complete metadata file at that commit has SHA256 `ded1b313c36b66daf46f3426288ef4670b04703497323314754bba18e872b2bf`.

Actual pixels guide acting: inner brows soften, a small sealed smile develops while eyes remain near canonical neutral at KP4. KP5 briefly closes into an upward smiling contour. KP6 already renews open eye contact while retaining the smile. KP7 and KP8 retain a decreasing smile before exact neutral. Generic metadata says a .3-second peak hold; that does not override the visibly reopened eyes at KP6. The smile remains near peak during reopening. This must not inherit EXP-003's closed KP6 or EXP-007's exhale/purse.

The nine keys use the source-proposed [0,.15,.30,.50,.75,1.05,1.35,1.65,1.90] seconds. These are explicitly proposed reference times, not recovered animation; rig weights are newly authored. Existing smiling-eye owners reach .90 only at KP5. Open KP4 and KP6 use .015 and .010, respectively, equivalent to3%/2% ordinary closure, so renewed eye contact remains near this canonical artwork's neutral opening. The source artwork's eye shape differs from the canonical rig; no wide-eye capability is invented. Closed smile uses mouth_smile .24 and mouth_corner_lift .60 at KP4/5/6, with softer onset and lingering tail. Eyebrows use small symmetric translation and mirrored inward tilt. All other mouth channels, gaze, hair and blush stay zero. No effects are specified or visible.

## Rig constraints and honest limits

Anatomy remains separate rigid artwork with fixed source pigment/UV, unit local scales and full anatomical opacity. Continuous interpolation changes owner coordinates, not anatomical opacity. Spatial clipping and fixed paint are unchanged. No flattened face/expression patch, mesh deformation or texture swap is introduced. Canonical face width, head/neck registration, white enamel at (533,626), and foreground hair stay protected. The general mouth cap remains normalized0–1 with physical multiplier.55 and30.8 source-pixel maximum, although this profile stays sealed.

The inherited eye path has two stages: ordinary closure, then upward rigid articulation. The thin downward ordinary contour appears briefly on both sides of the smiling closure; it is a transition, not the intended affectionate target. Dense20ms diagnostics and every30Hz final frame cover this trajectory. Partial-open softness uses the ordinary-lid family rather than a separately raised lower lid. The fixed canonical brow/lash/lip pigment does not reproduce the differently drawn reference pixel-for-pixel. No body/hand BOD-016/BOD-026 accompaniment, head acting, face tracking, real AI/model/TTS connection or live socket integration is implemented.

## Lifecycle and control verification

Auto-blink inherits the published state machine: enabled intent is suspended during playback/release and restored only after exact open neutral, restarting the ordinary idle clock. Initially-off remains off. Manual takeover, explicit disable and reset cancel pending intent. Three shared player/viewer/bridge runtime files are byte-identical to the published parent. Extended tests include selected002 peak and openKP6, completion/release/retrigger, incoming/outgoing prior-profile handoffs, interrupted recovery, initially-on/off, UI signal cancellation, ordinary closed/reopened idle blinking and later triggers after cancellation.

Run `python tools/verify_affection_scope.py`, historical strict scope guards, closed-smile support, blush source and `sha256sum -c SOURCE_FILES.sha256` on clean source. Migration guards permit only exact chained hashes, not broad file exceptions. Rebuild in an isolated copy: object face and smile support, then object/yawn/teeth/gaze assets/gaze coverage/lid handoff/smile/spread/closed-smile/blush verification. Use writable HOME/XDG for headless Godot4.6.3 import. Run the18 inherited runtime/control suites, extended auto-blink lifecycle, and `tests/test_affection_runtime.gd` (20 suites).

Final evidence includes actual-Godot full-bust and native-face renders of two complete cycles, a second independent render launch, source-key comparison, complete30Hz trajectory contacts, lifecycle/interrupt/retrigger/reset/manual/family-handoff images, exact neutral and source/rig invariants. Baseline prior-profile/gaze pixel caches may be reused only after independently verifying source/harness/plan/renderer/image identities and fresh candidate state equivalence. Reused prior evidence must be labeled; it is not a new baseline capture. Refresh controls after presentation transforms so clipping uniforms stay aligned.

No normal-speed visual playback is claimed. Opening a player is not motion observation. Real socket transport remains unrun. Independent review and captured-pixel receipts are external to frozen source to avoid circular identity. Local tests alone did not authorize publication. The user subsequently viewed the preview and approved publication; frozen review receipts retain their historical pre-approval wording. Media and diagnostics are not committed. The cumulative primary archive stays at version19.


## Complete current runtime checklist

Import the project first with `godot --headless --path . --editor --quit` using writable HOME/XDG directories. Then run every script below with `godot --headless --path . --script res://PATH`. All 20 are required; socket transport is deliberately separate and unrun.

- `test_object_rig.gd`
- `test_yawn.gd`
- `test_teeth.gd`
- `test_expression_backbone.gd`
- `tests/test_gaze_runtime.gd`
- `tests/test_viewer_layout.gd`
- `tests/test_smile_controls.gd`
- `tests/test_laughter_runtime.gd`
- `tests/test_spread_runtime.gd`
- `tests/test_giggle_runtime.gd`
- `tests/test_corner_lift_runtime.gd`
- `tests/test_closed_smile_contract.gd`
- `tests/test_blush_controls.gd`
- `tests/test_oral_lift_contract.gd`
- `tests/test_reassurance_runtime.gd`
- `tests/test_purse_transport.gd`
- `tests/test_relief_runtime.gd`
- `tests/test_purse_contract.gd`
- `tests/test_auto_blink_lifecycle.gd`
- `tests/test_affection_runtime.gd`
