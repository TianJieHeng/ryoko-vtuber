# Optional effect overlays: approved runtime validation

Tested with Godot 4.6.3 stable on 2026-11-05, using headless test suites and actual OpenGL runtime captures. The user approved the runtime review on 2026-11-05.

- Focused optional-effects suite: **15,118 checks, 0 failures**.
- All **24 existing Godot test suites passed** with exit status 0. No script errors, runtime errors or failure markers appeared in those test logs.
- Across the 25 suites, **183,041 counted checks passed**, plus the existing non-counted bounce measurements.
- Shared vertex include is byte-identical to the prior approved expression-cue shader's vertex source. The existing face fragment source is also byte-identical. No additional sampler is used by the face shader.
- All seven optional sprites start hidden. All-off rendering disables the sibling effects viewport and hides its mesh.
- Focused coverage includes 128 boolean combinations; all 93 expression selections plus neutral with blink/mouth/gaze changes; original authored effects preserved; malformed dictionary/key/type rejection; atomic active/paused replacement; cue deep-copy isolation; time-zero and same-time dispatch; pause, cancel, replay, completion and reset; actual loopback UDP rejection and takeover with rejected sequence reuse; timeout; source-region registration; and identical face/overlay deformation uniforms through motion, breath, bounce, pause and reset.

## Existing regression results

```text
test_audio_mouth.gd exit=0 AUDIO_MOUTH_CHECKS_PASS count=376
test_body_controls.gd exit=0 INDEPENDENT_BODY_CHECKS_PASS count=534
test_bounce.gd exit=0 BOUNCE_CHECKS_PASS body_peak=14.8804968419234 chest_peak=7.58371686935425 settled=true
test_breath.gd exit=0 BREATH_CHECKS_PASS count=15974 peak=0.99703496502315
test_brows.gd exit=0 BROW_CHECKS_PASS count=7752
test_chest_secondary.gd exit=0 CHEST_SECONDARY_CHECKS_PASS count=298 peak_source_pixels=3.06753778457642
test_clip_channels.gd exit=0 CLIP_CHANNELS_CHECKS_PASS count=348 failures=0
test_clips.gd exit=0 CLIP_CHECKS_PASS count=45
test_controls.gd exit=0 FACIAL_CONTROL_CHECKS_PASS count=89
test_earrings.gd exit=0 EARRING_CHECKS_PASS count=2065 failures=0 independent_peak=0.00077357773353
test_expression_cues.gd exit=0 EXPRESSION_CUES_CHECKS_PASS count=3951 failures=0
test_expression_gaze.gd exit=0 EXPRESSION_GAZE_CHECKS_PASS count=7135 failures=0
test_expressions.gd exit=0 EXPRESSION_CONTROL_CHECKS_PASS count=58504
test_eyelids.gd exit=0 EYELID_CHECKS_PASS count=120
test_gaze.gd exit=0 GAZE_CHECKS_PASS count=42103
test_gestures.gd exit=0 GESTURE_CHECKS_PASS count=256
test_hair_secondary.gd exit=0 HAIR_SECONDARY_CHECKS_PASS count=289 head_peak=6.67058324813843
test_integrated_bust.gd exit=0 INTEGRATED_BUST_CHECKS_PASS count=11
test_live_input.gd exit=0 LIVE_INPUT_CHECKS_PASS count=40
test_look_at.gd exit=0 LOOK_AT_CHECKS_PASS count=1107
test_loose_hair.gd exit=0 LOOSE_HAIR_CHECKS_PASS count=22731 failures=0 driver_peak=9.99901580810547 runtime_peak=4.34271812438965 independent_peak=4.52170133590698
test_motion_rig.gd exit=0 COUPLED_MOTION_RIG_CHECKS_PASS count=3204
test_ornament.gd exit=0 ORNAMENT_CHECKS_PASS count=826 driver_peak=0.08071931663141 rig_peak=0.06538102594081
test_pose_store.gd exit=0 POSE_STORE_CHECKS_PASS count=165
```

## Source and default-render preservation

- All 622 inherited PNGs and the existing expression registration remain unchanged from approved main `4328debdae08f993c90f151a29c0ee8ec7d03f95`.
- The seven optional effect PNGs are byte-identical copies of the original transparent assets in `avatar_build_assets/effects/layers/`. No new expression, artwork generation or full-body work is included. The deterministic copy/registration builder records each source checksum in the manifest.
- Actual runtime PNGs with optional effects off were compared against approved main for neutral, supported-expression gaze and authored-effect expression states. All three comparisons were pixel-identical: zero changed pixels and zero maximum channel error.

## Actual runtime review

- Godot's movie writer captured 901 frames at 30 fps, lasting 30.033 seconds. The main H.264 MP4 is 568 × 760; the face-detail MP4 is 1040 × 720 and is an enlarged crop of the same capture.
- The review shows the seven independently controlled original overlays, expression/blink/mouth combinations, head following, pause/resume, completion, replay, actual loopback UDP takeover of a paused clip, and timeout reset. This is runtime rendering, not a still-image animation.
- 121 sampled runtime states were checked. All seven effects appeared; pause held state and the cue clock; authored EXP-035 effects remained visible with optional overlays off; completion explicitly ended off; one real UDP packet took over the paused clip; timeout cleared optional overlays.
- Two source-AVI frames during pause, at 15.5 and 16.0 seconds, were pixel-identical across the complete frame.
- Sixty chronological samples at two frames per second were inspected in both full-view and enlarged face contact sheets. The sampled frames showed the expected visibility changes without visible overlay detachment, new seams or cropping. The original tear assets are fine and faint at the full-view resolution; the detail video makes them easier to inspect.

## Limits and acceptance

The 30-second movie took 1 minute 37 seconds to render, reported as 30% of real-time speed. Native-speed playback was unavailable during validation. Frame inspection and state checks do not establish temporal feel, target-machine live performance or face-tracking integration. The user approved the supplied runtime review with these limitations disclosed.

The effects are additive: turning an optional overlay off cannot remove blush, tears or other effects painted into an existing expression. No CI, paid resources, hardware flashing or remote-machine execution was used.
