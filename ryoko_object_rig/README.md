# Ryoko shared expression rig

One assembled separate-part character, one bounded performance controller, and data-only expression definitions. The default Godot application shows **one rig**. Only EXP-163 (Yawn) is authored and registered; the old expression catalogue and emotion sheets are references, not implemented performances.

## Run

Open `project.godot` in Godot 4.6.3 and run. Select the registered performance and press Play (P), Release (Space), or Reset (0). Sliders provide bounded manual controls. Manual input takes ownership and cancels active playback/release. The optional auto-blink is a manual-mode closure floor.

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

- `object_face.gd`, `object_rig.gd`, shaders and native artwork: existing separate-part assembly, unchanged by the backbone migration.
- `expression_registry.gd` and `expressions/registry.json`: transactional validation and supported-ID discovery.
- `expression_rig.gd/.tscn`: one timeline sampler/player, control validator and ownership lifecycle.
- `expression_viewer.gd/.tscn`: one-rig app using that public API.
- `control_bridge.gd` and `strict_control_json.gd`: optional bounded loopback adapter to the very same rig, not another controller.
- `yawn_performance.json`: unchanged 13-key, 5.8-second approved yawn data, registered as EXP-163 with alias `yawn`.
- `yawn_rig.gd`: only legacy names, labels and the Y shortcut. It delegates sampling, playback, validation and ownership to the generic player.

Future performances add validated JSON plus a registry entry. They do not add a controller subclass or a new application. See `CONTROL_API.md` for the shared callable contract and schema.

## Preserved appearance and motion

The native 1136×1384 approved bust supplies the visible head, face, nose, jaw, neck, hair, eyes and brows. Only fixed whole-rig presentation transforms are used. Independent moving owners retain unit local scale and full opacity.

Existing parts include four rigid hair regions with seam guards; independent brows; upper lashes, lower contours, irises, sclerae and closed lashes; fuller neutral lips; and continuous cavity, upper/lower lips, upper/lower teeth, tongue and static underlip shadow. Foreground hair ownership and the stationary connected neck/body remain intact.

Normalized `mouth_open` 0–1 maps to physical aperture 0–0.55: at most 30.8 source-pixel cavity height and 29.7-pixel lower-lip travel. Upper teeth stay attached at (533,626). White tooth derivatives, all other artwork and the yawn values/timing are unchanged.

There is no face/UV warp, animated feature scale, full-face patch or emotion opacity crossfade. Interpolation changes control coordinates, not image opacity.

## Honest limits

- Nonzero gaze is rejected until hidden iris/sclera travel pixels are verified.
- Hair is limited to ±0.07; wider travel needs additional hidden artwork.
- Non-neutral A/E/I/O/U and their viseme aliases are rejected by the public app/controller. The historical lower-level `object_rig` still exposes them for compatibility diagnostics and is **not** a safe app/AI entry point.
- Earrings remain static. Full-body motion, additional expressions, lip-sync/phoneme authoring and AI-model/voice-service integration are not implemented. An opt-in local external-process control bridge is available; it does not itself connect a model or TTS provider.
- Flattened-source crossings contain the existing documented hidden-skin, hair-seam and continuation estimates. They are not claimed to be original clean artwork.

## Verification

Python dependencies are in `requirements.txt`. A source-only package may omit generated diagnostic intermediates; run the full builder before source identity tests:

    python tools/build_object_face.py
    python tools/verify_object_base.py
    python tools/verify_yawn.py
    python tools/verify_teeth.py
    godot --headless --path . --editor --quit
    godot --headless --path . --script res://test_object_rig.gd
    godot --headless --path . --script res://test_yawn.gd
    godot --headless --path . --script res://test_teeth.gd
    godot --headless --path . --script res://test_expression_backbone.gd
    python tools/test_control_bridge.py --output /tmp/ryoko-bridge-evidence

`BACKBONE_VALIDATION.md` distinguishes current backbone results from inherited historical mouth/art reports. `tools/capture_backbone_parity.sh`, `tools/review_backbone_parity.gd` and `tools/compare_backbone_parity.py` provide actual-render comparison against an isolated approved baseline. Generated captures and caches belong outside source.
