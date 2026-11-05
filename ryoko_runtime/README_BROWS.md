# Independent neutral brow controls

User-approved on 2026-11-05 and integrated with rigid-iris gaze, controlled breathing, look-at and hairpin ornament. No new expression presets are produced.

## Controls

- O toggles both brows between neutral and raised. Shift+O independently toggles the hairpin ornament.
- API/live UDP: `brow_raise` sets both sides from -1 (lower) to 1 (raise).
- `brow_screen_left` and `brow_screen_right` independently override each side, using screen-side naming.
- R/reset and the live-input timeout return them to neutral.

Each visible neutral brow is a rigid texture translated vertically by at most five source pixels (about 2.5 pixels in the review window), with 0.15-second smoothing. No stretch, scale or eye deformation is used. Fixed masks keep the translated brow beneath the foreground hair. Gaze, eyelids, mouth, torso, crown and breathing controls remain separate.

The source brows were baked into the neutral face. The derivative layers therefore include a reconstructed skin patch where the original brow moves away, using nearby source skin colors. This is a small 2D cutout cleanup, not exact recovery of hidden skin or a complete redrawn expression. The original 594 artwork PNGs and the approved rigid-iris textures are untouched. At exact rest the shader uses the original brow rendering. Non-neutral expression presets disable these layers and retain their authored brows.

## Validation and review

`test_brows.gd` covers bounds, easing, uniform translation/preserved shape, independent sides, reset, blink/mouth compatibility, expression fallback, actual local UDP delivery and timeout release. All prior suites are rerun. See test logs for actual counts.

`--brow-proof` records both brows raising/lowering, each screen-side brow independently, a combined mouth/head pose and return to neutral. The MP4 is actual Godot rendering. Review includes chronological frames and enlarged face crops; normal-speed playback is unavailable here.

The user reviewed and approved both brow and breathing runtime proofs before publication.
