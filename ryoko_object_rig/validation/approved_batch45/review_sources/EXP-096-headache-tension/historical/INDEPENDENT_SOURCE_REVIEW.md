# EXP-096 Headache tension: independent source and evidence review

**Decision: PENDING native review; UNAPPROVED.** The reference interpretation and recorded numerical implementation are coherent. They are not proof that the rendered expression reads as headache tension. Native image capture, complete review-video verification and normal-speed visual observation have not occurred.

The reviewer inspected the actual reference pixels and read the frozen rig, profile, probes and receipts. This review imports no author validator or author geometry functions. The separately owned validator reuses the established read-only evidence scaffold, with independently pinned pose vectors, key times, channel names, pressure-owner identities and lifecycle mathematics. Synthetic mutation fixtures are test data, never candidate artwork.

## Frozen input and source identity

- Author freeze: `review_input_freeze.json`, SHA-256 `6f076e4127e9c07d4083c6a26560ce32dfcb25a9d9c7981ad0401d291a509520`. All 38 members match. The reviewer embeds this literal digest rather than trusting the mutable author checksum sidecar.
- Candidate: `EXP-096.json`, SHA-256 `21ba5c4393ed672a5496ed28577068bd4b56e3b8ff5d7ac4f9674df03badf1fe`.
- Reference: `RYO_EXP-096_headache-tension_sheet_v001.png`, 1159 × 1358, SHA-256 `bafbe369788ad7274cf22c30fc2401a875ef2d8cc22ef8cc842251c740d61753`. All nine panel-file hashes agree with the catalogue and are exact lossless crops of this sheet.
- Reference catalogue: SHA-256 `ded1b313c36b66daf46f3426288ef4670b04703497323314754bba18e872b2bf`. The EXP-096 entry is copied exactly.
- The approved36 source tree and isolated rig retain all 999 pinned files, including 184 PNGs, plus the source manifest. The launcher has only the planned project configuration override among those 999 files. All 993 common runtime/artwork files match approved41. Production registry remains the original 36 profiles and excludes EXP-096.
- Reviewer work did not modify any author-frozen file, artwork, runtime, shader, profile, registry or launcher. No UI, renderer, encoder, publication, CI, paid resource or remote machine was used.

## What the actual nine-panel reference shows

KP1 is neutral. KP2 introduces a visibly pinched central brow region. KP3 and KP4 progressively narrow the ordinary eyes while the brows angle inward and the lip line tightens. KP5 and KP6 have fully closed eyes with continuing brow tension and a small pressed, slightly downturned mouth. KP7 releases most of that brow and mouth tension **while the eyes remain closed**. KP8 reopens; KP9 returns toward neutral.

That ordering is the strongest source cue. It is not a smile-eye sequence, an open-mouth grimace or a sideways look. The static panels do not prescribe frame timing, velocity or a four-second duration. The candidate's four-second smoothstep sequence is a newly authored interpretation, not recovered source motion. The catalogue's proposed 1.9-second timing is not the implemented duration.

## Numerical interpretation and geometry

The reviewer pins eleven key times and eight unique anchors independently of the JSON being tested. The eight active channels are two vertical brow controls, two opposed rigid brow tilts, ordinary blink_L/R, mouth_lip_press and mouth_purse. The other 22 shared channels remain zero.

| Time | Anchor | Brow height | Inward tilt magnitude | Ordinary bilateral closure | Lip pressure | Purse |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 0–0.20 | neutral | 0 | 0 | 0 | 0 | 0 |
| 0.60 | tension_onset | −.12 | .20 | .12 | .12 | .01 |
| 1.00 | heavy_build | −.30 | .40 | .38 | .32 | .025 |
| 1.30 | close_build | −.45 | .55 | .70 | .50 | .04 |
| 1.60–2.40 | headache_peak | −.55 | .65 | 1 | .65 | .05 |
| 2.80 | soften_closed | −.12 | .12 | 1 | .08 | 0 |
| 3.20 | reopen | −.04 | .035 | .18 | 0 | 0 |
| 3.70–4.00 | neutral_return | 0 | 0 | 0 | 0 | 0 |

