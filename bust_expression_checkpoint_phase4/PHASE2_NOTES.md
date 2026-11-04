# Expression phase2 review

Exact reference targets: EXP-021 quiet sadness, EXP-102 knowing smirk, EXP-181 cheeky wink. Built-in image generation used the approved neutral as identity/placement target and each exact peak as expression guidance only. Emotion-specific blink variants preserve brows and rest-mouth expression. Extracted local eye/brow and mouth tiles are alpha-masked and registered to the existing fixed bust. Original body, neck, nose, speech mouths and neutral blink assets remain unchanged.

Controls preserve six independent speech shapes and restore each expression's rest mouth on release. Wink is viewer-right closed at rest and during blink; the remaining open eye closes on paired blink. Speech never clears the wink.

Godot4.6.3 headless results: 89 baseline facial assertions and 1266 six-expression assertions passed. All 25 prior approved artwork files are byte-for-byte unchanged. Tests cover all six emotions, six speech mouth states, four eyelid combinations, mouth exclusivity, emotion restoration, speech release, amplitude fallback, invalid inputs, reset, and wink closed-art identity through blink.

Review boards are actual sprite composites, not graphical runtime captures. Generated likeness and local blending were visually approved by the user. No network/audio analysis, head/body deformation, physics or additional phases were performed.

Sources are in sources/; tools/build_expressions_phase2.py reproduces new layer registration and review composites. Existing EXPRESSION_PHASE.md records the already-approved preceding phase, not these three additions.
