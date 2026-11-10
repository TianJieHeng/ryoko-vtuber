# EXP-061 Broad surprise: unapproved preparation v1

Prepared locally against approved36 commit `3ce98774282ad6c20dfbd7018d20838ff861b762`. This is a new current-shared-rig candidate, not historical sprite-composite acceptance or animation approval. No production, disk registry, runtime or art edits. No publication.

## Evidence and fit

Actual 1254×1254 sheet inspected before authoring, located through `insight_integration_work/avatar_build_assets/reference_library/metadata/expressions.json`. `SOURCE_REFERENCE.json` preserves the catalogue entry, sheet hash, observations and comparisons. Both brows rise as the open mouth and eyes build to panel 5, then soften. Timing is a new four-second interpretation, not recovered animation.

Only existing whole-brow vertical movement, bounded upper-eye opening, split-lip mouth opening, purse and pressure are used. At peak: both whole brows travel up 10 source pixels, upper opening is 4 pixels, central lip gap is 27.735 source pixels (13.59015 bust pixels). Lower-eye expansion and a true dropped jaw/chin silhouette are unsupported. Broad rounded mouth is partial fit with existing parts, not anatomical reproduction. Body/head, gaze and blink stay fixed; no new controls, shaders, anatomy or artwork.

Shocked Gasp EXP064 uses quick inner-brow rotation with stationary outer anchors, more purse (.7 versus .32) and a smaller residual gasp. This candidate gradually raises whole brows, reaches a less-pinched broad opening at 1.35 seconds and holds/eases through 2.35 seconds. Delighted Discovery EXP004 converts round opening to a spread smile; this candidate never smiles or spreads. They share open-surprise vocabulary, so perceptual distinctness still requires actual native visual review.

## Completed numerical checks

- 999 pinned source files, 184 source PNGs and 36 approved profiles copied, plus the approved manifest. `BASELINE_FREEZE.json` pins all source/reference hashes.
- `state_checks.json`: PASS, 838 checks on eight anchors, including actual brow travel/rotation/scale, eye opening, central lip gap, excluded controls, exact resets and fixed body.
- `motion_state_checks.json`: PASS, 9,023 checks, 121 states at 30 fps across four seconds, neutral holds, symmetric brows, distinctive temporal profile, bounded frame steps and restart/release/reset tests at nine times.
- `preparation_verification.json`: pinned originals/copy and reference catalogue/art unchanged. Candidate only registered in memory by probes, never written to the registry.
- GUI Node wrapper scripts parse successfully; native renderer and GUI have NOT run for this candidate. Strict image guards require full 568×800 and detail 400×360. Eight anchors would generate sixteen stills; motion would generate 121 full and 121 detail images.

Headless logs contain the shared upper-opening shader compiler custom-sampler diagnostic and shared image-loader export warning. Numerical PASS does not validate native rendering or export. Initial headless tests crashed because inherited XDG paths pointed outside the workspace; the successful `run_state.sh` explicitly uses workspace-local HOME/XDG directories. No permission escalation or display/server workaround was attempted.

## Prepared GUI handoff, not executed

Project: `native_launcher/project.godot`

Unique GUI name: **Ryoko EXP061 Broad Surprise PREVIEW ONLY**

Scene: `native_launcher/launcher.tscn`, Node `BroadSurprise061ReviewLauncher`.

The launcher refuses existing capture/motion output, captures static first, checks PASS before motion and preserves dimensional guards. Use only the parent's scheduled supported Godot UI workflow, after approved36 parity and Controlled Anger EXP041. `GameEmbedModeDisabled` with editor reload is managed/restored by the GUI worker. No shell-native launch, Terminal workaround, Xorg/socket/server attempts or remote execution.

Pending: native rendering, pixel guards/neutral check in real renderer, visual inspection, normal-speed playback, independent review, user preview and approval. Do not mark approved or publish this preparation.

## Native evidence update, 2026-11-10

Native standalone capture and MP4 encoding are now complete. Static 870 checks and motion 9,508 checks pass; final independent evidence validation passes. See `NATIVE_CAPTURE_REVIEW.md` and `PLAYBACK_REVIEW.json` for actual pixel review, sampled Kdenlive playback and limitations. The initial configuration byte-identity failure caused by Godot formatting is preserved and resolved by exact restoration, not a weakened guard. The candidate remains **UNAPPROVED** and is not integrated. The preparation sections above record the earlier pre-capture state.
