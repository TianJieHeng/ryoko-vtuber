# Approved timed bust-control cues

Built on approved main `a04cbc82c443a1e1cbfb068155f82a5c2af043d9`. Adds clip scheduling for the already-approved iris gaze, controlled breathing, brows, look-at and hairpin ornament. There are no new expressions, artwork, motion amplitudes or full-body changes. The user reviewed and approved the supplied runtime video on 2026-11-05.

## New version-1 cue controls

- `pendant_secondary`: boolean, approved pendant-only addition (README_PENDANT.md). The enabled preference persists through reset, cancellation and timeout, while dynamics clear.

- `loose_hair_secondary`: boolean, added by the approved lower side-lock revision (README_LOOSE_HAIR.md). Like other secondary-motion toggles, the setting persists through cancellation and reset.

- `gaze_x`, `gaze_y`: numbers in [-1, 1]. Set both to 0 to center the independent iris offset.
- `brow_raise`, `brow_screen_left`, `brow_screen_right`: numbers in [-1, 1]. Per-side values override `brow_raise` when supplied together. Use `brow_raise: 0` to return both sides to neutral.
- `breath_level`, `breath_strength`: numbers in [0, 1]. `breath_trigger: true` starts one inhale/exhale with the optional strength. `breath_level` holds a level. `breath_cancel: true` releases it smoothly. In the same cue, trigger overrides level and cancel overrides trigger, matching the live API.
- `look_x`, `look_y`: numbers in [-1, 1]. `look_release: true` releases the attention overlay while retaining the underlying head/body pose. Aim fields in the same cue take precedence over release, matching the live API.
- `ornament_secondary`: boolean, using the existing persistent enabled/disabled setting. A clip that turns it off should explicitly turn it back on if that is the intended ending.
- `earring_secondary`: boolean, added by the approved earring revision (README_EARRINGS.md). It is likewise a persistent setting and is not changed by clip cancellation or reset.

New numeric fields reject booleans, text, non-finite values and out-of-range values at load time. Boolean fields reject numeric lookalikes. Existing clip version, fields, value handling, ordering, and demo behavior are retained. Invalid loading leaves the prior running clip untouched. Cues still cannot write files, choose paths, start nested clips or send network commands.

## Playback and ownership

- `play_clip("res://demo_bust_clip.json")` starts the new example. Shift+T plays the new example; T still plays the original demo.
- P pauses the cue clock and the entire rig, including the five new channels. P resumes without repeating cues.
- A large frame can collect several cues. They run once in array order. A reset or cancellation invalidates the remaining collected cues, including cues at the same time.
- Escape or live-input takeover cancels scheduling. Gaze, brows, breathing and look-at are released smoothly only if that clip actually controlled them. A legacy clip therefore does not claim unrelated new live controls.
- The new O, Shift+O, I, Y and V shortcuts take over from an active clip before applying their own command.
- Replacing an active clip cleans its owned new channels before the replacement starts. Invalid replacement leaves it playing.
- Natural completion keeps the final commanded state, as before. Add explicit release cues when the ending should settle to neutral. The example does this.
- Ornament, hair and chest enable settings remain persistent toggles, as they were in the live rig. Cancel and reset do not silently change those preferences.
- R/reset clears all dynamics and cancels the clip. Repeated cancellation while inactive does not erase unrelated live state.

## Actual runtime review

`review_clip_channels.gd` plays the real `demo_bust_clip.json` through the runtime clip player. The 27-second recording shows independent eye/brow cues, eyes-first attention with a breath, a 1.5-second pause/resume, ornament off/on during head motion, explicit release and completion, replay, cancellation and reset. It uses existing mouth shapes silently; it is not speech synthesis or lip-sync analysis.

Capture uses Godot's OpenGL movie writer and FFmpeg encoding. State/cue logs and decoded chronological frames support inspection. Native-speed video playback is unavailable to the assistant. The user reviewed the supplied MP4 and approved the feature before publication.
