# Approved 2D bust expression checkpoint: phase 12

Standalone Godot 4.6 project with thirty-six cumulative expression profiles, six speech mouths, independent left/right blinks and expression rest-mouth restoration. Open project.godot and run preview.tscn.

New approved profiles: EXP-047 clenched-teeth annoyance, EXP-076 overwhelmed stare, EXP-177 meditative calm. Exact reference comparisons are in previews, source peaks in references, generation sources in sources. All previous 33 profiles and their artwork remain unchanged. Original full-body and earlier checkpoints are untouched.

Headless verification: 89 baseline checks and 22,573 expression checks passed. See control_tests.log, expression_tests.log and prior_asset_regression.txt. Run godot --headless --path . --script res://test_controls.gd and test_expressions.gd after importing the project.

These are registered raster sprite layers with immediate state changes, not a completed production rig. Comparison boards are static sprite composites, not live runtime captures. Smooth transitions, audio analysis/wiring, physics and body motion are deferred. No CI was run.

See PHASE12_NOTES.md for visual acting and layer details.
