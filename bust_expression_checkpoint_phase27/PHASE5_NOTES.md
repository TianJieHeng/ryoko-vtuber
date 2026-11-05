# Phase5: pending review

Exact EXP-005, EXP-161 and EXP-197 references guide facial acting on the approved fixed neutral bust. Generated raster artwork is separated into registered eye/brow, blink and mouth sprites. Kiss adds independent cheek blush.

Hearty laughter has broad upturned open mouth, upper teeth/tongue and happy closed crescents. Sleepy has low lids exposing amber slivers, relaxed brows and small slack mouth. Playful kiss has fully closed eyes, small centered pursed pink lips and normal unpuffed cheeks. These are controllable expression states, not dedicated laughter or kiss animation clips.

All twelve prior expression assets and previously approved blink fixes remain unchanged. Independent left/right blink and speech overrides remain. Source imagery and prompts are in the enclosing phase folder; Pillow handles masks, alpha extraction and registration only.

Comparisons are static composites. Graphical runtime capture, actual audio-to-viseme integration, continuous deformation and physics remain untested or unimplemented.

Verification: Godot 4.6.3 headless passed 89 baseline facial checks and 6,137 expression-control checks. All 76 prior artwork PNGs are byte-identical. Tests cover fifteen expressions, six speech states, independent blink combinations, closed-eye release, sleepy open/closed distinction, persistent blush and all prior special effects.
