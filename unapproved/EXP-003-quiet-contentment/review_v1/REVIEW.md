# Quiet Contentment EXP-003 independent review

**PASS for review delivery; not approved or integrated.**

The v002 reference sheet and all seven native static bust/detail pairs were inspected, followed by selected decoded MP4 phases. The primary closed-eye pose corresponds to the actual reference peak, even though the catalogue says half-relaxed eyes. The separate partial-opening alternative is not in the timeline. The clear action is a gentle eye-settling transition and held closed-eye pose, followed by reopening; the small sealed smile is intentionally restrained. This reads as calm contentment rather than a large happy reaction.

Existing lash/hair edge seams and the thick closed-lash contour remain visible in the detail crop. The existing eye geometry does not reproduce the reference contour exactly. No new anatomy, body acting or runtime change is claimed. Continuous normal-speed observation is not part of this independent image/decode review; the parent performs and reports its own sampled playback inspection separately.

## Verified

- All 1,124 frozen baseline files, including 184 PNGs, match both the isolated rig and original approved27 source. Registry IDs remain identical, with EXP-003 absent from production. Only the recorded import-generated UID sidecar is additional.
- Reference catalogue, sheet and all nine panel hashes match.
- Native static gate passes 4,193 assertions; native motion gate passes 8,943. All 139 native pose records match the headless records.
- All 278 full/detail raw-image hashes match the capture records. Exact neutral bookends and static-neutral agreement hold. Every full-frame changed pixel lies inside face bounds x209–355, y287–387, leaving body and background unchanged.
- Five selected static/motion anchor pairs match exactly, including the held peak and neutral return.
- Shipped MP4 is H.264, yuv420p, 968×800, 139 frames at 30 fps, 4.633333 seconds, 213,730 bytes. Complete independent decode exits cleanly. All 139 timestamps match frame/30.
- Every decoded bust/detail panel was compared with its same-index native frame. Maximum detail panel mean absolute RGB error is 2.0691/255; maximum expected-versus-nearest face error difference is 0.00729/255, consistent with compression and repeated/near-identical poses rather than reordered animation.

MP4 SHA-256: b6ee41008ff0d45a9eae2fc056f9de0bbc98444107b7bc7da817ac1efc456432

Evidence: `review_evidence/review_checks.json`, `native_frame_hashes.json`, `decoded_frame_order.json`, `static_faces.png`, `encoded_keyframes.png`, and `bust_progression.png`. `review_validation.py` requires the original workspace's full baseline freeze and accessible source references; it is not a self-contained portable runtime test.

## Parent playback observation

The parent reports sampled 1× ffplay phases at a 1180×812 bust/detail window: the closed-eye hold and half-open transition showed clearly visible settling/reopening, with the mouth remaining quiet. The player was closed and verified gone. This is sampled-phase evidence, not continuous observation or a live engine pacing certification. See `PLAYBACK_REVIEW.json`.
