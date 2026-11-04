# Ryoko expression phase4: approved checkpoint

This isolated local 2D project preserves nine approved expressions and adds open sobbing (EXP-023), mild disgust (EXP-081), and cheeks puffed (EXP-192). The user approved these three comparison boards before publication.

Review previews/EXP-023_approval_comparison.jpg, EXP-081_approval_comparison.jpg and EXP-192_approval_comparison.jpg. Exact reference crops appear beside actual registered rest/speech/blink composites, not graphical runtime screenshots.

Sobbing keeps squeezed-shut eyes and cheek flush without fabricated tears. Disgust has a dedicated scrunched-nose detail and crooked tooth mouth. Puffed cheeks use an actual expanded face contour; it deflates during speech and returns with the pinched rest mouth afterward.

Open project.godot here; --demo cycles all twelve profiles. Existing mouth override/rest and independent blink controls remain. No head/body deformation, continuous eyelid motion, audio analysis or physics is claimed. Further expression phases require a new visual review.

Run headless tests with Godot 4.6.3: --headless --path . --script res://test_controls.gd and res://test_expressions.gd. Rebuilding this phase’s artwork/composites uses tools/build_expressions_phase4.py with Pillow, NumPy and SciPy; runtime needs no Python.
