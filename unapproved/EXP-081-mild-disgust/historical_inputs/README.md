# EXP-081 Mild Disgust: unapproved shared-rig candidate

This is an isolated data-only candidate against frozen approved36 commit `3ce98774282ad6c20dfbd7018d20838ff861b762`. All 999 manifest-pinned files, including 184 PNGs, remain exact in the source and `rig/` copy. Both available manifest copies are also retained. Candidate and probes are registered only in memory, outside the unchanged 36-profile disk registry.

A direct local comparison to the published39 tree confirms 993 common files remain identical, including runtime scripts, scenes, shaders, asset metadata and artwork. Only the six documented registry/release/readme/aggregate-validation files differ in that newer tree. No current runtime changes were needed or made.

## Source and interpretation

The actual 1213 × 1296 EXP-081 nine-panel sheet was viewed before authoring. Catalogue, sheet and all nine panel hashes are recorded. Separate pixel checks confirm every linked panel is a lossless crop of that sheet. `SOURCE_CATALOGUE_ENTRY.json` preserves the actual record, and `SOURCE_REFERENCE.json` records observations and limits.

The source gathers unequal brow and eyelid tension, lifts one side of the upper lip at the peak, closes the mouth while retaining the objection, then relaxes. This four-second interpretation uses eight static anchors and eleven timeline keys:

- 0.00–0.20: neutral lead-in.
- 0.20–0.60: screen-left brow lowers first; uneven lids begin narrowing.
- 0.60–1.00: a small common mouth-corner bias and purse enter.
- 1.00–1.40: build to a brief, slightly parted asymmetric response.
- 1.40–1.75: hold the restrained peak.
- 1.75–2.15: lips seal while unequal brow/lid tension persists.
- 2.15–2.70: mouth-side bias releases before the brow.
- 2.70–3.70: soften and return exactly to neutral; hold through 4.00.

This is newly authored timing from static references, not recovered motion or an approved animation. There are 121 endpoint-inclusive samples at 30 Hz.

## Deliberate limits and distinction

- There is **no independent upper-lip lift/curl or nose-wrinkle control**. The existing screen-right corner control moves BOTH upper and lower contours together. It cannot reproduce the painted one-sided upper-lip anatomy.
- Peak common upper-contour offsets are −2.4 source pixels at screen-right and +1.44 at screen-left. The central lip gap is 5.2164 source pixels, or 2.556036 at bust scale. This is a small split-lip aperture, not jaw rotation or a true asymmetric aperture.
- Purse narrows both sides symmetrically. Sealed-only width controls remain zero even after closure, avoiding invalid transitions. No new anatomy, shader, texture or runtime is introduced.
- Head tilt/recoil, cheek deformation, body gestures, breathing, sound and facial effects are omitted. They are never claimed as simulated. Gaze stays forward and the head/body remain still.
- Brow/corner names use screen sides. Blink names use character sides: `blink_R` narrows screen-left; `blink_L` narrows screen-right. Geometry tests verify this mapping.
- Unlike Bitter Taste, the response is mild and asymmetric, with only a brief small opening. Unlike Queasy, it has no inner-brow lift or lip pressure. There is no full blink or smile-eye action. Numerical comparisons cover the 36 frozen profiles plus five later candidates.
- A common corner lift can read as objection or a restrained smirk. Numeric difference is not proof of perceptual distinction or source fidelity. This remains a disclosed partial approximation requiring native review.

## Passed headless preparation

- **1,526 static assertions**: bounds, pose requests, actual brow translation/rotation, lash travel and iris closure, fixed gaze/body, lip geometry and mouth domain, exact reset, unchanged registry.
- **11,330 motion assertions** across every sample: actual geometry, bounded controls/steps, source-specific timing, exact neutral and disk registry preservation. This total includes **36 lifecycle assertions at nine interruption times**.
- **8,421 separate Python assertions**, including independent smoothstep, static brow/lash/lip formulas, every timeline sample and aperture, source-specific timing, neutral holds and lifecycle evidence. Maximum control error is below 1.5e-8. All nine source panel crops are pixel-exact.
- **20 encoder guard unit tests** and **11 independent-audit unit/mutation tests** pass. These use temporary receipts/mocked pixels or copies of numerical records, never generated preview art.
- Headless Godot 4.6.3 import and script parse checks pass. The separate launcher has one intentional pinned override: its project name/main scene. The other 998 baseline launcher files and both manifests remain exact.
- Generated static and motion launcher scripts match the documented probe transformation byte for byte. Strict capture dimensions are checked before any PNG save.

An initial independent audit used an overly tight translation threshold for Godot's single-precision Vector2 values. The corrected 0.0001-source-pixel tolerance is documented with the original failure in `development_audit/`. No profile/runtime change was made for that correction. The frozen runtime emits its inherited Image-load warning for `uneasy_clear_parting.png`; it was not suppressed or changed.

Re-run only headless work from this directory:

    sh run_motion.sh --state
    python verify_preparation.py
    python independent_geometry.py
    python -m unittest discover -s . -p 'test_*.py' -v

`run_motion.sh` supports headless state checks only. Re-running checks changes log/receipt bytes and therefore requires a new review-input freeze if their hashes change. Do not overwrite previous native evidence.

## Native review still pending

The prepared project is `native_launcher/project.godot`, named **Ryoko EXP081 Mild Disgust PREVIEW ONLY**. This preparation did not launch it natively. Under separate authorization, use the existing native Godot UI to run that project. It captures eight static anchors and then all 121 motion samples, refusing existing capture/motion directories.

Both probes require actual bust/full size **568 × 800** and detail **400 × 360**. Embedded-game settings can ignore requested sizes; receipt dimensions are the gate. Preserve any failed capture and resolve settings through the permitted UI before a fresh attempt. No display server or socket workaround is provided.

After successful native captures, `python encode_preview.py` can create `Mild_disgust_review_v1.mp4`. It rejects missing or headless receipts, changed profile/plan/baseline hashes, wrong dimensions/modes, incomplete frames, incorrect timeline or pixel hashes, wrong neutral return and existing video. Expected output is 968 × 800 at 30 fps, approximately 4.033 seconds for all 121 endpoint-inclusive frames.

**No native capture or video exists at preparation completion.** Native frame inspection, source-fidelity review, normal-speed observation, independent review and user approval are pending. No production integration, publication, CI, paid resource, remote-machine execution or hardware action occurred.
