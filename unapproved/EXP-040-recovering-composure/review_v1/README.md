# Recovering composure: unapproved motion review v1

This is an unapproved review candidate, not an addition to the production registry. It uses the approved22 rig from cbe1feab48143cabbe8196912bb767f9c2276c33, without changing runtime, artwork or existing profiles.

A newly authored 6.2-second arc: neutral, gathering distress, collecting oneself, tiny brave smile, neutral return. It interprets the source sheet with existing bounded controls only. Tears, blush and head/body movement are omitted. Canonical eye/hair seam artifacts are inherited baseline limitations. The source panels are not an animation.

The in-memory review catalogue adds EXP-040 only for testing. No approval is implied. Headless lifecycle validation passed 958 checks. Native OpenGL/Mesa llvmpipe capture passed 1,333 checks across 187 endpoint-inclusive frames, with exact neutral object/pixel return, continuous restart/release and reset at five interruption points. Five keyframes match the earlier isolated pose captures. An independent visual review found no candidate-specific blocker. Live runtime pacing and continuous normal-speed observation remain unverified.

The H.264 review MP4 includes bust and face-detail views. It decodes fully, at 968x800, 30 fps, 187 frames, 6.233333 seconds (one endpoint hold frame). REVIEW_RESULT.json records its checksum and validation summary.

Reproduction: use run_gate.py with --rig pointing to the approved rig for static checks. Run render_motion.gd using Godot --headless for state validation, or a functioning native gl_compatibility renderer with -- --capture for PNG frames. EXP-040.json must sit beside the script. This is a review harness, not a production integration. Encode with encode_preview.py, adjusting workspace paths as needed. No CI or paid resources were used.

During recovery the first harness accumulated 1/30 deltas and stopped infinitesimally before the duration, leaving expression ownership active despite zero controls. Sampling by absolute target time corrected the harness; no shared runtime change was needed. Final headless and native reruns passed.
