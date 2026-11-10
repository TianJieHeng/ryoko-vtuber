# Bitter Taste EXP-093: independent review

**Ready for user review, not approved or integrated.** The open-mouth grimace, heavy-lid narrowing, inward/lowered brows, closed aftertaste and neutral return are visibly distinct in the actual-size bust frames. The rendered performance reads as displeased/disgusted grimacing. It is less anatomically specific than the painted source.

## Visual limitations

The source panel has an independently raised/curled upper lip. The existing rig cannot reproduce that anatomy: purse lowers both contours and opening moves the lower lip farther down. This candidate does not claim an upper-lip lift or use a smile control to simulate one. Rigid lash/hair overlap edges and small mouth contour edges remain visible in the magnified crop; the lash/hair seams are inherited, not newly painted assets. The gaze, head and body stay still by design.

## Validation

- Native static capture: 6,978 assertions passed. Native motion: 7,546 assertions passed over 121 frames.
- All 242 native RGBA frame hashes match their capture records. Native poses match the headless numerical sequence exactly.
- Neutral first/last frames and static neutral match pixel-for-pixel. Motion pixels change only inside the bust face bounds (209,287)-(356,395); all pixels outside the conservative face box remain unchanged.
- All 1,124 frozen baseline files, including 184 PNGs, are unchanged in the candidate rig and original approved27 source. Additional candidate rig files are only recorded generated UID sidecars. The registry remains 27; EXP-093 is not registered.
- Reference sheet, catalogue and nine source panels match their documented hashes.
- Shipped MP4: H.264 yuv420p, 968×800, 121 frames at 30 fps, 4.033333 seconds, 206,530 bytes. Full decode is clean. Every decoded frame was compared against both same-index native panels and its timestamp checked. The small nearest-frame ambiguity is consistent with repeated/near-identical poses and lossy encoding, not material reordering.
- Native log contains the inherited image-import/export warning and unsupported V-Sync warning, not a failed assertion. The preparation's separate approved-EXP-063-only probe establishes the unrelated headless opening-shader warning; no runtime modification is part of this preview.

## Evidence and scope

`review_evidence/review_checks.json`, `native_frame_hashes.json`, and `decoded_frame_order.json` hold the scoped checks. `encoded_keyframes.png` shows the actual shipped encoding; `bust_progression.png` preserves the native bust viewing scale. `review_validation.py` is an original-workspace checker requiring the complete local baseline freeze and source paths; it is not a standalone portable renderer.

This independent review inspected static and decoded frames. The parent separately sampled default 1× ffplay at a 1180×812 bust-and-detail window: the open grimace/narrowed-eye peak visibly contrasted with closed-mouth/reopening-eye recovery. The player was closed and verified; see `PLAYBACK_REVIEW.json`. Neither frame inspection nor sampled playback certifies continuous observation, live engine frame pacing, lip-sync behavior, all runtime interactions, or user approval.
