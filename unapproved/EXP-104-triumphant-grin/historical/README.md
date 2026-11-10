# EXP-104 Triumphant Grin: unapproved shared-rig candidate

This is an isolated, data-only preparation using the frozen approved36 baseline at commit `3ce98774282ad6c20dfbd7018d20838ff861b762`. All 999 manifest-pinned files, including 184 PNGs, remain byte-exact in both the source and `rig/` copy. Both available manifests are retained. The production disk registry still contains exactly its original 36 profiles. Static probes and EXP-104 are registered only in memory.

Local comparisons also preserve all 993 common runtime/artwork files against `approved40_integration_work` and `approved41_integration_work`. Six newer registry/release/readme/aggregate-validation files are explicitly excluded from that comparison. No runtime, artwork, shader, control, source-reference or production registry change was made.

## Actual reference and interpretation

The actual 1159 × 1358 nine-panel EXP-104 sheet was inspected before authoring. `SOURCE_CATALOGUE_ENTRY.json` retains the complete catalogue entry. `SOURCE_REFERENCE.json` records the sheet, catalogue, nine panel hashes, observations and limitations. The separate Python check confirms all nine panels are exact lossless crops of that sheet.

The source develops bilateral lowered inward-angled brows, forward focused eyes and a centered smile. Panel 5 has a wide tooth-showing grin; panel 6 opens it further. Panels 7–9 recover. This candidate uses the existing equal brow-height controls, mirrored brow tilts, equal ordinary partial lid closure, legacy smile/spread and modest mouth opening. No new feature or anatomy is introduced.

Eight static anchors define an eleven-key, four-second interpretation:

- 0.00–0.20: exact neutral lead-in.
- 0.60: low inward-angled brows and a sealed emerging smile.
- 1.00: focused grin develops with shallow lip parting.
- 1.60–2.00: centered shallow tooth-grin hold.
- 2.40: a somewhat more open grin.
- 2.80: smile, aperture and brow tension recover together.
- 3.20: lips reseal while a small residual smile and brow tension remain.
- 3.70–4.00: exact neutral hold.

Timing is newly authored from static art, not recovered motion. All 121 endpoint-inclusive samples are checked at 30 Hz. The unchanged smoothstep sampler has zero velocity at joins. An in-memory restart also uses the existing 0.30-second transition.

## Supported approximation and exclusions

The tooth-grin uses brow height −0.32 on both sides, inward tilts +0.42/−0.42, equal 0.12 lid closure, 0.84 smile, 0.86 public spread and 0.30 mouth opening. The later open grin uses −0.30 height, +0.40/−0.40 tilts, 0.10 closure, 0.88 smile, 0.90 spread and 0.46 opening.

Effective internal spread is the product of public spread and smile, not public spread alone. At the tooth-grin this gives 28.896 source pixels of additional mouth width, an 8.91-source-pixel central aperture and equal −9.28368-source-pixel corner lift. At the later open grin the added width is 31.68 pixels and aperture is 13.662 pixels. Bust scale is 0.49. Rigid tooth support follows those existing controls passively, with its actual node positions, rotations and visibility flags checked. A visibility flag is not evidence of visible enamel pixels.

The original upper tooth arch and spread support are used unchanged. **No independent dental control, exact opposing tooth-row anatomy or true clenched-teeth shape is implemented or claimed.** The candidate is a shallow open tooth-bearing grin rather than a sealed clench. There is no jaw rotation, cheek deformation, new lower-teeth anatomy, smile-eye closing, gaze shift, inner-brow lift, independent corner bias, purse, lip pressure, sealed-only width, blush, head/body motion, hair motion, speech or effect.

Brow names use screen sides. Positive screen-left and negative screen-right tilt lower the inner ends symmetrically. Blink names use character sides: `blink_R` closes screen-left and `blink_L` closes screen-right. Both ordinary lid channels remain equal.

