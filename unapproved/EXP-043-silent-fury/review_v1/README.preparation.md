# Silent Fury EXP-043: unapproved review candidate

Prepared from the verified approved27 integration snapshot at commit 816d77fafb6e016dc70f0802743d444e618f7b0f. All 1,124 frozen files, including 184 PNGs, are unchanged. One import-generated UID sidecar is recorded separately. The production registry contains 27 profiles and does not contain EXP-043. No runtime, shader, artwork, production profile or registry was edited.

The reference sheet was visually inspected. Peak has inward-sloping brows, visible amber irises and thin closed lips. This data-only approximation lowers the whole brows 9.5 source pixels, tilts them by opposing eight degrees and uses existing full lip pressure. Neutral eye opening is preserved. No local brow knitting, horizontal brow convergence, nose creases or jaw tightening is supported. Four-second timing is newly interpreted, not recovered source animation.

Headless verification: 816 static pose/geometry checks and 7,541 temporal checks pass, including bounded controls, excluded controls, fixed body, exact neutral, restart and release continuity, and byte-identical on-disk registry. Source-preservation checks pass. The inherited caught-staring loader produces the same raw-image export warning as other candidates; no export is attempted.

Native capture and normal-speed review are still required. Nothing is approved or published.

From this folder, with the native desktop display available:

    python run_gate.py --rig rig --capture
    sh run_motion.sh --capture
    python encode_preview.py

These commands preserve existing captures by refusing overwrite. The MP4 is Silent_fury_review_v1.mp4, 30 fps, 121 frames, with bust and detail views. Inspect at normal speed and bust scale, including lip edges, brow/eye collision and exact neutral return. The encoding script does not perform rendering. Library delivery remains pending successful native review.
