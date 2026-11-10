# EXP-081 Mild Disgust: independent source and preparation review

## Decision

**Suitable for a limited native preview; UNAPPROVED.** No numerical, source-preservation or preparation blocker was found against the frozen inputs. The candidate follows the source's unequal brow/lid tension, brief asymmetric mouth response, closed-mouth objection and release.

The central fidelity limit is material: **the common screen-right corner control moves both lip contours together. It does not independently lift or curl the upper lip.** The aperture remains spatially symmetric. This can provide a side-biased objection but cannot reproduce the source's upper-lip anatomy or nose/cheek deformation. It may read as a restrained smirk or skepticism rather than unmistakable disgust. If complete anatomical reproduction is required, this preparation does not meet that criterion.

This is a source and numerical review, not a native visual pass, normal-speed viewing claim, user approval, integration approval or publication approval. Native capture was absent at this review checkpoint. The separate capture operator owns that pending work.

## Independently examined inputs

- Opened and inspected the actual **1213 × 1296** nine-panel EXP-081 sheet. SHA-256: `833980ce5d88d6e4cbc53a396380b971ac09de745ddbe93ebc99028d8cf82592`.
- Independently recomputed all nine linked panel hashes and checked that each is a pixel-exact integer crop from the sheet. Verified exact catalogue-entry equality and the complete catalogue hash, not only the author's source summary.
- Final `review_input_freeze.json` SHA-256: `22509ab2bf568edc6291e261fc0310bdac3818bbc08f4db6656be9ee30748086`. All **46** frozen preparation/evidence files match.
- Candidate SHA-256: `4a6783b9232217ed468f626dc36e5c4c43dc0a5a284108a210ef1975496e1dd9`. Read the eleven-key profile, eight-anchor plan, static/motion probes, 121 headless records, shared mouth/brow/lid formulas and object pivots.
- The intended baseline is **approved36**, published commit `3ce98774282ad6c20dfbd7018d20838ff861b762`. All **999** pinned files, including **184 PNGs**, match in the source baseline and copied rig. The additional approved manifest matches. All 36 registry IDs remain exact and EXP-081 is absent from the disk registry.
- The launcher preserves 998 pinned files and the additional manifest. Its sole pinned-file override is `project.godot`, separately frozen with its unique preview title and launcher scene.
- Independently checked the **993** common runtime/artwork files against approved39. Only the six explicitly listed registry, release/status, readme and aggregate-validation files are excluded. This is runtime/artwork parity, not a claim that approved36 and approved39 registries are identical.
- Independently sampled all 36 baseline profiles plus Mental arithmetic, Controlled anger, Broad surprise, Puzzled and Open sobbing. Also viewed the actual Bitter taste and Queasy reference sheets and their existing native peak-detail images for comparative context. Their paths and hashes are in `review_evidence/comparison_sources.json`; this is not a fresh complete audit of those prior previews.

## Source interpretation

The nine-panel Mild Disgust sheet starts neutral. Panels 2–4 gather uneven brow and eyelid tension. The screen-left eye becomes more narrowed, while the central brow shape becomes less neutral. Panel 5 contains the strongest one-sided mouth response: the screen-right side rises and the lips part, with the opposing side comparatively low. Panel 6 closes the mouth while keeping asymmetric tension. Panels 7–8 relax and panel 9 returns toward neutral.

The catalogue says “One brow lowers; eyes narrow; upper lip lifts slightly on one side.” It does not specify which side in that sentence. Its general convention is character sides; the candidate explicitly uses screen-side brow/corner names and character-side blink names. Those are not interchangeable: `blink_R` narrows the **screen-left** eye. Both candidate brows lower, but screen-left moves substantially more, a disclosed and plausible dominant-brow interpretation rather than literal single-brow isolation.