- EXP-114 Daring Provocation has unequal lids, opposed brow heights and a crooked corner-biased grin. EXP-104 is bilateral and centered.
- EXP-152 Private Pride is downcast and sealed. EXP-104 looks directly forward and opens its grin.
- EXP-001 Bright Welcome raises its brows and reaches 0.80 opening. EXP-104 lowers/inward-angles its brows and peaks at 0.46 opening.
- Numeric comparisons against 36 baseline and seven subsequent candidate profiles establish nonduplicate trajectories only. They do not establish perceptual distinction or reference fidelity.

## Headless preparation verification

- 1,582 static assertions check requested/excluded channels, scope, bounds, actual brow/lash/lip geometry, smile-coupled spread and tooth support, fixed gaze/body, exact reset and registry preservation.
- 12,646 motion assertions cover all 121 samples, the shallow hold followed by the more open grin, symmetry, monotone opening/recovery, exact neutral and 36 lifecycle assertions at nine interruption points.
- 8,544 separate Python numerical checks reproduce geometry and smoothstep sampling. Maximum control error is below 1.48e-8. All nine reference panels match exact source crops.
- 47 unit tests pass: 20 encoder guards, 17 numerical mutation checks and 10 source/launcher guards. Tests use synthetic temporary receipts where appropriate, never synthetic review artwork.
- Headless Godot 4.6.3 imports and three generated launcher scripts parse successfully. The frozen runtime's inherited warning about direct loading `uneasy_clear_parting.png` is retained, not suppressed or fixed.
- One initial probe failed because `is_equal_approx` on a tiny lash displacement was tighter than the float32 position subtraction error. The final static check uses the same explicit 0.0001-source-pixel tolerance as the independent and timeline geometry checks. Original failed receipts are preserved under `development_audit/`; no rig/control/pose change was needed.

The Python files named `independent_geometry` are a separate mathematical implementation by the candidate author. They are not independent reviewer sign-off. No reviewer-owned files were copied or pinned by this preparation.

Run existing prepared checks from this directory:

    sh run_motion.sh --state
    python verify_preparation.py
    python independent_geometry.py
    python source_guards.py
    python -m unittest discover -s . -p 'test_*.py' -v
    python verify_input_freeze.py

Re-running writes numeric receipts/logs and requires an explicit new handoff freeze if bytes change. `verify_input_freeze.py` itself is read-only. `prepare_candidate.py` creates a new baseline/data preparation and refuses an existing rig. `prepare_native_launcher.py` creates the separate launcher and refuses an existing launcher. The construction adapter under `development_audit/` is an archival authoring aid, not a supported regeneration entry point; the prepared files are authoritative.

## Separate native launcher, unexecuted

Project: `native_launcher/project.godot`

Unique name: **Ryoko EXP104 Triumphant Grin PREVIEW ONLY**

Its sole baseline-file override is the project name/main scene. The other 998 pinned baseline files and both manifests remain exact. Generated wrappers match the original probe-to-node transformation byte for byte. The launcher refuses an existing `capture/` or `motion/` directory.

Under separate authorization, the native Godot UI may run this project to capture eight static anchors and all 121 motion samples. Actual full/bust size must be **568 × 800** and detail size **400 × 360**. Both probes gate PNG writes on actual captured dimensions, not merely the requested viewport size. Preserve any failed evidence before correcting settings through the authorized UI. No display server, socket or shell-rendering workaround is supplied.

Only after native capture passes may `python encode_preview.py` create `TriumphantGrin_review_v1.mp4`. The encoder rejects missing, headless, failed, stale or mismatched receipts; wrong dimensions/modes; missing/extra frames; wrong frame order/times; pixel-hash mismatches; failed neutral return; and existing video output. Target video is 968 × 800, 30 fps, 121 frames, about 4.033 seconds including both endpoints. Current preflight correctly stops because native evidence does not exist.

**No native capture, MP4, normal-speed observation, independent visual review or user approval exists at this handoff.** Visible tooth exposure, mouth seams, focused eyes, full/detail crop fidelity and perceptual distinction remain pending. No UI/native shell launch, display server/socket work, remote execution, CI, paid resource, production integration or publication occurred.