Both brows use the listed height. Screen-left tilt is positive and screen-right negative. Blink names are character-sided: blink_R drives the screen-left eye and blink_L the screen-right.

Independent recomputation of all 121 recorded poses agrees within `2.915e-8`. Closure is monotonic through frame 48; the peak is held through frame 72; both eyes stay fully closed through frame 84 (2.8 seconds), when brow/lip tension is already softened. Reopening follows rather than accompanying the initial relaxation. Exact neutral holds occur at frames 0–6 and 111–120. Every active control step is less than .20.

At the peak, the rigid brow pivots translate down 5.5 source pixels and rotate +5.2/−5.2 degrees. Each ordinary upper lash travels 36 source pixels. The frozen outer-anchor coordinates and recorded pivots/rotations agree with the independent calculations at all eight static anchors. Iris sprite and shader offsets remain zero. All 14 named pressure owners have the correct amount and visibility at every static and motion sample.

The mouth remains sealed: zero central aperture throughout. Purse .05 moves each side inward .7 source pixels, reducing width from 71 to 69.6 pixels. The common upper/lower contour shifts down .2 pixels at the center and .6 at both endpoints. At bust scale, total width reduction is only .686 pixels and the endpoint-to-center vertical difference is .196 pixels. This is a subtle existing-contour adjustment, not independently authored downturned corners.

### Important fidelity limits

The frozen rig has no true central forehead furrows, horizontal brow convergence, local brow reshaping or independent downturned mouth corners. Rigid lowering and opposing rotations cannot reconstruct the source's actual knit. The purse moves the whole sealed lip contour and does not create a new frown anatomy. Existing lip-pressure shading does not establish that a native rendered mouth reads as the reference's small tense line.

The candidate may therefore read as closed-eye irritation, concentration or a generic tense pause rather than headache. Its numerical intent is reasonable, but the absent detail must remain disclosed. No native likeness, seam quality, forehead tension, corner shape or semantic success is approved here.

## Distinction from the three closest references

The reviewer viewed all three comparison sheets at their actual pixels and verified their catalogue hashes and dimensions, not merely their names.

- **EXP-043 Silent Fury:** the reference keeps the eyes open under more aggressive inward brows and a thin mouth. Its approved profile uses open neutral lids with brow height −.95, tilt magnitude 1 and pressure 1. Headache adds sustained full closure and a still-closed release, with smaller brow/pressure values. Maximum normalized control difference is 1.0; all-channel RMS difference is .210384. Similar eyebrow/mouth ingredients alone do not prove semantic separation.
- **EXP-174 Sleepy Annoyance:** the reference holds partly open heavy eyes with a visibly compact pout. Its profile peaks at closure .4, brow height −1, tilt magnitude 1 and purse .75, without lip pressure. Headache closes fully and uses pressure .65 with only .05 purse. Maximum normalized control difference is .76128; RMS is .193588. The much smaller purse avoids claiming a lower-lip pout that is not the Headache source intent.
- **EXP-177 Meditative Calm:** the reference closes the eyes with relaxed brows and a neutral, softly sealed mouth. Its approved profile acts only on ordinary lids. Headache's tense closed peak differs numerically through the brow and pressure channels; maximum difference is .65 and RMS is .163911. The deliberately relaxed, still-closed KP7 may resemble calm in isolation. Native review must judge the entire tense-build/hold/release sequence, not demand that every late recovery frame look unique.

All 36 approved baseline trajectories are numerically distinct at 121 normalized samples. The author's separate check covers nine additional candidates; this reviewer independently recalculates the frozen 36-profile baseline, including the three comparisons above. Neither result establishes perceptual distinctness.

Comparison source hashes:

- Silent Fury, 1159 × 1358: `57b55f0be62381608fbdb42b40d620f0eb7135b87f69c8f88e1d911570cb7134`.
- Sleepy Annoyance, 1254 × 1254: `cd149911dfd8c7309f25ed828772e739f6a79f859e824b69c98a0c87281cfcca`.
- Meditative Calm, 1254 × 1254: `793f57f3bdfb9974dcd076d5e84af20c356e15d0c98db0b2985e3ab65eeb731b`.

