# Approved39 focused native parity

PASS: 2,546/2,546 native harness checks and 726/726 exact approved RGBA comparisons across 363 checkpoints. Independent Pillow decode/rehash passed every PNG, with exact full 568x800 and detail 400x360 dimensions and exact file count.

## Scope

Full 121-frame trajectories at 30 fps for the three newly integrated approved profiles: EXP-129 Mental arithmetic, EXP-041 Controlled anger, and EXP-061 Broad surprise. This is not prior36 full-trajectory native parity, cross-transition rendering, or normal-speed live-pacing evidence.

## Supported native execution

Imported the isolated native_launcher directory through the existing Godot 4.6.3 Project Manager UI. Set Editor Settings > Run > Window Placement > Game Embed Mode to Disabled, reloaded the current project, and clicked Run Project. The standalone changing full/detail window was visibly observed. X11 display with llvmpipe (LLVM 19.1.7, 256 bits), OpenGL compatibility renderer.

The original Use Per-Project Configuration setting was restored and visually verified. The UI slot was released after completion. No shell-native launch, display-server creation, socket workaround, remote machine, CI, or publication was used.

Godot's console reported output overflow while printing the full large JSON receipt. RESULT.json was written in full before that print and independently checked; this note does not claim an error-free console.

## Preservation and receipts

All 1,396 frozen production files remained byte-identical during capture, and all 1,011 receipt-pinned native source copies matched before and after. Production was untouched. Only the isolated launcher/editor cache was opened. The approved38 preflight remains historical evidence; approved38 was not separately run after the approved39 expansion.

- RESULT.json: full native checks and expected/actual hashes.
- independent_png_verification.json: all 726 independently decoded PNG hashes and dimensions.
- source_preservation.json: production and pinned-copy preservation.
- native_preflight_baseline.json: production snapshot before native Run.
- source_copy_receipt.json: pinned copied source bytes.
- NATIVE_CAPTURE_REVIEW.json: UI execution, restoration, scope, and receipt hashes.
- verify_native_result.py: independent verification script. Run before release-only metadata finalization, since that later authorized step intentionally changes production metadata.
