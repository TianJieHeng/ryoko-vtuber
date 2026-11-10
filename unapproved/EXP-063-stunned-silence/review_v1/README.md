# Stunned silence: unapproved motion review v1

EXP-063 is next in the historical reference catalogue after EXP-125 and already-approved EXP-186. This is a new review candidate, not an approved production expression. Production approved24 is b5d2d30229d20829d21a85abb8df5e16938263f6.

Source sheet SHA256: 4a256631c867855772cd169d2b13ac652adde74331ca8cea9a1d0fbbafa61823. The static sheet shows raised brows, fixed wide centered eyes, slightly parted lips, a frozen hold, then recovery. This new four-second interpretation uses unchanged approved24 artwork and existing bounded opening/lip controls. Eye widening is subtler than the painted source, and mouth contours are approximate. No smile, head, neck, body, gaze or blush acting, tears or new anatomy. Existing outer-lash/hair seam limitations remain unchanged. The catalogue's 1.9-second timing was a reference proposal, not recovered animation.

Static fitting uses five in-memory probe definitions through the shared registry because opening_px is deliberately scoped to timeline playback. Static headless and native captures each passed 34 checks. Timeline state, restart/release/reset and neutral-return tests passed 629 headless checks. Native evidence and independent visual review are recorded in REVIEW_RESULT.json and REVIEW.md. Interrupted transitions are state-tested, not rendered; continuous live playback pacing is not claimed.

The MP4 presents full bust and face detail at 968x800, H.264, 30 fps, 121 endpoint-inclusive frames (4.033333 seconds). The extra endpoint frame is neutral. This candidate awaits user approval.

Reproduce with the approved24 rig: place EXP-063.json beside render_motion.gd. Run Godot --headless --path PATH_TO_RIG --script ABSOLUTE_PATH_TO_RENDER_MOTION for state checks, or native gl_compatibility with -- --capture for frames. Run encode_preview.py afterward. run_gate.py --rig PATH_TO_RIG --capture performs the isolated-pose study. Neither harness changes the production registry on disk. No CI or paid resources were used.
