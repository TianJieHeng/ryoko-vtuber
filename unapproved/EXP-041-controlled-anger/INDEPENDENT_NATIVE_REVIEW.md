# EXP-041 independent native and MP4 review

Reviewed 2026-11-10. **Qualified for user review; candidate remains UNAPPROVED.** Automated native/frame/decode checks pass. The staged lip-pressure release is not visibly demonstrated, as explained below. No production integration, publication, or approval is inferred.

## Verified artifact and preservation

- Video: `Controlled_anger_review_v1.mp4`, SHA-256 `cb080ef5a98cfb12d4fa885315ca39893d301954f8a37cef2432ca9d23d0a0db`.
- H.264, 968×800, 30 fps, 121 decoded frames, 4.033333 seconds including the final sampled endpoint. Complete decode returned exit 0 with no diagnostic text. Every presentation timestamp matches its 30 fps index.
- Native receipts report 1,102 static checks and 9,406 motion checks, zero failures. Capture reports X11 and llvmpipe; it is not a headless visual substitute.
- Exact membership and dimensions pass for 16 static images and all 242 native motion images: bust/full 568×800, detail 400×360. All 242 raw RGBA hashes match native capture records. Native poses match the headless receipts; independent smoothstep/restart arithmetic differs by at most 2.70×10⁻⁸ control units.
- All 999 frozen files and the extra manifest remain unchanged in both source and copied rig. The 36-profile registry is unchanged and excludes EXP-041. Reference sheet/catalogue hashes match the freeze.
- Native neutral holds and bookends are pixel-exact. Five corresponding static/motion anchors match exactly in RGBA. All native motion changes lie within full-frame rectangle [209,287,356,385); pixels outside the face remain unchanged.
- Both decoded video panels were compared with every same-index native frame. Maximum panel mean absolute RGB error is 1.295 for bust and 2.070 for detail. Maximum expected-versus-nearest face-error gap is 0.01266, below the established 0.10 review threshold. These lossy comparisons reveal no material reorder; repeated or nearly identical poses cannot be uniquely ordered by visual matching alone.

## Actual pixel inspection

Viewed all eight static face anchors, four native actual-size bust frames, nine chronological decoded face frames, the actual candidate peak detail, and approved Cold Glare/Silent Fury peak details. The two neighbor detail images independently match frame-45 RGBA hashes in their frozen approved native receipts.

- The result visibly narrows both eyes, lowers and angles the brows, holds a closed restrained mouth, and returns to neutral. Gaze and body remain fixed. At bust scale this reads as restrained sternness; the strongest source-painted inward brow tension is only partially conveyed by rigid parts.
- Compared with Cold Glare, the candidate has added inward brow angle and avoids the small pursed-mouth shape. It has slightly less lid closure. Compared with Silent Fury, its narrower eyes and milder brow angle are visible. These are related expressions, with modest detail-scale distinctions rather than radically different silhouettes.
- **Important limit:** `controlled_anger` and `ease_pressure` static captures are byte-for-byte pixel-identical in both views, although lip pressure changes from 0.65 to 0.38. Therefore the proposed lip-first release is a control-state distinction, not a demonstrated visible beat. Do not describe the video as visibly easing its mouth before the brow/lid release. This does not invalidate the native receipt or change the authored profile, but it limits the performance claim.
- Outer-eye/hair-edge fragments remain visible, including in neutral and approved neighboring captures. The inherited rigid-part appearance is not newly repaired by this candidate. No new mouth opening, missing iris, body shift, or lost neutral return was evident in the inspected images.

## Remaining limits

This review used still pixels and complete frame/decode arithmetic, not continuous normal-speed viewing. Live engine pacing, cross-expression transitions, speech/lip-sync, full-runtime composition and export behavior were not newly validated. Source art is a reference, not exact motion ground truth. User aesthetic approval remains outstanding. No baseline, profile or rendering code was changed during this independent review.

Machine receipts: `review_evidence/review_checks.json`, `native_frame_hashes.json`, `decoded_frame_order.json` and `independent_visual_findings.json`. Visual evidence: `static_faces.png`, `bust_progression.png` and `encoded_keyframes.png` in the same directory. The earlier `partial_review.json` records missing inputs before capture and is superseded by the completed PASS receipt.
