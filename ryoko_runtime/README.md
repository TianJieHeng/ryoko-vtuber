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
