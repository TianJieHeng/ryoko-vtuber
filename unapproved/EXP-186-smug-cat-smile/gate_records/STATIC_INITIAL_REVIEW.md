# EXP-186 bounded static review

## Verdict

**HOLD: the KP5 peak and KP6 eased-peak ordinary eyelids close too far.** The source requires a narrowed, amused watching gaze. The frozen render leaves only very thin lower-iris strips and looks nearly asleep at bust scale. This materially changes the combined facial read despite its technically nonzero iris exposure. The broad, biased, sealed mouth itself is viable.

This is a specific two-anchor control-fit hold, not a claim that EXP-186 needs new art, a new eye family or an anatomical capability extension. It is not a rejection for canonical lip fullness, missing painted creases or failure to reproduce the source painting pixel-for-pixel. The current source is not a lightly narrowed EXP-102 relabeling or EXP-181 wink; its deeper bilateral eye state is distinct, but overclosed.

## Exact reviewed inputs and capture

- Original reference commit: `7693d1b8718c3bb1c717bd586fb472a7efc42403`.
- Original sheet SHA256: `95a85f6bd6f16fc3ecd0d914b83dafef8464a91928239e9bd53bf0add180ccc8`.
- Common source freeze: `dd52d78b1a6987140ea0728a41f35841746fc0e102c66c1941fd64677ddf919a`.
- Frozen six-state plan: `f5343ba386dc1b2544adebdd04db94494fd61909456266b51d2f42fdc54e8445`.
- Accepted retry input binding: `386041cf230a1a15da4ab295159914ff263b43a0774e421ba637527bb9146a3c`.
- Actual capture receipt: `0a0c34bb322a12373088eb1cc7a3959b8bc53c91abfb32e23c0684edd4eb4dbc`.
- Six native 1136 by 1384 frames, X11, llvmpipe, zero capture failures. No normal-speed observation.

The original launcher failed before Godot with exit 127 because `python` was not on the desktop terminal PATH. Its wrapper and binding remain saved. Independent review verified that the retry changed only two invocations to `/usr/bin/python3`, with no changed source, pose or harness. The successful retry exited 0. This launcher correction is not a parameter refinement.

## Visual findings

I inspected all nine exact original source panels individually, the native peak and recovery busts, all six native face crops and reduced busts, enlarged eye comparisons and all six mouth details.

1. **Neutral and onset: sound.** The onset develops bilateral lid narrowing, slight brow asymmetry and a small sealed biased smile without adding unrelated motion.
2. **Mouth peak and ease: sound as a bounded static component.** The lip seam broadens from the canonical neutral, the screen-right endpoint lifts more strongly, and the left side remains positively lifted. The center joins stay connected; no oral opening, tongue, tooth flash, detached corner, new pigment or whole-mouth proxy appears. Canonical lip fullness differs from the thinner source painting and is not itself a blocker.
3. **Peak and eased-peak eyes: HOLD.** The exact source KP5/6 retains recognizable amber iris and pupil windows beneath the upper lashes, including the more-open screen-right eye. The current .72/.65 and .66/.62 ordinary closure states leave almost only the bottom amber rims. In the native crop, small amber pixels do remain, so this is not literal full closure; in the whole bust, the expression nevertheless reads near-closed/drowsy rather than knowingly amused. The brow asymmetry and grin do not fully recover that missing watching gaze. See `evidence/SOURCE_RENDER_EYE_READ.png` and `evidence/INDEPENDENT_BUST_ATLAS.png`.
4. **Recovery and neutral return: sound.** Both eyes reopen, the sealed smile diminishes, and the final frame is pixel-identical to the initial canonical neutral. The static samples establish those anchors, not their interpolation or acting timing.

The smallest justified next fit, if separately authorized, is less ordinary closure at KP5 and KP6 while preserving the same slight left/right bias and every other frozen value. Do not switch to a fully closed smile-eye contour, add widening, repaint, change mouth values or sweep unrelated controls. No such refinement or extra capture has been performed or authorized by this review.

## Independent integrity and anatomy checks

All 605 baseline files, 182 PNGs and 16 profiles remain exact; no profile or timeline for EXP-186 exists. Independent source Git-blob/crop proofs, pre-render binding audit and 5,011-check headless replay passed. Builder checks reported 6,573 static assertions and 826,602 retained-baseline assertions with zero failures.

Every actual PNG and raw RGBA hash matches the capture receipt. All six actual controls and anatomical snapshots match the independent headless fixture exactly. Changed pixels are confined to eye/brow and mouth regions. Native neutral start and return are identical. Head/body, source textures, UV, unit scale, full owner opacity, separate rigid anatomy, exact zero opening and existing corner/width budgets remain preserved. See `evidence/INDEPENDENT_CAPTURE_INTEGRITY.json`.

The reviewer's separate cold import exited 137 without a reported reason. Its successful independent headless replay reused completed derived imports in a separate byte-identical source copy; no independent cold-import success is claimed. An initial reviewer test overconstrained valid rigid oral-owner translation and was corrected without changing source or poses; its diagnostic is retained.

## Retained limits

This is a static HOLD, not permission to author EXP-186's full performance. No timeline, registry addition, public preview, Library/Git write, CI, paid resource, remote execution, live socket, AI/TTS or approved integration is included. No pose refinement has been used. Any later full-performance continuation must first include the separately reviewed EXP-050 seventeenth profile in the common baseline.
