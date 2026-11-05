# Timed bust cue validation

User-approved update based on main `a04cbc82c443a1e1cbfb068155f82a5c2af043d9`, 2026-11-05. The user reviewed and approved the runtime video before publication.

## Tests

All 20 local Godot 4.6.3 suites passed: 132,041 counted assertions plus the existing bounce amplitude/settling suite. The added clip-channel suite passes 348 checks, covering typed/ranged loading, invalid replacement preservation, defensive copies, ordering, large frame skips, pause/resume, reset invalidation, selective cancellation, repeated cancellation, natural completion, replay, manual takeover, actual loopback UDP takeover, and the original demo.

- `AUDIO_MOUTH_CHECKS_PASS count=376`
- `INDEPENDENT_BODY_CHECKS_PASS count=534`
- `BOUNCE_CHECKS_PASS body_peak=14.8804968419234 chest_peak=7.58371686935425 settled=true`
- `BREATH_CHECKS_PASS count=15974 peak=0.99703496502315`
- `BROW_CHECKS_PASS count=7752`
- `CHEST_SECONDARY_CHECKS_PASS count=298 peak_source_pixels=3.06753778457642`
- `CLIP_CHANNELS_CHECKS_PASS count=348 failures=0`
- `CLIP_CHECKS_PASS count=45`
- `FACIAL_CONTROL_CHECKS_PASS count=89`
- `EXPRESSION_CONTROL_CHECKS_PASS count=58504`
- `EYELID_CHECKS_PASS count=120`
- `GAZE_CHECKS_PASS count=42103`
- `GESTURE_CHECKS_PASS count=256`
- `HAIR_SECONDARY_CHECKS_PASS count=289 head_peak=6.67058324813843`
- `INTEGRATED_BUST_CHECKS_PASS count=11`
- `LIVE_INPUT_CHECKS_PASS count=40`
- `LOOK_AT_CHECKS_PASS count=1107`
- `COUPLED_MOTION_RIG_CHECKS_PASS count=3204`
- `ORNAMENT_CHECKS_PASS count=826 driver_peak=0.08071931663141 rig_peak=0.06538102594081`
- `POSE_STORE_CHECKS_PASS count=165`

## Preserved inputs

All 606 PNG files are byte-identical to the approved integration. The original demo clip, live adapter, facial controller, shader and gaze/breath/brow/look/ornament drivers are unchanged. No new artwork, expression presets, animation amplitudes or full-body changes are included.

## Actual runtime evidence

The review MP4 is 27.033 seconds, 811 frames at 30 fps, 568 × 760. It is actual Godot OpenGL output, encoded by FFmpeg. The real clip player dispatches the included `demo_bust_clip.json`; it is not a hand-composited animation.

There are 109 logged state samples. All six paused samples have identical cue time, gaze, brows, breath, look, head and ornament angle. The log proves both ornament enabled states, breathing, both iris directions, independent brows, normal completion, replay, cancellation and reset. Final reset clears every new transient channel. No script or shader errors were emitted.

Chronological frames sampled at 2 fps and enlarged eye/brow crops were visually inspected. Features remain aligned, the pendant remains attached, the pause holds the character still, and the final state is neutral. Native-speed playback is unavailable to the assistant, so the user reviewed and approved temporal motion in the supplied video.

## Reproduction and limits

- Run every `test_*.gd` script using `godot --headless --path . --script res://<script>` after import.
- Run `review_clip_channels.gd` with Godot's OpenGL movie writer under a local graphics display for the review sequence.
- Shift+T plays the new example; T still plays the original demo. Call `play_clip("res://demo_bust_clip.json")` for the new one.
- Secondary-motion toggles remain persistent settings. Natural completion holds final values; explicit release cues define a neutral ending.
- No CI, paid resources or remote-machine execution was used. Git publication was authorized after runtime review.