The four-second timing is newly authored from static references. The catalogue's 1.9-second schedule is explicitly proposed, not implemented or recovered motion. The candidate holds neutral through 0.20 seconds, establishes brow/lid tension at 0.60, begins a small closed-mouth corner bias by 1.00, reaches a briefly parted peak from 1.40–1.75, seals the mouth at 2.15, drops the corner bias by 2.70 and settles to exact neutral by 3.70 through 4.00.

Head recoil/tilt, nose wrinkle, cheek deformation and the separately paired BOD-008 stop-palm and BOD-027 dismissive-wave references are not implemented. No voice, breathing or speech performance is supplied. This must remain described as a facial-only partial approximation.

## Existing controls and measurable limits

### Brows and eyes

At peak, screen-left/right vertical brow values are −0.44/−0.12: **4.4/1.2 source pixels downward**. Legacy tilt values +0.22/−0.10 produce **+1.76°/−0.80°** rotations. No inner-brow lift, inward pull or painted brow deformation is added. Independent pivot/rotation/anchor checks match the static records within the justified `1e-4` source-pixel tolerance for float Vector2 storage.

Ordinary blink values are 0.34/0.18 for screen-left/right. The recorded upper-lash travel is **12.24/6.48 source pixels**, with matching iris closure. This is mild partial closure, not a full blink, smile-eye or newly drawn disgust lid. Gaze remains forward. The degree of visible asymmetry beneath the unchanged hair and lashes needs native inspection.

### Mouth

Peak opening 0.18, purse 0.12 and screen-right common-corner lift 0.32 yield:

- Central gap **5.2164 source pixels**, or **2.556036 bust pixels** at scale 0.49.
- Symmetric horizontal endpoint movement **+1.68/−1.68 source pixels** and nominal mouth width **67.64 source pixels**. The center does not translate.
- Upper-contour endpoint offsets **+1.44** at screen-left and **−2.40** at screen-right. The corner-to-corner bias is 3.84 source pixels.
- The lower contour has the **same 3.84-pixel side bias** because corner lift is common to both contours. Left/right aperture gaps remain equal; the opening is not anatomically one-sided.

Purse additionally drops the common center contour by 0.48 source pixels. These are geometry measurements, not measured visible tooth or cavity dimensions. No upper-lip-only curl, independent nose movement or jaw rotation can be inferred from them.

The lips seal while asymmetric objection remains, then corner bias disappears before the brow settles. Sealed-only width controls stay zero throughout, including when closed. Global/left corner lift, smile, spread, lip pressure, oral lift, kiss, uneasy opening, blush and hair motion are zero. Absence of smile controls alone cannot prove that the common corner will not look like a smirk.

## Distinction from Bitter Taste and Queasy

**Bitter taste / EXP-093:** Its reference sheet has a broader, more bilateral downturned response, with the upper lip rising while the lower pulls down. The frozen profile lowers both brows to −1, tilts them +0.70/−0.70, uses equal 0.40 lids and an opening of 0.45 with purse 0.35. It has no unilateral corner lift. Its central peak gap is 12.84 source pixels, versus Mild Disgust's 5.2164, and its mouth remains open later before sealing at 2.65. Mild Disgust's milder dominant brow, unequal lids, short small opening and side-biased common contour are numerically different. The normalized-time maximum difference is approximately **0.903623**. Neither profile fully reproduces independent source upper-lip anatomy.

**Queasy / EXP-090:** Its source emphasizes raised inner brows, heavy lids, pressed-forward lips and cheek tension. The frozen profile has inner-lift 0.68/0.60, equal 0.44 lids, purse 0.72 and pressure 1.0, with no mouth opening or unilateral corner lift. Mild Disgust uses no inner lift or pressure and instead briefly parts the mouth with asymmetric low-brow tension. The normalized-time maximum difference is **1.0**.

