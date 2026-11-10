# Sudden insight: unapproved motion review v1

EXP-125 is the next entry after EXP-040 in the historical reference catalogue. This is a new review candidate, not an approved production expression. Production remains approved23 at 1ab3a90d8737c4a06c42e2f4fb790e07dace417d.

The source sheet SHA256 is ead8eab6687291e65c98067cebcc0886b932218a940955523882c862dd62fd66. It shows brightened brows/eyes, rounded realization, open pleased smile and a small sealed smile. This newly authored 3.6-second interpretation uses existing bounded opening and lip controls, unchanged artwork and unchanged shared runtime. Eye widening is subtler and the open smile toothier/flatter than the painted source. No head, neck, body, gaze or blush acting, tears or new anatomy. Existing eye/hair seam artifacts remain baseline limitations. The catalogue 1.9-second timing was a reference proposal, not recovered animation.

Static fitting used five in-memory probe definitions through the shared registry because opening_px is deliberately a timeline-only scoped channel, not a manual apply_controls input. An initial manual harness attempt was rejected, then corrected to use the supported registered-player route. A second pose study rounded the realization mouth using existing purse/press/oral-lift controls. The exported plan.json is that final study, not the earlier flat-mouth probe.

Final headless timeline/lifecycle validation passed 569 checks. Native OpenGL/Mesa llvmpipe capture passed 788 checks across 109 endpoint-inclusive frames. Neutral return is byte-exact in both views. All frame pixel changes remain in the face. Restart/release/reset passed state checks at five interruption times; rendered interruption clips and live runtime pacing are not claimed. An independent review found no new seam or anatomy defects in sampled native frames.

Sudden_Insight_review_v1.mp4 contains bust and face detail at 968x800, H.264, 30 fps, 109 frames, 3.633333 seconds. Full decoding passes. The one extra endpoint frame is a neutral hold. The user has not approved this candidate.

Reproduce with the approved23 rig: place EXP-125.json beside render_motion.gd. Run Godot --headless --path PATH_TO_RIG --script ABSOLUTE_PATH_TO_RENDER_MOTION for state checks, or native gl_compatibility with -- --capture for frames. Run encode_preview.py afterwards. run_gate.py --rig PATH_TO_RIG --capture performs the final isolated-pose study. Neither harness changes the production registry on disk. No CI or paid resources were used.
