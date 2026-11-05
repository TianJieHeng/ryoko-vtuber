# Approved 2D bust expression checkpoint: phase 24

Standalone Godot 4.6 project with 72 cumulative expression profiles, six speech mouths, independent left/right blinks and expression rest-mouth restoration. Open project.godot and run preview.tscn.

New approved profiles: EXP-069 suspicious startle, EXP-137 realizing a mistake, EXP-178 restless drowsiness. Exact reference comparisons are in previews, source peaks in references, generation sources in sources. All previous 69 profiles and their artwork remain unchanged. Original full-body and earlier checkpoints are untouched.

Headless verification rerun on 2026-11-05: 89 baseline checks and 45,278 expression checks passed. Twelve displayed states retain the original jaw/chin/neck/body outside shared speech-mouth bounds. See test logs and test_jaw_registration.py. Run godot --headless --path . --script res://test_controls.gd and test_expressions.gd after importing the project.

These are registered raster sprite layers with immediate state changes, not a completed production rig. Comparison boards are static sprite composites, not live runtime captures. Smooth transitions, audio analysis/wiring, physics and body motion are deferred. No CI was run.

See PHASE24_NOTES.md for visual acting and layer details. Build script in tools records original extraction workflow; it expects the enclosing phase directory with project/ and sources/.