All **41** independently sampled comparison profiles have a different active-control set and a nonzero trajectory difference. These raw mixed-channel differences establish numerical nonduplication only; they are not perceptual distances. The existing Bitter/Queasy native detail images also demonstrate why anatomy and emotional readability must be judged from pixels rather than control names. Mild Disgust itself still needs direct native comparison, particularly for disgust versus smirk, skeptical objection, generalized annoyance and aftertaste.

## Independent validator and tests

`review_validation.py` never starts Godot, a renderer, UI, encoder, integration or publication. It reads frozen inputs and any future native evidence, writing only reviewer reports/contact sheets under `review_evidence/` by default.

At this checkpoint, the validator returns **PENDING (exit 2)** with **32/32 available checks passing**, no failures and three pending categories. Its independent smoothstep maximum control error is `1.4507828549614743e-08`. All eight static pose/geometry records and all 121 recorded poses and central gaps agree with separate Python calculations. Per-frame actual brow/lash/iris checks are author probe assertions; the independent review recomputes actual recorded static geometry and the motion pose/gap records rather than inventing unavailable per-frame transform records.

**32/32 independent validator tests pass; 63/63 combined Python tests pass.** Tests use temporary or in-memory synthetic fixtures, never substitute them for native artwork. They cover failed/missing receipts, altered freeze identity, wrong dimensions/modes, ordering/nonfinite/channel changes, wrong blink side, full-blink substitution, symmetric-brow substitution, forbidden inner lift/pressure/smile, corner-side reversal, an upper-only rather than common-lip offset, incorrect geometry/gaps, neutral/peak mutations, suppression and release timing, and exact-grid anchor selection. No author frozen file was modified.

The validator has Mild Disgust-specific values, counts, anchors, limits and mouth math. It does not inherit Open Sobbing's full squeeze, inner lift, sob aperture, second catch, twelve keys or nine anchors, or Puzzled's sealed-mouth width assertions.

Once native evidence exists it additionally checks:

1. All **16 static PNGs**, exact names, 568 × 800 bust and 400 × 360 detail, RGBA mode, SHA-256/pixel hashes, matching records and source hashes, exact neutral return and fixed pixels outside the face box.
2. All **121 full plus 121 detail** PNGs, exact frame filenames, every receipt-bound raw RGBA hash, 121 ordered times/poses, native renderer/display identity, bounded motion, exact neutral holds, fixed body pixels and the held peak at frames 42–52.
3. Exact static/motion pixel correspondence only at aligned anchors: neutral 0, detect 18, recoil 30, peak 42, release 81 and neutral return 120. Suppress at 2.15 and settle at 3.25 are half-frame anchors and are intentionally not compared to different nearby samples.
4. Expected native assertion totals of **1,558 static** and **11,815 motion**, including **36 lifecycle checks at nine interruption times**, against the unchanged approved36 source.
5. Complete H.264 MP4 decode: 968 × 800, yuv420p, all 121 frames at 30 fps, monotonic timestamps, approximately 4.033 seconds, every decoded full/detail panel compared with its same-index native source, and all-frame nearest-face checks for material reordering. Lossy encoding leaves identical or near-identical holds ambiguous; the report says so.

## Capture blockers and next step

Native evidence is **pending, not denied**: 17 required static files and 243 required motion files including receipts are absent, and no Mild Disgust review MP4 exists at this checkpoint. Consequently native dimensions, pixels, seams, perceptual distinction, full MP4 decode and continuous normal-speed observation have not passed or been claimed.

The separate capture operator has the frozen launcher and an exact pre-import project backup. Run only through the permitted native workflow. If the editor rewrites `project.godot`, preserve that rewrite/diff and restore the frozen bytes only after editor closure through the operator's workflow; do not weaken this identity guard. Preserve failed captures rather than overwriting them. Then rerun `python mild_disgust_work/review_validation.py`, inspect both bust/detail native and decoded pixels, and explicitly evaluate the disclosed smirk/upper-lip limitation. Keep EXP-081 UNAPPROVED pending user review.
