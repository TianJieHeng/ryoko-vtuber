# Ordinary near-closed lash correction

This records the separately reviewed ordinary-lid correction. Its unchanged-runtime and one-expression statements refer to that correction alone. This combined package adds the separately documented EXP-005 smile support, with explicit hash migrations in validation/smile_lid_baseline_migration.json. The focused shader and all 126 baseline PNGs remain unchanged.

Local review candidate. User visual approval and publication remain pending.

## Report and cause

The supplied screenshot matches approximately frame 321 (10.7 seconds) of the delivered 34-second gaze review. At about 71% lid closure, unrelated upper-lash and closed-lash clipping thresholds exposed two separated dark bands. The old lower-contour object also retained an upward diagonal at the screen-right outer corner. Both defects were present in raw Godot frames, before encoding.

## Narrow correction

Only `canonical_eye_alpha.gdshader` changes runtime behavior. The rigid moving upper lash and stationary closed lash now use opposite sides of one shared boundary in fixed eye coordinates. A spatial reveal envelope prevents higher closed-lash tips from appearing before the central contour can join them. The old lower contour is clipped behind the approaching aperture.

Filtering-aware margins preserve the existing edges. The original fixed closed-lash boundary fringe remains present in every pose, and a continuous terminal guard covers adjacent-column bilinear support at full closure. There is no exact-endpoint branch, texture swap or image crossfade.

All 126 delivered PNGs are unchanged, including the 103 original PNGs and all gaze derivatives. Eye profiles, rigid 36-pixel upper-lash travel, foreground hair, gaze coverage, mouth, white teeth, control bounds, transport and authored EXP-163 data remain unchanged. No face deformation, UV warp or additional expression is introduced. Intermediate blink and yawn lid appearance intentionally changes; the yawn's timing, controls and mouth do not.

The prior gaze reconstruction and its measured differences from the older published artwork are documented in GAZE_VALIDATION.md. This correction compares against the delivered gaze candidate at local commit 27083b1, not against the older flattened-eye renderer.

## Verification

- Clean startup and import pass. A full rebuild reproduces every tracked source and configuration file exactly.
- All existing Python suites pass: base 131, yawn 29, teeth 303, gaze assets 1,215, plus the continuous gaze-support proof. Historical mouth/art hashes remain enforced; the narrow shader migration record is updated explicitly.
- The new `tools/verify_lid_handoff.py` passes 7,946 checks. It covers all delivered artwork hashes, unchanged core runtime files, 401 closure samples per eye, four subpixel phases and bilinear endpoint support.
- Existing Godot suites pass: base 8,254; yawn 57,367; teeth 17,017; backbone 101,957; gaze 330,814; viewer layout 21. The real subprocess loopback suite passes 332 checks.
- Independent endpoint review compares 288 actual-Godot images at native, 0.49 and 1.6 scales, with 16 fractional XY positions, both endpoints and three hair positions. Every image is pixel-identical to the delivered candidate.
- Independent dense transition capture passes 2,134 assertions across 904 crops, covering every 1% closure, exact movie frames 270–330 and reverse, unilateral lids, diagonal gaze and both hair extremes. The full gaze/lid/hair matrix also passes 519 checks across 472 frames. Numeric capture success alone is not visual acceptance.
- Every frame of the corrected 1,020-frame movie is compared with the original raw sequence. There are zero changed pixels outside the projected eye regions, zero changed mouth-panel pixels and an identical controller trace. Open, fully closed, reset and final-neutral endpoints match exactly. Start and end match above the changing caption.

## Review artifact and known limits

`ryoko_separate_eye_gaze_review_2026-11-07_lid_correction.mp4` is a separate actual-Godot review artifact: 34 seconds, 1,020 frames, 30 fps, 1136×800, no audio. Full decoding reports no errors. Normal-speed playback is not claimed. Generated frames, movies, comparison sheets and logs are excluded from this source package.

Fine angular cheek outlines belong to pre-existing hair underlap edges. They are unchanged and outside this focused correction; no face repaint is hidden in this fix. Gaze remains bounded to left/right 4 source pixels, up 2 and down 1. The original inferred-art limitations still apply.

`tools/review_reported_transition.gd` reproduces the reported pose, owner isolation and near-closed samples through the public controller. Keep its output outside source. Run the README checks before merging into another expression project. The runtime patch affects only the ordinary eye shader; artwork, role meanings and full-open/full-closed registration remain compatible.
