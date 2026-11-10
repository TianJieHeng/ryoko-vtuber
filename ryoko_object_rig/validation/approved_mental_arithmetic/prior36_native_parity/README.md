# Approved36 focused native parity recovery

PASS: 731/731 harness checks; 180/180 exact native RGBA comparisons at 90 sampled checkpoints across the nine newly approved profiles. Independent Pillow decode/rehash also passed all 180 images, with exact full 568x800 and detail 400x360 dimensions.

Executed through supported existing Godot 4.6.3 desktop UI: import isolated project, disable Game Embed Mode, reload project, run standalone visibly. X11 display; llvmpipe (LLVM 19.1.7, 256 bits) OpenGL compatibility renderer. Original Use Per-Project Configuration preference restored and visually verified. No shell-native launch, Xorg creation, sockets, remote machines, CI or publication.

All 999 manifest-pinned source files verified before copy and after capture; production untouched. Isolated project changes only launcher.gd, launcher.tscn, project.godot; editor-generated cache/imports remain isolated. Captures and receipts outside production.

Scope: ten checkpoint poses for each newly approved profile, not all 36 full trajectories, not prior27 native parity, and not evidence of normal-speed live pacing. Exact expected/actual hashes: RESULT.json. Independent decoded PNG hashes/dimensions: independent_png_verification.json. Source receipts: source_copy_receipt.json and source_preservation.json.
