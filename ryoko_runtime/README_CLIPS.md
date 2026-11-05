# Timed animation clips

Based on approved pose rig a14d2c2. Combines existing controls without changing artwork or motion physics.

The approved bust-channel extension and its cancellation rules are documented in [README_CLIP_CHANNELS.md](README_CLIP_CHANNELS.md). Shift+T plays the new bust-channel example; the original demo and T shortcut remain unchanged.

## Playback
- T: play the included `demo_clip.json` once.
- P: pause/resume the clip and rig simulation together. WAV playback, if active, is paused too.
- Escape: stop scheduling future cues, release active gesture/eye/audio overrides, and keep the current live pose.
- Normal movement keys or M take control and stop an active clip.
- R resets the rig and stops the clip.

The local API accepts `clip_play: true` for the demo, `clip_paused: true/false`, and `clip_stop: true`. Code can call `play_clip(path)` to load another local JSON clip.

## Format
A clip has `version: 1`, a finite `duration` in seconds (0–120), and a time-ordered `cues` array. Each cue contains a nonnegative `time` and a `controls` dictionary. The controls use the existing head/body, gesture, wink, eyelid, mouth/audio-level, blink and secondary-motion fields. Only scalar, typed controls from the driver's allowlist are accepted. Clips cannot write pose files or choose arbitrary file paths through cue data. Invalid loading leaves the prior loaded clip untouched.

Cues crossed by a slow frame are dispatched once in order. Equal-time cues preserve array order. Playback does not loop. A normal completion leaves the final commanded pose/control state in effect, so authors should include explicit release cues for transient controls; the included demo does. A reset cue intentionally stops the clip, just like manual reset.

The demo combines a greeting, a screen-right wink, silent mouth-control cues, an acknowledgment dip, a screen-left wink and a neutral recovery. It is choreography, not speech recognition or audio lip sync. `--clip-proof` records a 19-second runtime demonstration including a 1.5-second pause/resume.

`test_clips.gd` adds 45 checks for cue order, single dispatch, frame skipping, one-shot completion, paused clocks/rig, validation, no file-writing cues, cancellation cleanup, inactive-stop isolation and reset. All prior test suites also pass.

Approved by the user on 2026-11-05 and published with existing artwork and motion preserved.
