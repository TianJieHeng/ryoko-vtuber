# EXP-104 Triumphant Grin native capture review

## Result

The isolated candidate has complete native and encoded technical evidence. It remains **UNAPPROVED**. No production integration, Library upload or publication was performed.

- `TriumphantGrin_review_v1.mp4`: 187,963 bytes; SHA-256 `caa4914959146c87fa371a17e829ca3c5d85b4db4a273b341f62781a8b33d17b`.
- H.264/yuv420p; 968 × 800; 30 fps; 121 endpoint-inclusive frames; 4.033333 seconds.
- Native static: eight anchors, 16 PNGs, 1,614 assertions, zero failures.
- Native motion: 121 full and 121 detail PNGs, 13,131 assertions, zero failures. X11 / llvmpipe (LLVM 19.1.7, 256 bits).
- Native RGBA full/bust dimensions are exactly 568 × 800 and detail dimensions exactly 400 × 360.
- Unchanged author encoder's `validate_capture` and complete FFmpeg decode pass. Receipt: `native_capture_audit/author_native_validation.json`.
- Unchanged independent validator: **94/94 checks PASS**, no failures or pending checks. Report: `independent_native_review_evidence/review_checks.json`.
- All 105 combined unit tests pass before and after capture. All 8 independently frozen reviewer files remain exact.

## Native route and preservation

The existing Godot Project Manager imported the exact `native_launcher` directory using its native file chooser. The editor's original Game Embed Mode was visibly **Use Per-Project Configuration**. It was temporarily set to **Disabled**. The editor was closed/reopened during menu navigation, and then **Reload Current Project** was explicitly selected and its restart observed before F5. The standalone debug window was observed at 568 × 800. The unchanged launcher completed all static and motion captures on the first run, with no failed native capture discarded.

After the completed capture, F8 stopped the run. During restoration, one menu selection briefly displayed Make Game Workspace Floating; no capture was run in that mode. The original **Use Per-Project Configuration** was then selected and visibly verified. The candidate editor exited to the Project Manager, observed through the window inventory and desktop screenshot, before original project bytes were restored. An unrelated preexisting Controlled Anger editor was not changed.

Godot moved the `[editor]` section ahead of `[rendering]` and added its normal blank line. No setting values changed. The rewrite, exact diff, failed author freeze/source-guard checks, and failed independent review remain under `native_capture_audit/`. No freeze or validator was weakened. The original saved project bytes were restored after editor exit; the final author freeze and source guard pass. The exact original launcher project SHA-256 is `320bd93799e972fb219ccb8e74430b9d02de9ca2c888a5509e39d1c839120c24`.

Only supported CUA controls were used for native Godot and Kdenlive operations. No native-shell launch, display-server, socket, remote-machine, CI or paid-resource workaround was used. Encoding and validation consumed only already captured native files. No source artwork, rig runtime, profile, capture wrapper or production registry was changed.

## Pixel review and decode coverage

The actual EXP-104 nine-panel source and EXP-114, EXP-152 and EXP-001 comparator source sheets were inspected. Native inspection covered all eight static detail anchors, full/bust progression at frames 0/30/48/84 and nine decoded detail anchors at 0/18/30/48/60/72/84/96/120. These are actual capture/decoded pixels, not invented or rerendered evidence.

The independent validator completely decoded all 121 video frames with clean exit and empty stderr. All same-index full/detail panels and frame timestamps were checked, including nearest-face comparisons for material reordering. Identical/near-identical held frames remain ambiguous under lossy encoding. Mean full/detail errors on the 0–255 scale are 1.29178 and 2.04319; maxima are 1.29420 and 2.06922. Static/motion anchors match exactly, neutral holds and return are exact, the shallow grin hold is exact, and all full-view pixels outside the face region remain unchanged.

The centered tooth-bearing grin is visible, with a shallow held grin followed by a slightly more open smile. Eyes remain directed forward and similarly narrowed, and the mouth broadens symmetrically. This reads as a confident, focused smile. The source has a more emphatic broad tooth-showing grin and stronger inward brow tension; this native version is softer and less intensely triumphant. The mouth uses the existing upper tooth arch, with thin bright lines and segmented tooth outlines. It does not reproduce an exact opposing-teeth clench, new dental anatomy, cheek deformation or jaw rotation. Fine jagged/stitched-looking pixels at hair/lash boundaries are visible in the unchanged neutral and remain noticeable in detail views; no seam-free claim is made.

Relative to the inspected sources/profiles, the candidate is centered rather than EXP-114's crooked unequal-eye challenge, direct and open rather than EXP-152's downcast sealed pride, and lower-brow/more restrained than EXP-001's raised-brow welcome. Native videos for those three comparators were not available in the inspected approved36 parity captures, so this is not a formal native perceptual A/B pass.

## Playback status

The encoded clip was loaded into existing Kdenlive at its unchanged 30 fps. Normal Play was initiated from 00:00:00:00 and the 00:00:04:00 neutral endpoint was observed. This initial observation sampled only the endpoint; additional moving/peak samples are pending. There is no continuous uninterrupted observation or user approval claim.
