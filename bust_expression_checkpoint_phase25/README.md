# Approved 2D bust expression checkpoint: phase 25

Standalone Godot 4.6 project with 75 cumulative expression profiles, six speech mouths, independent left/right blinks and expression rest-mouth restoration. Open project.godot and run preview.tscn.

New approved profiles: EXP-007 relieved smile, EXP-092 sour taste, EXP-128 reading intently. Comparison boards are in previews, exact peaks in references, generation inputs in sources. Previous 72 profiles and 447 artwork PNGs remain byte-identical.

Headless verification: 89 baseline checks and 47,164 expression checks passed. Twelve displayed states retain original jaw/chin/neck/body outside shared speech-mouth bounds. After importing, run godot --headless --path . --script res://test_controls.gd and test_expressions.gd. Run python test_jaw_registration.py for pixel checks. Configure writable XDG cache/config/data directories if running in a sandbox.

Comparison boards are static sprite composites, not live runtime captures. Smooth transitions, audio analysis/wiring, physics and body motion are deferred. No CI was run. User approved the visual comparisons before publication.

Rebuild phase25 layers and comparisons with python tools/build_expressions_phase25.py (Pillow required). Earlier phase scripts record their original enclosing-directory workflows.
