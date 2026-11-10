# EXP-041 Controlled anger: unapproved current shared-rig candidate

Baseline is approved36 commit 3ce98774282ad6c20dfbd7018d20838ff861b762: 999 pinned source files, 184 PNGs, 36 registered profiles. Candidate and probes register only in memory. All baseline and frozen rig source bytes, art and registry remain unchanged. Existing historical approved sprite-composite EXP-041 art is not approval for this newly authored shared-rig performance.

The actual nine-panel reference sheet was inspected before authoring. Narrow fixed eyes, brows drawing down toward the center and a thin, restrained closed mouth support this interpretation. Existing rigid controls cannot converge the brows horizontally: vertical lowering and opposing rotation approximate that cue. There is no new anatomy, art, runtime, gaze, head or body motion.

The four-second authored performance has a measured onset, moderate inward/downward brow peak, symmetric narrow lids and lip pressure. After the still held peak, pressure eases while eyes/brows remain fixed, then all controls settle to exact neutral. This interpretation is not recovered source animation. Cold Glare uses no added brow tilt and a small purse. Silent Fury uses neutral lids and maximum brow tilt/lip pressure. Controlled anger combines narrower fixed eyes with moderate tilt/pressure and its own staged release.

Reproduce numerical checks with `sh run_checks.sh`. Coverage includes eight isolated anchors; actual brow and lash transforms and lip-pressure shader state; 121 samples at 30fps; exact neutral holds/reset; bounded frame increments; fixed body/gaze; restart, release and reset at nine points; source/registry hash preservation. Numerical checks do not prove visual fidelity.

An initial headless attempt omitted XDG directory overrides and failed while creating application data. The reproducible runner sets all HOME/XDG paths inside this work folder. Initial static checks also exposed float32 subtraction error of 0.0000134 source pixels at the final small lash displacement; the geometry assertion now uses the same absolute 0.0001-pixel precision as the brow-position check. No rig or candidate values were changed to mask a behavior failure. Baseline image-loading export warning is unchanged; this is a native editor review, not an export validation.

## Native capture handoff

Open `native_launcher/project.godot`, uniquely named Ryoko EXP-041 Controlled Anger Review, through the existing supported desktop Godot UI. The separate launcher is a clean source copy, not a copied .godot cache. Locally generated import caches are preparation output only. The wrapper uses Node and runs static then motion capture without modifying the frozen rig.

Set Editor Settings > Run > Window Placement > Game Embed Mode to Disabled, reload the current project through the UI, and Run Project. Restore the previous setting afterward. Do not start a display server, shell-native renderer, remote execution or AF_UNIX workaround. The parent coordinates the shared native UI slot. Existing capture/motion folders cause an intentional refusal to overwrite.

Strict PNG pre-save guards require full/bust 568×800 and detail 400×360. After successful native receipts, run `python encode_preview.py` for the labeled side-by-side MP4. The encoder independently verifies dimensions for all 242 frames, native receipt success and exact frame membership before encoding. Native capture, pixel review, normal-speed playback and user approval are still pending. Do not publish or add EXP-041 to the production registry.
