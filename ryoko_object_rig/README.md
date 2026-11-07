# Ryoko shared expression rig

One assembled separate-part character, one bounded performance controller, and data-only expression definitions. The default Godot application shows **one rig**. EXP-163 (Yawn), EXP-005 (Hearty laughter), EXP-001 (Bright welcome), EXP-006 (Suppressed giggle), EXP-107 (Confident reassurance), EXP-007 (Relieved smile), and EXP-002 (Affectionate warmth) are authored and registered. All seven are user-approved for publication; the old expression catalogue and emotion sheets are references, not implemented performances.

## Run

Open `project.godot` in Godot 4.6.3 and run. Select the registered performance and press Play (P), Release (Space), or Reset (0). Sliders provide bounded manual controls. Manual input takes ownership and cancels active playback/release. The optional auto-blink defaults off. When enabled, it pauses during performances and resumes after exact neutral recovery. The viewer reports actual activity separately from the saved preference; changing it is manual takeover. See AUTO_BLINK_VALIDATION.md for this independently reviewed focused correction and its verification limits.

`expression_viewer.tscn` is the default app. `yawn_stage.tscn` is a separate legacy three-view review scene, not another runtime architecture. It delegates to the same player through a thin compatibility wrapper.

## Local external control

To let a separate local process control this same rig, launch with
`godot --path . -- --control-port=18163`, then run
`python tools/ryoko_control_client.py --port 18163 --demo` in another terminal.
The bridge is off by default and binds only 127.0.0.1. Manual UI actions revoke
external writes until explicitly re-enabled. See `LOCAL_CONTROL_BRIDGE.md` for
the exact protocol, trust boundary, lifecycle, error handling and real-process tests.
No AI model or TTS service is connected by this phase.

## Architecture

- `object_face.gd`, `object_rig.gd`, shaders and native artwork: separate-part assembly; the backbone migration preserved it and the later bounded-gaze phase adds explicit derived eye owners.
- `expression_registry.gd` and `expressions/registry.json`: transactional validation and supported-ID discovery.
- `expression_rig.gd/.tscn`: one timeline sampler/player, control validator and ownership lifecycle.
- `expression_viewer.gd/.tscn`: one-rig app using that public API.
- `control_bridge.gd` and `strict_control_json.gd`: optional bounded loopback adapter to the very same rig, not another controller.
- `yawn_performance.json`: unchanged 13-key, 5.8-second yawn data, registered as EXP-163 with alias `yawn`.
- `expressions/EXP-005.json`: the 15-key, 5.4-second hearty-laughter performance, using generic smile-eye/lip channels and the existing player. See `SMILE_VALIDATION.md` for the historical laughter review.
- `expressions/EXP-001.json`: the approved nine-key, 3.0-second bright welcome. Separate rigid lateral lip/oral owners broaden the smile. See `WELCOME_SCOPE_VALIDATION.md`.
- `expressions/EXP-006.json`: a 13-key, 2.8-second pressed smile, small escaped laugh and re-press. Two closed-smile controls and separately registered original cheek-blush FX use the same shared controller. Published and user-approved at `4f3deaa2de3eedb691a9f0c795c7b8563663e472`. See `GIGGLE_SCOPE_VALIDATION.md`.
- `expressions/EXP-002.json`: nine-key, 1.9-second affectionate warmth with one brief smiling closure, renewed eye contact and a lingering sealed smile. User-approved for publication. See `AFFECTION_SCOPE_VALIDATION.md`.
- `source_references/expression_catalogue_93.json`: preserves all 93 historical IDs as references; only the seven actual authored performances are playable.
- `yawn_rig.gd`: only legacy names, labels and the Y shortcut. It delegates sampling, playback, validation and ownership to the generic player.

Future performances add validated JSON plus a registry entry. Any missing movement capability must be implemented generically with separate rigid owners; performances do not add a controller subclass or a new application. See `CONTROL_API.md` for the shared callable contract and schema.

## Preserved appearance and motion

The native 1136×1384 approved bust supplies the visible head, face, nose, jaw, neck, hair, eyes and brows. Only fixed whole-rig presentation transforms are used. Independent moving owners retain unit local scale and full opacity.

Existing parts include four rigid hair regions with seam guards; independent brows; upper lashes, lower contours, irises, sclerae and closed lashes; fuller neutral lips; and continuous cavity, upper/lower lips, upper/lower teeth, tongue and static underlip shadow. Foreground hair ownership and the stationary connected neck/body remain intact.

