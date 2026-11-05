# Local live controls

User-approved revision based on approved main efee69d. The existing rig can now receive actual commands from a separate local program. This closes the live-input requirement in the original handoff for the controls already implemented in this bust rig; it does not add face tracking or claim the original full-body project is finished.

## Run

Start Godot with `godot --path . -- --live-input`. This explicitly enables UDP on **127.0.0.1:9122 only**. By default the port is not opened. No firewall or network setting is changed. Other programs on the same computer can send controls while enabled. No remote/LAN binding, file paths, credential handling or persistent writes are supported.

Send a JSON envelope with an increasing integer `seq` and `controls` object:

    python send_live.py --seq 1 '{"head_tilt":0.5,"body_tilt":-0.2,"mouth":"A"}'

Send updates more often than every two seconds. A two-second gap resets facial, head, torso and transient gesture controls and releases them to the local rig. A newer sequence resumes control. Sequence numbers remain monotonic for the lifetime of the running receiver; restart the rig to restart numbering. New live commands stop recorded clips so playback cannot overwrite the live source.

## Accepted controls

- `look_x`, `look_y`: finite numbers from -1 to 1; `look_release`: boolean.
- `ornament_secondary`: boolean; enables or disables the hanging hairpin cutout.

- `brow_raise`, `brow_screen_left`, `brow_screen_right`: finite numbers from -1 to 1, neutral brows only.

- `breath_level`, `breath_strength`: finite numbers from 0 to 1. `breath_trigger` and `breath_cancel`: booleans. See README_BREATH.md.

- `gaze_x`, `gaze_y`: finite numbers from -1 to 1; neutral-face eye direction.
- `head_tilt`, `head_x`, `head_y`, `body_tilt`, `body_x`, `body_y`: finite numbers from -1 to 1.
- `eye_screen_left`, `eye_screen_right`, `audio_level`, `blink`, `gesture_strength`: finite numbers from 0 to 1.
- `wink_duration`: 0 to 2 seconds, further limited by the existing eyelid driver.
- `reset`, `auto_blink`, `body_follow`, `release_eye_controls`, `gesture_cancel`, `audio_stop`, `speech_active`: booleans.
- `expression`: `neutral` or a registered expression ID.
- `mouth`: A/E/I/O/U/REST/RELEASE/neutral.
- `gesture`: acknowledge/greet. Send triggers once, not in every heartbeat.
- `wink`: screen_left/screen_right/both. Send triggers once.

Unknown keys, malformed envelopes, invalid types/ranges, duplicate/out-of-order sequences and datagrams over 4096 bytes are rejected before applying any controls. At most 32 packets are processed per frame. A bind failure is reported, not silently treated as live input. This is a local trusted-computer interface, not an authenticated network protocol.

## Evidence and limits

`test_live_input.gd` performs 40 checks including real UDP delivery, atomic validation, replay rejection, port collision, timeout neutral release and recovery. All 12 previous local suites also pass. The original live-input revision left the 594 artwork PNGs and deformation shader byte-identical. This integration retains all original artwork and extends the shader for the approved iris, breath, brow and ornament features.

The runtime review is an 18-second Godot recording. A **separate Python process** sends UDP head/body poses, mouth shapes, a held wink and a greeting. It then disconnects so the timeout release is visible. The recording harness observes render time only to pace commands; Godot applies the commands through the real socket. This proves local input, not webcam tracking or speech/phoneme recognition.

Full-body/registered arm-gesture integration remains outside this approved bust rig. Rigid clipped gaze, neutral brow controls and the hanging hairpin ornament are now integrated. Earrings and necklace remain unrigged. Existing expression presets are not new expression artwork.

Visually reviewed and approved by the user before publication. Video review uses decoded chronological frames; native-speed playback is not available here.

