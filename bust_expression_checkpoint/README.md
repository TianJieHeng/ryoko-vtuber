# Ryoko dedicated facial expressions: review checkpoint

This isolated local 2D project extends the approved bust facial checkpoint with EXP-002 (warm smile), EXP-041 (controlled anger), and EXP-061 (surprise). This is the approved expression checkpoint.

Read `EXPRESSION_PHASE.md` for controls, test results, provenance, scope and approval limits. Open `project.godot` here to run. `--demo` cycles the three expressions with speech/blink states.

Tests: `godot --headless --path . --script res://test_controls.gd` (89 checks) and `godot --headless --path . --script res://test_expressions.gd` (633 checks).

Review files are `previews/EXP-002_approval_comparison.jpg`, `previews/EXP-041_approval_comparison.jpg`, and `previews/EXP-061_approval_comparison.jpg`. They show exact-reference crops and actual registered sprite composites, not graphical runtime captures.

The original fullbody project and the approved Git checkpoint are untouched. No3D, audio phoneme analysis, head/body deformation or secondary physics is added here.