Normalized `mouth_open` 0–1 maps to physical aperture 0–0.55: at most 30.8 source-pixel cavity height and 29.7-pixel lower-lip travel. Upper teeth stay attached at (533,626). This EXP-002 extension preserves all 182 parent PNGs and all six approved performance definitions byte-for-byte. The historical lateral-mouth extension added seventeen source-derived PNGs for separate cavity, posterior enamel, tongue and explicitly inferred joint-underlap support. The fixed central white teeth remain unchanged.

There is no face/UV warp, animated feature scale, full-face patch or emotion opacity crossfade. Interpolation changes control coordinates, not image opacity.

## Honest limits

- Local candidate gaze is normalized to [-1,1] per axis, calibrated to left/right 4 source pixels, up 2 and down 1. Wider travel is rejected. See GAZE_VALIDATION.md for inferred eye artwork, ownership corrections and measured neutral/yawn differences. Historical candidate measurements are preserved there; this package keeps the approved laughter predecessor eye path unchanged.
- Hair is limited to ±0.07; wider travel needs additional hidden artwork.
- Non-neutral A/E/I/O/U and their viseme aliases are rejected by the public app/controller. The historical lower-level `object_rig` still exposes them for compatibility diagnostics and is **not** a safe app/AI entry point.
- Earrings remain static. Full-body motion, the other historical catalogue expressions, lip-sync/phoneme authoring and AI-model/voice-service integration are not implemented. An opt-in local external-process control bridge is available; it does not itself connect a model or TTS provider.
- Flattened-source crossings contain the existing documented hidden-skin, hair-seam and continuation estimates. They are not claimed to be original clean artwork.

## Verification

The complete current 20-suite runtime and clean-source checklist is in AFFECTION_SCOPE_VALIDATION.md. RELIEF_SCOPE_VALIDATION.md retains the historical EXP-007 scope. Run diagnostic builders only in an isolated copy, preserving the clean source inventory. Real socket transport has not been rerun under the current restrictions.

Python dependencies are in `requirements.txt`. A source-only package may omit generated diagnostic intermediates; run the full builder before source identity tests:

    python tools/build_object_face.py
    python tools/verify_object_base.py
    python tools/verify_yawn.py
    python tools/verify_teeth.py
    python tools/verify_gaze_assets.py
    python tools/verify_gaze_coverage.py
    python tools/verify_lid_handoff.py
    python tools/build_smile_support.py
    python tools/verify_smile_support.py
    godot --headless --path . --editor --quit
    godot --headless --path . --script res://test_object_rig.gd
    godot --headless --path . --script res://test_yawn.gd
    godot --headless --path . --script res://test_teeth.gd
    godot --headless --path . --script res://test_expression_backbone.gd
    godot --headless --path . --script res://tests/test_gaze_runtime.gd
    godot --headless --path . --script res://tests/test_viewer_layout.gd
    godot --headless --path . --script res://tests/test_smile_controls.gd
    godot --headless --path . --script res://tests/test_laughter_runtime.gd
    python tools/verify_spread_support.py
    python tools/verify_welcome_scope.py
    godot --headless --path . --script res://tests/test_spread_runtime.gd
    python tools/test_control_bridge.py --output /tmp/ryoko-bridge-evidence

`BACKBONE_VALIDATION.md` distinguishes current backbone results from inherited historical mouth/art reports. `tools/capture_backbone_parity.sh`, `tools/review_backbone_parity.gd` and `tools/compare_backbone_parity.py` provide actual-render comparison against an isolated approved baseline. Generated captures and caches belong outside source.

## Preserved EXP-005 review history

The approved laugh is a complete authored performance on the same rig, not a new controller or expression-specific project. Its smiling lips include explicitly inferred hidden joint material. Source images being unchanged does not imply the rendered ownership corrections are unchanged. The ordinary-lid shader also incorporates the separately reviewed F handoff correction. Read `SMILE_VALIDATION.md` for exact scope, inference, measured differences and playback limits. The exact approved laughter predecessor was published at commit `6a61452e29ffbfcd4f7c5afe9b728b367f145f3e`. Historical candidate receipts remain unchanged.

The focused ordinary near-closed lash correction is preserved in LID_HANDOFF_CORRECTION.md. Its shader, source assets and filtering tests remain protected alongside the new shared smile additions.

## Historical scoped welcome publication

