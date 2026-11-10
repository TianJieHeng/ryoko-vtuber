# Quiet Contentment EXP-003: unapproved review v1

The 4.6-second candidate has been rendered and delivered for review. It is not approved or integrated. Approved main remains 816d77fafb6e016dc70f0802743d444e618f7b0f (27 expressions).

The revised v002 reference closes the eyes at the peak despite the catalogue wording “half relax.” This performance follows those pixels: gentle eye settling, a closed-eye hold, reopening and a deliberately tiny symmetrical smile. The half-relaxed alternative is a static probe only. Timing and control values are newly authored interpretations. No body motion, new anatomy, runtime changes or artwork changes were made.

## Completed validation

- Native static: 4,193 assertions passed; native motion: 8,943 assertions passed.
- Headless static 4,179, motion/lifecycle 8,664, dense sampler 316,256 assertions passed.
- Independent review verified all 278 native frame hashes, 139 chronological decoded frames, exact neutral return and fixed body. All 1,124 baseline files and 184 PNGs remained unchanged.
- MP4: H.264, 968×800, 30 fps, 139 endpoint-inclusive frames, 4.633333 seconds, 213,730 bytes; full decode passed.
- Sampled phases in normal 1× ffplay playback at bust viewing size showed visible eye settling/reopening. This is not continuous observation or live engine pacing certification.

The closed-eye shape approximates rather than traces the source anatomy. Existing lash/hair seams remain visible in detail. The smile is intentionally subtle. Export packaging, live lip-sync and the complete production release suite were not tested. No CI was run.

## Reproduction

Use a checkout of the approved baseline commit above. Copy its `ryoko_object_rig` directory into this review folder as `rig`, excluding generated `.godot` caches. Import the copied project with the existing Godot 4.6.3 installation before capture. Keep the candidate outside the production registry; the harness injects it only in memory. Run from this folder on the supported native desktop:

    python3 -B run_gate.py --rig rig --capture
    sh run_motion.sh --capture
    python3 -B encode_preview.py

Capture and encoding refuse to overwrite existing outputs. Inspect static poses before motion capture. `build_candidate.py` can reproduce the data-only candidate; `test_candidate.gd` contains dense constraints. This review snapshot includes compact portable baseline metadata, not the original broad filesystem inventory. Original-workspace preservation checks and preparation receipts are historical results, not a standalone release certification. The copied baseline includes local generated UID metadata in the original workspace; a fresh checkout/import may differ in auxiliary metadata without changing approved artwork/runtime. `README.preparation.md` is explicitly historical and contains pre-capture statements.

See REVIEW.md, REVIEW_SUMMARY.json, PLAYBACK_REVIEW.json and scoped review evidence. Approval and integration remain separate.
