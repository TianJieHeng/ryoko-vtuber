# Delighted Discovery EXP-004 independent review

PASS for review delivery, not user approval or integration.

The small open discovery transitions into a clear broad smile at bust size. Eyes stay open through the smile. The layered result is toothier than the painted reference, and the source's whole-eye expansion and mouth contours are approximations. No obvious new lip break or displaced tongue was seen in the inspected static and decoded phases. Existing lash/hair edge seams remain visible in the detail view.

This is similar to approved Sudden Insight's round-to-smile vocabulary. The distinction is a brighter, broader held smile: EXP-004 holds opening 2.5, brow lift 0.6, mouth opening 0.7, smile 1.0 and spread 0.8. Approved EXP-125 holds opening 0, brow lift 0.18, mouth opening 0.6, smile 0.8 and spread 0.6. Its later release uses blink 0.08, not closed eyes. The README comparison was corrected; original preparation README preserved. Profile and frozen scripts are unchanged.

Validation:
- All 1,124 frozen files and 184 PNGs match both the candidate rig and approved27 baseline. Registry remains 27 and excludes EXP-004.
- Source sheet, catalogue and nine panel hashes match. Candidate freeze has no changed files.
- Native static 489 and motion 7,178 assertions pass. Native logs contain warnings but no ERROR lines.
- All 242 native RGBA hashes match their capture records. All 121 native poses match headless records. Exact neutral bookends and static peak match; pixels outside the face region remain unchanged.
- MP4 has 121 frames at 30 fps, 968×800, H.264/yuv420p, 4.033333 seconds. Full decode succeeds. Frame timestamps and both panels match chronological source frames within lossy compression tolerance.
- Parent sampled default 1× ffplay at 1180×812 bust/detail size, observing intermediate opening and broad smile; mouth action was clear, with eyes open. Player closure verified. This is sampled playback, not continuous viewing or live engine pacing certification.

Evidence: review_evidence/review_checks.json, native_frame_hashes.json, decoded_frame_order.json and inspected contact sheets. Reproduction uses the original local baseline/source paths; these evidence checks are not a standalone portable renderer.
