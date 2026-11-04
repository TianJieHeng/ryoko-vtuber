# Expression phase4: approved checkpoint

Targets are exact EXP-023 open-sobbing, EXP-081 mild-disgust and EXP-192 cheeks-puffed peaks. Built-in image generation used the approved neutral as identity/position target, with reference facial acting only. Sobbing has closed eyes, flushed cheeks and a broad crying mouth, but no invented tear streams. Disgust adds a separate nose-crease detail. Puffed cheeks add a genuine expanded contour extracted from generated face artwork, not only a pinched mouth on the neutral silhouette.

Puffed contour is a rest-only effect: any active speech viseme deflates it; speech release restores it and the pinched emotion mouth. Sobbing cheek flush and disgust nose detail remain during speech and blink. All previous expression assets remain unchanged. No continuous cheek inflation animation or mesh deformation is claimed; this is a discrete registered-art state change.

Verification: Godot4.6.3 headless passed 89 baseline facial checks and 4,331 twelve-expression checks. Tests include every expression across six speech states and four eyelid combinations, mouth restoration, blink preservation, closed-eye behavior, blush/nose effects, and puff deflation/restoration. The prior asset regression report verifies all prior artwork is byte-identical.

Review boards are actual registered-sprite composites, not graphical runtime screenshots. Full GPU/display capture and audio-driven runtime integration remain untested. Head/body deformation, physics and audio analysis are not added. User approved this phase before publication; further phases remain subject to review.

Source imagery is included in sources/; the rebuild script is tools/build_expressions_phase4.py. Pillow/NumPy/SciPy handle alpha extraction, masking, registration and diagnostic composites; the facial artwork itself was image-generated.
