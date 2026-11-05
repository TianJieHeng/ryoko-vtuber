# Approved timed existing-expression cues

Built on approved main `40c4e4e71e054da6ea419286cb807c9267b1a561`. This closes a scheduling gap: a clip can now select already-approved expressions instead of requiring a manually selected face before playback. No new expressions, artwork, deformations or driver amplitudes are produced. All 622 inherited PNGs and the expression registration remain unchanged.

The user approved the actual Godot runtime review on 2026-11-05 before publication.

## Format and use

Existing version-1 clips may now include an `expression` string in a cue's `controls`. It must be `neutral` or an exact ID in the project's registered expression collection. Unknown IDs, paths and non-string values reject the entire clip before it replaces a playing or paused clip. The previous clip and current rig remain intact on failed loading.

```json
{"time": 1.0, "controls": {"expression": "EXP-064", "gaze_x": -0.7, "mouth": "E"}}
```

Call `play_clip("res://demo_expression_clip.json")` on the existing MotionRig API to run the included 17-second example. T and Shift+T keep their existing examples and keyboard behavior; this revision adds no extra shortcut.

The example selects neutral, EXP-064, EXP-041, EXP-189 and neutral again. It combines the existing gaze, blink, speech-mouth, head and attention controls. EXP-064 and EXP-189 use their approved independent iris profiles; unsupported expressions retain authored gaze. It uses silent mouth cues, not synthesized speech or phoneme detection.

## Playback and ownership

- Pausing freezes the cue clock and rig simulation. Resuming continues once from the held cue position.
- Same-time cues retain source order. Slow frames apply crossed cues once. Reset invalidates later queued cues, including those with the same timestamp.
- Natural completion holds the final expression. Authors should explicitly select neutral at the end when desired; the example does.
- Escape cancels future cues and keeps the current expression. Existing transient mouth, blink, gaze and other channel release rules remain unchanged.
- Comma/period expression selection takes over an active or paused clip. Cycling continues from the current registered expression rather than a stale keyboard index.
- A valid live UDP packet retains the existing priority over clips. A packet without an expression keeps the current face; a packet with an expression selects that face. The existing timeout/reset behavior still returns to neutral.
- Direct API expression changes retain their existing behavior, including changing the selected face while a clip is paused. They do not replace the explicit clip-stop/live-takeover API.
- Legacy clips and both existing demo files are unchanged.

## Evidence and limits

The local test suite covers validation and replacement atomicity, all registered expression IDs, ordering, pause/resume, natural completion, cancellation, reset, keyboard cycling, live UDP takeover and compatibility with existing gaze/blink/speech behavior. All 24 local suites passed, totaling 167,923 counted checks plus the bounce/settling suite. See [VALIDATION_EXPRESSION_CUES.md](VALIDATION_EXPRESSION_CUES.md) for evidence and limits.

`review_expression_cues.gd` plays the real JSON clip through MotionRig, pauses/resumes it, replays it, then performs keyboard takeover and reset. The supplied MP4 is actual Godot rendering. Decoded chronological frames, close-ups and recorded runtime states support inspection; native-speed playback is unavailable to the assistant. Rendering a movie does not establish real-time performance or face tracking.
