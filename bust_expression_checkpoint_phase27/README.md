# Approved 2D bust expression checkpoint: phase 27

Standalone Godot 4.6 project with 81 cumulative expression profiles, six speech mouths, independent left/right blinks and expression rest-mouth restoration. Open project.godot and run preview.tscn.

New approved profiles: EXP-063 stunned silence, EXP-090 queasy, EXP-153 hiding a smile. Comparison boards are in previews, exact peaks in references and generation inputs in sources. All previous 78 profiles and 489 artwork PNGs remain byte-identical.

Headless verification: 89 baseline and 50,944 expression checks passed. Twelve displayed states retain original jaw/chin/neck/body outside shared speech-mouth bounds. After importing, run godot --headless --path . --script res://test_controls.gd and test_expressions.gd. Run python test_jaw_registration.py for pixel checks. Configure writable XDG cache/config/data directories in a sandbox.

Comparison boards are static sprite composites, not live runtime captures. Smooth transitions, audio wiring, physics and body motion are deferred. No CI was run. User approved the visual comparisons before publication.

Rebuild phase27 layers and comparisons with python tools/build_expressions_phase27.py (Pillow required).
