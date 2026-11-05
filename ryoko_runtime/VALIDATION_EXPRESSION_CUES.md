# Timed existing-expression cue validation

Approved update based on main `40c4e4e71e054da6ea419286cb807c9267b1a561`, tested 2026-11-05. The user approved the actual runtime review on 2026-11-05 before publication.

## Scope and preservation

The version-1 clip player now accepts a validated `expression` string selecting neutral or any of the existing 93 registered expressions. Loading an invalid clip preserves the active or paused clip and rig state. Comma/period cycling takes over playback from the actually selected expression; valid live UDP input keeps its existing priority. Pause/resume, cancellation, reset invalidation, legacy clips and natural completion semantics are retained.

All 622 inherited PNGs, expression registration, old demo clips, shader, facial controller and individual drivers are SHA-256-identical to the approved baseline. Only the clip player, MotionRig integration and relevant documentation change among inherited files. No artwork, expressions, driver amplitudes, full-body work, CI, paid resources or remote-machine execution is included.

## Automated checks

All 24 local Godot 4.6.3 suites passed: 167,923 counted checks plus the existing bounce amplitude/settling suite. The new expression-cue suite passes 3,951 checks. It covers all 93 registered IDs, invalid types/names/paths, late invalid-cue replacement atomicity, defensive copies, time-zero/same-time/large-frame dispatch, pause/resume, natural completion, replay, same-frame reset invalidation, direct paused selection, key release/repeat handling, active/paused keyboard takeover, repeated cancellation, blink/speech independence, real loopback UDP takeover and timeout, and both legacy demos.

Independent code review found no concrete correctness regression. No script errors or failed checks were emitted.

## Actual runtime review

`review_expression_cues.gd` plays the real `demo_expression_clip.json` through MotionRig, pauses and resumes it, completes it, replays it, uses the expression-cycle key to take over, then resets. The recording is actual Godot OpenGL movie-writer output, not hand-composited animation.

- Full view: 568 by 760, 931 frames, 31.033 seconds at 30 fps.
- Face detail: 1040 by 720, cropped and enlarged from the same recording; no extra visual detail is invented.
- 125 logged state samples validate the selected expression and matching gaze profile, supported independent winks and mouth shapes, unsupported authored-gaze fallback, completion, replay, takeover and reset.
- All six paused state samples hold the same cue time, expression and gaze. The decoded source AVI frames at 6.0 and 6.5 seconds are pixel-identical, including the character and labels. The compressed MP4 can show tiny encoding differences between those still frames.
- 62 chronological full frames and matching face close-ups were visually inspected. The existing facial features and accessories remain aligned, and reset restores the neutral expression. The inherited breathing oscillator continues, so initial and final full-bust pixels need not be identical.

The record shows neutral, EXP-064, EXP-041, EXP-189 and EXP-067 (the manual takeover). EXP-064 and EXP-189 use their previously approved iris profiles; EXP-041 and EXP-067 retain authored gaze. Speech uses silent mouth-shape cues, not synthesized audio or phoneme detection.

## Reproduction and limits

Run every `test_*.gd` with `godot --headless --path . --script res://<script>` after import. Run `review_expression_cues.gd` with Godot's OpenGL movie writer at 30 fps under a local graphics display, then encode the AVI with FFmpeg. Call `play_clip("res://demo_expression_clip.json")` for the new example; existing T and Shift+T shortcuts remain unchanged.

Native-speed playback is unavailable to the assistant. The 31-second movie took 2 minutes 37 seconds to render (19% real-time speed), so it does not establish live performance. The user reviewed and approved the supplied video. Hardware performance and face tracking remain unverified. Git publication followed user approval.
