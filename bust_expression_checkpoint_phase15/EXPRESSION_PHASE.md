# Expression phase: approved visual checkpoint

Three dedicated expression profiles have been added locally, keyed to the exact provided peak references:
- EXP-002: warm affectionate closed-eye smile.
- EXP-041: controlled anger, lowered inward brows and narrowed eyes.
- EXP-061: surprise, wide eyes, raised brows and rounded resting gasp mouth.

Each profile has separate left/right eye+brow artwork, expression-specific left/right blink artwork, and an independent resting mouth. EXP-002's reference already has both eyes closed; its blink retains the smiling closed-eye shape rather than opening them. Neutral uses the previously approved corrected blink unchanged.

Speech uses the existing six independent mouth sprites. `set_mouth` or `viseme` temporarily overrides the emotion mouth without changing eyes/emotion. `release_speech`, `mouth:REST`, `speech_active:false`, or amplitude below0.08 restores that emotion's resting mouth. An explicit neutral viseme closes the speech mouth; it does not cancel the emotion. Switching emotion while speaking preserves the active speech override.

## Verification
- Original neutral facial control suite: 89 checks passed.
- Expression control suite: 633 checks passed, including all three expressions crossed with six speech states and all four independent eyelid combinations, no duplicate eyes or mouths, speech restoration, silence and explicit release, expression switching and reset.
- Review boards show actual asset composites using registration.json, alongside crops from the exact peak references. They are not graphical runtime screenshots.

## Limits and approval
Artwork is generated and registered to the approved fixed bust, with local facial redraw; inspect likeness, hair boundaries, eyebrows, mouth scale and blink compatibility before approval. No head/neck deformation, continuous eyelid motion, audio phoneme analysis or secondary physics has been added. This phase was visually approved before publication. Do not proceed into additional expressions or motion until review.

## Provenance
Built-in image generation edited the approved neutral using each exact peak as expression-only guidance, then generated emotion-specific closed-eye variants for anger and surprise. Outputs were normalized to the1136x1384 registration canvas. Pillow performed crop, alpha masking, registration and diagnostic compositing only. Source images are in sources/, exact peak references in references/, and the rebuild script in tools/build_expressions.py. The approved neutral checkpoint on Git is unchanged.
