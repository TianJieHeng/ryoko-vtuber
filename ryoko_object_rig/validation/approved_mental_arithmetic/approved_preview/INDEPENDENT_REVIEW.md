# EXP-129 Mental arithmetic: independent review

## Result and scope

The corrected third native capture and encoded preview pass independent technical review. This is an isolated, unapproved candidate, not production integration or permission to publish. No production files were edited. The original approved36 baseline remains pinned to commit `3ce98774282ad6c20dfbd7018d20838ff861b762`.

Deliverable: `Mental_arithmetic_review_v1.mp4`, 180331 bytes, SHA-256 `7d952bd8a306cd72bb9fe374e50b3d852821c96d139b88c2fa80f55d96447a50`. H.264/yuv420p, 968×800, 30 fps, 121 frames, 4.033333-second container duration covering authored samples from 0 to 4 seconds inclusive. The existing dimension-gated encoder assembled only verified third-attempt native frames. The two wrong-size attempts are historical evidence only and were not encoded.

## Verified evidence

- Eight native static anchors pass 934 assertions. Correct full/detail PNG dimensions are 568×800 and 400×360.
- Native temporal receipt passes 9341 assertions. All 121 frame/time entries are correctly ordered, and all 242 raw RGBA SHA-256 hashes match the actual PNGs.
- All 121 native poses equal the headless poses. An independently reconstructed smoothstep timeline, including the existing runtime's initial 0.30-second restart blend, differs by at most 2.975e-8 per control.
- Pose-specific assertions verify initial symmetric lowering, first screen-left lift/upward glance, intervening pinch, second screen-right lift with centered gaze, purse release by frame 80, no speech opening, and bounded symmetric partial lids.
- All 17 neutral-hold samples are pixel-exact in both views; first and final native frames are identical. Static neutral, first-lift, second-lift, and final neutral match their corresponding native temporal samples exactly.
- All changed full-view pixels lie in face rectangle [209,284,356,389]. Body, clothing, hair outside the face, background, and overall silhouette are unchanged across the native sequence.
- All 999 frozen source files (184 PNGs) and the external manifest retain their exact hashes in both source and candidate rig copy. Production registry IDs match the approved36 list and omit EXP-129.
- MP4 fully decodes to 121 RGB frames with no decoder error. All timestamps match 30 Hz. Every decoded full/detail panel is compared with its same-index native frame. Mean absolute channel differences are 1.292/255 full and 2.030/255 detail. Maximum same-index versus nearest-frame face-error disadvantage is 0.002257/255, consistent with lossy coding and repeated/near-identical poses rather than material reordering. Equal hold frames need not have a unique nearest index.

Machine-readable evidence: `review_evidence/review_checks.json`, `native_frame_hashes.json`, and `decoded_frame_order.json`. Visual evidence: `static_faces.png`, `encoded_keyframes.png`, and `bust_progression.png` in the same directory.

## Visual and source-fit review

I inspected the actual nine-panel source sheet, native static face views, actual-size 568×800 bust captures, and decoded keyframe pixels. This inspection does not constitute continuous normal-speed observation.

The candidate visibly alternates brow emphasis and seals/purses the lips, with a brief upward gaze on the first lift and return to center before the second. At bust scale these changes are restrained; the upglance and brow alternation read more clearly in the detail panel. The gaze remains paired in inspected images, without an obvious divergent-eye jump. There is no obvious new mouth opening or lip seam in the inspected keyframes. Dark/jagged upper lash and hair-overlap edges are visible at detail scale in neutral as well as active poses; those inherited edges remain a visual caveat, not evidence of a newly introduced candidate defect.

Source fit is partial. The rig cannot move brows horizontally together, so the knitted-brow intent is approximated with vertical lowering and opposing tilt. The source sheet includes head tilts and a closed-eye/open-mouth release that this facial-only, sealed, speechless candidate deliberately excludes. The second-side lift is an authored interpretation of catalogue intent rather than a pixel-identical source panel. Exact neutral is verified, but resemblance and expressiveness still require user judgment.

No continuous normal-speed viewing, whole-runtime/lip-sync integration test, all36 native trajectory regression, approval, or publication is claimed by this independent review. Supported-UI playback, if performed by the capture reviewer, is separate evidence and should retain that reviewer's precise limitations.
