# Focused determination v2 review backup

**UNAPPROVED.** This backup adds only `unapproved/EXP-139-focused-determination/review_v2/` on `review/exp139-focused-determination-v2`. It is not a production profile, acceptance decision or integration. V1 was judged too subtle. V2 uses the stronger C pose and a newly authored onset blink. See [the review](REVIEW.md) and [the preview](motion_study/Focused_determination_review_v2.mp4).

## Completed evidence and later documentation correction

Native captures passed 600 static, 592 onset and 63,948 motion checks. Headless motion passed 63,705 checks. The independent image/sequence review passed 42 checks and verified all 121 encoded frames against a chronological reconstruction. Desktop playback was sampled at normal speed; continuous perception and live engine pacing are not certified. User approval remains pending.

The original review receipt verified all 28 files in `STATIC_ALTERNATIVES_FREEZE.json`. `README.md` was subsequently amended to report completed motion review instead of leaving a stale pending-motion statement. The final state has 27 unchanged frozen static files and that one documentation-only difference. The original freeze and review receipt were retained, rather than rewritten to hide the change. The final inventory rechecks the entire frozen rig, frozen v1 files and frozen static files. `MOTION_PREPARATION.md`, `REVIEW.md` and `REVIEW_RESULT.json` also explain the amendment; they were not part of that static freeze.

The backup includes candidate source, generation and capture scripts, measured static/motion results, source and baseline manifests, the independent checker, compact review receipt, decoded frame hashes and the delivered MP4. It omits the runtime copy, caches, native frame directories, redundant comparison MP4, the broad historical v1 inventory, visual contact sheets, expanded diagnostic/reproduction inventories and most logs. The v1 preservation count is retained without exporting its full file list. Original files are retained locally. The archived original-workspace validators require those omitted inputs; this compact backup alone is not sufficient to rerun their complete historical preservation checks.

## Pinned rendering baseline

The parent commit is `816d77fafb6e016dc70f0802743d444e618f7b0f`; its `ryoko_object_rig` tree is `2ce4ba51a6dc03d11cc1b33d0935e53bffd88c54`. Rendering scripts, shaders, scenes, PNG artwork and expression profiles match the captured rig byte-for-byte. EXP-139 is not in its 27-profile production registry and is injected only in memory by the capture harness.

The captured 1,112-file freeze also contains local import/UID sidecars and historical metadata. It is not identical to a fresh checkout in every file: 836 files match the pinned repository paths, 276 differ or are local-only, and 13 repository files are absent from that capture freeze. Aside from sidecars, the differences are integration/release documentation and manifests, a validation log and an integration-verification utility, not expression rendering code or artwork. The detailed comparison is retained locally; this compact backup records the counts and rendering-relevant scope. Importing a fresh checkout can regenerate sidecars and caches; do not interpret that as reproducing the complete original workspace freeze.

## Reproduce the motion in a fresh local folder

Prerequisites: the pinned repository files, Godot 4.6.3, Python 3, FFmpeg/ffprobe and a local native desktop for capture. The original metadata checkers additionally use NumPy/Pillow and the retained source catalogue, sheet, v1 and native frame evidence. The following commands are documented reproduction instructions, not a claim that a clean-checkout rerun has already been executed.

From the repository root on this review branch, create a fresh folder so no archived evidence is overwritten:

```sh
REPO="$PWD"
P="$REPO/unapproved/EXP-139-focused-determination/review_v2"
git diff --exit-code 816d77fafb6e016dc70f0802743d444e618f7b0f -- ryoko_object_rig
WORK=$(mktemp -d)
mkdir -p "$WORK/onset_study" "$WORK/motion_study"
cp -R "$REPO/ryoko_object_rig" "$WORK/rig"
for f in BASELINE_FREEZE.json plan.json check_and_capture.gd run_gate.py; do cp "$P/$f" "$WORK/$f"; done
for f in plan.json check_and_capture.gd run_gate.py; do cp "$P/onset_study/$f" "$WORK/onset_study/$f"; done
for f in EXP-139.json poses.json render_motion.gd run_motion.sh encode_preview.py; do cp "$P/motion_study/$f" "$WORK/motion_study/$f"; done
godot --headless --editor --path "$WORK/rig" --import
python -B "$WORK/run_gate.py" --rig "$WORK/rig"
python -B "$WORK/onset_study/run_gate.py" --rig "$WORK/rig"
sh "$WORK/motion_study/run_motion.sh" --state
```

For local native capture, inspect the poses before motion and encoding:

```sh
python -B "$WORK/run_gate.py" --rig "$WORK/rig" --capture
python -B "$WORK/onset_study/run_gate.py" --rig "$WORK/rig" --capture
sh "$WORK/motion_study/run_motion.sh" --capture
python -B "$WORK/motion_study/encode_preview.py"
```

The output is `motion_study/Focused_determination_review_v2.mp4`, containing 121 chronological 30 Hz frames with bust and detail views. Exact pixels and encoding hashes can depend on the Godot, graphics and codec environment. The delivered video is H.264, 968×800, 4.033333 seconds, SHA-256 `101456109207dcc9389f9c6053bc664fbad5369dab28232c39375889991bc955`.

The source image and catalogue already live under `avatar_build_assets/reference_library/`; `SOURCE_REFERENCE.json` records their original paths and hashes. Its recorded absolute paths and the historical integrity checkers refer to the original capture workspace, not the temporary reproduction folder.

## Boundaries

No production registry, approved profile, runtime or main-branch file is changed by this backup. No PR, merge, CI, paid resource, purchase, hardware flashing or remote-machine execution is part of publication. The commit message includes `[skip ci]`. Approval and any later integration remain separate steps.