This source adds only EXP-001 and its required lateral-mouth support to the exact approved laughter predecessor. Wide-eye support, held EXP-003/006/007 profiles, closed-smile pressing and oral lift are excluded. Historical receipts remain historical evidence, not proof of this package’s render parity. See `WELCOME_SCOPE_VALIDATION.md` for newly executed checks, exact approved welcome rendering and disclosed predecessor mouth-edge changes.

## Historical scoped EXP-006 publication

This extension is based on the published EXP-001 source at `69e74ce5049a13ad5aa33014cacb1287f494787a`. All 174 parent PNGs and the three existing performance definitions remain byte-identical. Rigid closed-smile corner curvature and inferred inner-upper-lip pressure add only the required mouth support. The original separate left/right blush FX are registered as fixed cheek-only effect objects under foreground hair. Their bounded intensity is independent of facial geometry and facial-object opacity.

The exact EXP-006 static reference is interpreted with authored timing. Painted brow curvature, fine reference hatch density and body/hand acting are not reproduced; the source FX have their original three strokes. This is a reference-matched separate-object performance, not a pixel-identical repaint. Wide-eye and oral-lift capabilities, held EXP-003/007, and AI/TTS integration remain excluded. The original no-blush EXP-006 profile is retained as a timing/control fixture, not another playable entry.

## Published EXP-107 extension

This extension starts from the exact approved EXP-006 commit `4f3deaa2de3eedb691a9f0c795c7b8563663e472`. It preserves all 182 PNGs and four prior profiles byte-for-byte, adds no artwork, and introduces only the shared normalized `mouth_oral_lift` channel. EXP-107 uses eleven keys across 3.0 seconds: a closed reassuring smile, one modest open accent, a closed lingering smile and neutral return. Direct gaze, fixed head/body/hair and separate rigid owners remain unchanged.

The exact nine-panel source sheet, panel hashes and proposed reference timing are documented in `source_references/EXP-107_reference_metadata.json`. The reference is not a pixel-identical target for the different approved canonical artwork. See `REASSURANCE_SCOPE_VALIDATION.md` for the complete scope, current verification and honest limits. Earlier scope sections and receipts describe historical stages, not current exclusions.

Run `python tools/verify_reassurance_scope.py`, the two historical scoped guards and the applicable runtime suites in `REASSURANCE_SCOPE_VALIDATION.md`. Source diagnostics must be rebuilt only in an isolated copy.

## Approved EXP-007 extension

This expression and generic rigid-purse extension starts from approved EXP-107 commit `35a7ddc615e7501a9a814ca02d722ddb40f200c9`. It preserves all 182 PNGs and five prior profiles byte-for-byte. A generic bounded mouth_purse channel adds inward rigid lip articulation through the existing shared controller, viewer and preparation-only bridge. It adds no artwork. EXP-007 is relieved smile, not teasing grin: inward worried tension, parted exhale, open smile, closed lingering smile and exact neutral.

The new nine-key 3.2-second timeline interprets the original static sheet, whose 1.9-second timing was a proposal. Slight ordinary-lid lowering keeps eyes open; no laughing-eye substitution or additional FX. Fixed canonical artwork means the brow hook and upper-lip bow are approximations. The reference's BOD-037 shoulder/hand action is excluded. See `RELIEF_SCOPE_VALIDATION.md` and exact source metadata in `source_references/EXP-007_reference_metadata.json`. EXP-007 is user-approved for publication. `RELEASE.json` records current approval status. Frozen review receipts and descriptive profile metadata retain their historical wording; the reviewed runtime, artwork, profile values and timing are unchanged.


## EXP-002 affectionate warmth: approved publication

This candidate adds only EXP-002 to the same shared application and registry. The six published profiles and all runtime code, shaders and artwork remain byte-identical to approved commit `8c349e29fb1e742231918260d7db56026492a6c9`. EXP-003 is not included. See `AFFECTION_SCOPE_VALIDATION.md` for exact v001 source, original proposed timing, source-pixel interpretation, rigid-object constraints and test coverage.

The smile develops with eyes near canonical neutral; one brief upward smiling closure is followed by renewed eye contact and a lingering sealed smile. Auto-blink inherits published restoration semantics, including initially-off behavior and cancellation by manual takeover, disable or reset. `RELEASE.json` describes this approved publication; `source_references/affection_predecessor_RELEASE.json` preserves the published predecessor record. The user approved publication after viewing the preview. The primary cumulative archive remains version 19.
