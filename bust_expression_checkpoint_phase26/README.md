# Approved 2D bust expression checkpoint: phase 26

Standalone Godot 4.6 project with 78 cumulative expression profiles, six speech mouths, independent left/right blinks and expression rest-mouth restoration. Open project.godot and run preview.tscn.

New approved profiles: EXP-040 recovering composure, EXP-125 sudden insight, EXP-186 smug cat smile. Comparison boards are in previews, exact peaks in references, generation inputs in sources. Previous 75 profiles and 468 artwork PNGs remain byte-identical.

Headless verification: 89 baseline checks and 49,054 expression checks passed. Twelve displayed states retain original jaw/chin/neck/body outside shared speech-mouth bounds. After importing, run godot --headless --path . --script res://test_controls.gd and test_expressions.gd. Run python test_jaw_registration.py for pixel checks. Configure writable XDG cache/config/data directories if running in a sandbox.

Comparison boards are static sprite composites, not live runtime captures. Smooth transitions, audio analysis/wiring, physics and body motion are deferred. No CI was run. User approved the visual comparisons before publication.

Rebuild phase26 layers and comparisons with python tools/build_expressions_phase26.py (Pillow required). Earlier phase scripts record their original enclosing-directory workflows.
