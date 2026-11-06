# Approved reusable bust performance presets

Based on approved main `93b39bb03918be0f73aa73465ec196f34bbb32e4`. The user approved the actual Godot runtime review on 2026-11-06. It adds no expressions or artwork, no deformation, and no full-body work. All existing motion drivers, source artwork, expression registrations, shaders, default behavior and legacy pose slots are retained.

The bust channels in the original handoff are already implemented. This addition makes their existing controls reusable together instead of requiring the performer to re-enter pose, gaze, brows, expression selection and optional effects separately.

## Use

- Ctrl+Shift+1, Ctrl+Shift+2 or Ctrl+Shift+3 saves a performance setup.
- Shift+1, Shift+2 or Shift+3 recalls it.
- The original Ctrl+1/2/3 saves and 1/2/3 recalls still use independent head/body-only pose slots.
- Direct local API: `apply_controls({"performance_save": 1})` and `apply_controls({"performance_load": 1})`. Slot values must be integral numbers from 1 through 3; booleans and numeric strings are rejected.

A performance snapshot stores head/torso control targets, body-follow mode, gaze targets, independent brow targets, one existing expression ID, and all seven optional-effect flags. It is not a new expression registration. Selecting an existing expression preserves that expression's own artwork and the approved expression-specific gaze/brow fallback.

It stores targets, not the current eased frame, active gesture or attention offsets. If body-follow is on, the saved body target is the head target, matching the original pose store. It does not save transient winks, mouth/audio state, breath, bounce, gesture phases, pointer-follow modes, clip progress or secondary-motion preferences. Saving while those are active does not reproduce their freeze-frame on recall.

## Recall and ownership

Recall validates the entire saved entry before changing anything. Missing or invalid entries leave the current clip, pause state and controls unchanged. A successful recall cancels an active or paused clip, disables head/gaze pointer-follow, releases the coordinated-attention overlay smoothly, and applies the saved targets. Existing head, gaze and brow easing is preserved. Expression selection and optional-effect visibility remain discrete, just like their existing controls.

The saved effects replace all seven flags, including false values. They do not remove effects painted into expression artwork. Existing live mouth, eyelid, gesture and breath control remains independent. Cancelling an active clip retains the previously approved cleanup of its audio, gesture, eyelid and owned channels.

A combined API patch loads after reset and before its explicit control fields, then saves after them. This allows `performance_load: 1`, explicit head/effect overrides, and `performance_save: 2` in one patch. Invalid preset slot/load values reject the patch before reset or other mutation. This does not introduce a general strict-validation policy for legacy direct-API fields.

Existing UDP input can take over a recalled setup, and its existing two-second timeout still resets the rig. A local recall does not cancel an already-active UDP lease, so the same timeout can also reset a locally recalled setup. Reset and timeout do not erase saved slots. UDP and timed clips cannot save or load performances and retain their original no-persistence allowlists.

## Persistence

The three slots use `user://rig_performances.json`, separate from `rig_poses.json`. No file is created and no setup is recalled automatically at startup. The format has version 1, exact required snapshot fields, registered-expression validation, strict booleans and bounded finite numeric axes. Loading rejects files over 64 KiB, malformed schemas and invalid slots without replacing in-memory entries or writing the file. Saving deep-copies a complete candidate, writes and flushes a temporary sibling, then renames it over the destination. A failed write or rename leaves the in-memory slots unchanged.

The review uses `review_performances.json` in an isolated Godot data directory, not the user's normal slots.

## Review and checks

`review_performance_presets.gd` creates an actual 26-second Godot movie. It saves two setups made from existing controls/artwork, clears and reloads the in-memory slots from disk, recalls both, layers mouth/wink/greeting controls, takes over a paused clip, then receives a real loopback UDP command and shows timeout recovery. The synthetic audio-level input only moves existing mouth shapes; it does not claim microphone capture or phoneme recognition.

`test_performance_presets.gd` checks persistence, deep-copy isolation, invalid schemas/types, bounded files, failed writes, target easing, active/paused clip cancellation, invalid recall atomicity, combined command ordering, pointer/attention release, existing expressions, independent live controls, reset, keyboard separation and real UDP takeover/timeout. All inherited suites are retained.

The review is inspected using decoded chronological frames and enlarged face crops. Native-speed playback is unavailable in this environment, so perceived naturalness and real-time performance remain unverified. The reviewed source and motion behavior are preserved in this approved checkpoint.