## Lifecycle and evidence checks

The reviewer independently evaluates the shared .30-second restart blend from the interrupted displayed pose and .45-second release blend to zero at nine interruption times: .35, .6, 1, 1.6, 2.4, 2.8, 3.2, 3.5 and 3.7 seconds. All 252 recorded samples, their order and 7,560 scalar values match. Maximum restart error is `4.036e-8`; maximum release error is `4.472e-8`. Release endpoints are exactly neutral.

These are calculations against frozen recorded samples. Immediate trigger continuity, actual object reset and fixed head/body transforms are covered by the author's frozen probe assertions, not a second live engine execution by this reviewer. There is no native-pixel or normal-speed lifecycle claim.

The author receipts report 1,806 static assertions and 16,260 motion assertions, including 36 lifecycle continuity/reset checks. Their identities, status, expected counts, baseline/profile hashes and lack of native hashes are verified. Headless receipts cannot be relabeled as native evidence.

The reviewer-owned validator additionally prepares strict future checks for:

- All 16 static RGBA PNGs at 568 × 800 bust and 400 × 360 detail dimensions; exact eight anchor names and neutral equality.
- All 242 motion PNGs, exact 0000–0120 filenames/order, native dimensions, RGBA hashes against native capture receipts, exact static-to-motion anchors, neutral holds, unchanged peak pixels and all full-view pixels outside the face box remaining fixed.
- Current native receipt identities, exact 1,838/16,745 successful capture counts, non-headless display/renderer and independent trajectories/lifecycle.
- The entire 968 × 800 H.264 yuv420p MP4 decoded to RGB, 121 frames at 30 fps, approximately 4.033 seconds, all timestamps, clean decoder exit and every frame compared to its same-index full/detail native source.
- All-frame nearest-face comparisons to detect material frame reordering. Identical or near-identical hold frames remain ambiguous under lossy encoding; no stronger order claim is made.
- Incomplete evidence returns PENDING/2; malformed/stale evidence returns FAIL/1. Partial corrupt PNGs and unexpected filenames are failures even when other capture files are missing.

## Results and blocker

`independent_review_validation.py` returned **PENDING, exit 2, zero failures**, with all **40 available checks passing**. It found 17 missing static inputs (16 PNGs and receipt), 243 missing motion inputs (242 PNGs and receipt) and no review MP4.

`test_independent_review_validation.py` passed **72 reviewer tests**. Coverage includes source/input-freeze identity, exact vectors/times, mirrored lids/brows, closed-through-KP7 timing, geometry/pressure owners, numerical lifecycle, neutral/body/hash/anchor corruption, native dimensions, full-decode helper, timing/order errors, stale receipts, safe output paths and missing-native behavior. Pixel and decoder tests use synthetic/mocked fixtures; they do not count as native capture or actual MP4 review.

**Pending action:** native capture of this frozen candidate, encoding only after capture passes, and continuous normal-speed visual review against the references. No capture action was attempted or denied. This assignment is headless/read-only review; native inputs are absent, so those checks cannot yet run. No evidence was fabricated and no graphics or authorization workaround was used.

The next native reviewer should inspect the full-closure tension, tiny mouth read, lash/iris closure and seams, fixed body, exact neutral return, and especially relaxation at 2.8 seconds before reopening. Compare the complete sequence with Silent Fury, Sleepy Annoyance and Meditative Calm at native bust and detail scale. User/source-art acceptance is not animation approval.

Run the current read-only checks with:

    python independent_review_validation.py
    python -m unittest test_independent_review_validation -v
    python verify_input_freeze.py

Reports are in `independent_review_evidence/review_checks.json` and `partial_review.json`; test details are in `independent_reviewer_tests.log`. These are reviewer-owned outputs excluded from the author freeze. **No production integration or publication is approved by this review.**
