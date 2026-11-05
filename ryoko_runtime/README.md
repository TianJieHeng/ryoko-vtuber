# Approved lower side-lock motion

See [README_LOOSE_HAIR.md](README_LOOSE_HAIR.md) for independent outer hair-tip follow-through, X toggle, source-preservation checks and actual runtime review. The user reviewed and approved the runtime footage on 2026-11-05.

# Approved independent earrings

See [README_EARRINGS.md](README_EARRINGS.md) for restrained independent earring sway, Shift+F, derivative-art limits and actual runtime review. The user reviewed and approved the runtime footage on 2026-11-05.

# Approved timed bust controls

See [README_CLIP_CHANNELS.md](README_CLIP_CHANNELS.md) for new version-1 gaze, breath, brow, look-at and ornament cues. The user reviewed and approved the runtime video on 2026-11-05.

# Approved bust-rig integration

The user approved controlled breathing, independent neutral brows, coordinated look-at, and the hanging hairpin ornament on 2026-11-05. They are integrated here with the previously approved rigid-iris gaze and existing bust controls. Full-body work is not included.

- [Rigid iris gaze](README_GAZE.md): V toggles independent pointer gaze.
- [Controlled breathing](README_BREATH.md): I triggers one inhale/exhale.
- [Neutral brows](README_BROWS.md): O toggles brow raise.
- [Coordinated look-at](README_LOOK_AT.md): Y toggles eyes-first pointer attention.
- [Hairpin ornament](README_ORNAMENT.md): Shift+O toggles its secondary motion.
- [Live input](README_LIVE_INPUT.md): all new channels share the existing opt-in loopback adapter and timeout reset.

O and Shift+O are separate controls so brow and ornament toggles cannot fire together. Driver motion, artwork and limits retain the approved candidates. See VALIDATION_APPROVED_BUST.md for integration checks and scope.

# Rigid independent iris motion

See [README_GAZE.md](README_GAZE.md) for rigid iris translation, fixed clipping, reconstructed hidden eye regions and supported controls. This revision was reviewed and approved by the user.

# Local live input

See [README_LIVE_INPUT.md](README_LIVE_INPUT.md) for opt-in localhost UDP controls and timeout release. This revision was reviewed and approved by the user.

# Crown/bun motion

See [README_HAIR.md](README_HAIR.md) for bounded hair secondary motion. This revision was reviewed and approved by the user.

# Timed animation clips

See [README_CLIPS.md](README_CLIPS.md) for combined animation playback, pause and cancellation. This revision was reviewed and approved by the user.

# Pose presets

See [README_POSES.md](README_POSES.md) for saved head/body poses. This revision was reviewed and approved by the user.

# Independent eyelid controls

See [README_EYELIDS.md](README_EYELIDS.md) for screen-side winks and holds. This revision was reviewed and approved by the user.

# One-shot gestures

See [README_GESTURES.md](README_GESTURES.md) for gesture triggers and cancellation. This revision was reviewed and approved by the user.

# Whole-chest secondary motion

The user-approved bounce and broad chest follow-through are documented in [README_SECONDARY.md](README_SECONDARY.md). Existing head, body, audio, mouth and expression controls remain available.

# Independent torso controls

See [README_BODY.md](README_BODY.md) for the new separate head/body controls. This addition was reviewed and approved by the user.

# Live motion rig added

The default scene is now the interactive head/neck and coupled upper-torso rig. See [README_MOTION.md](README_MOTION.md) for controls, limits and validation. Original expression playback remains available as playback.tscn. The coupled-torso revision was approved and published in 48c976a. The approved audio-driven mouth controls are described in [README_AUDIO.md](README_AUDIO.md).

# Ryoko 93-expression runtime playback

Based on TianJieHeng/ryoko-vtuber phase31 at c752edde815eaab559d06cf43b7ae0784bf79e1c. Original artwork and registrations are unchanged.

## Run
Open project.godot in Godot 4.6 and run playback.tscn for eight highlights. For all expressions use:

    godot --path . res://playback.tscn -- --batch=1
    godot --path . res://playback.tscn -- --batch=2
    godot --path . res://playback.tscn -- --batch=3

Each batch covers 31 unique expressions for 3.6 seconds each. Every profile shows expression-rest, closed-eye blink, speech visemes, combined speech/blink, and restoration of its own emotion mouth. Small rigid cutout sway is added. Labels display the active expression and state. Capture uses Godot's movie writer with actual OpenGL rendering, then FFmpeg H.264 encoding, not static image compositing.

The underlying facial_controller.gd demo now derives its list from the registered expression map rather than a stale list of 72 IDs. Existing command methods are unchanged: set_expression(id), set_blink(left,right), set_mouth(viseme), release_speech(), and _handle_command(data).

## Scope
This is the approved layered bust/facial runtime. It uses discrete eye/mouth texture changes and small rigid whole-cutout motion. It does not implement mesh deformation, hair physics, full-body skeleton integration, microphone analysis, face tracking, or audio. Viseme timing is scripted demonstration, not speech-synchronized audio.

## Validation
89 baseline control checks and 58,504 expression control checks pass. Runtime loads all 93 profiles. Captured frames were decoded and inspected for open eyes, closed eyelids and speaking mouth. Complete batch logs record each expression and frame/time at its transition.

## Local checks

    godot --headless --path . -s test_controls.gd
    godot --headless --path . -s test_expressions.gd

Playback transition logs are written to Godot’s user data directory (`user://playback_<batch>.jsonl`). This standalone project does not require an adjacent output directory. Generated movie files and editor import caches are not committed.
