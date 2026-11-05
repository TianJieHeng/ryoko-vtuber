# Independent eyelid controls

Based on approved gesture rig 3383edb. Uses existing eyelid textures with no changes to expressions or artwork.

## Controls
- J: one screen-left wink (your left when looking at the character).
- K: one screen-right wink.
- U: release independent eyelid controls.
- Existing B bilateral blink and R reset remain available.

API fields:
- `wink`: `screen_left`, `screen_right`, or `both`.
- `wink_duration`: optional seconds, bounded to 0.08–0.8, default 0.28.
- `eye_screen_left` and `eye_screen_right`: held eyelid controls, closed at values >=0.5. Values below 0.5 select the expression's normal eye layer.
- `release_eye_controls: true`: clears held controls and active winks.

Names deliberately use viewer coordinates. The existing R eye asset is screen-left; the L asset is screen-right. Unknown wink names are rejected rather than guessing a side. Held per-eye values override the shared blink setting; a timed wink can temporarily close a held-open eye. Release restores the original shared/automatic control behavior.

Automatic bilateral blinking is deferred while independent controls are active, then resumes after a short grace period. Gesture, head/body, chest secondary and audio controls continue independently. Reset clears the independent controls.

The existing artwork supplies discrete open/closed layers, not continuously deforming eyelids. A naturally closed-eye expression still uses its authored resting eye shape; this feature does not redraw it.

`--eyelid-proof` captures a 16-second runtime test with screen-left wink, screen-right wink, held screen-left closure combined with a greeting gesture, release, explicit bilateral blink and automatic blinking recovery. Automatic blinking is suppressed during the labeled one-eye proof sections to keep the demonstration unambiguous.

`test_eyelids.gd` adds 120 checks covering exact screen mapping, visible sprites, timing, holds, auto-blink deferral, duration bounds, invalid names, simultaneous gesture/audio controls, reset and keyboard input. All prior suites pass.

Approved by the user on 2026-11-05 and published with all existing artwork and motion preserved.
