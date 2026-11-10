# EXP-061 Broad Surprise: independent source review

**Decision: UNAPPROVED. Source-aware preparation is coherent and numerically distinct, but native appearance, perceptual distinction, and playback are still pending.**

Review date: 2026-11-10 UTC. Review scope is the files in `broad_surprise_work`, the pinned approved36 source, the actual EXP061 reference-sheet pixels, and existing EXP064/EXP004 comparator pixels. This review did not launch Godot, a renderer, a display server, or UI; change any profile, runtime, artwork, baseline, or registry; or publish anything.

## Evidence actually inspected

- `SOURCE_REFERENCE.json` and the actual 1254 × 1254 EXP061 nine-panel PNG at its recorded path. Verified SHA-256: `91df47914f1bd8301b9adbd5b6e98c03621d4239b72883f46d6a309d8c46b043`.
- `EXP-061.json`, all eight static anchors in `plan.json`, `README.md`, both capture/state probe scripts, and the prepared Node launcher scripts.
- `state_checks.json`: existing reported PASS, 838 checks and eight anchor records. Independently recomputed requested poses, brow displacement/rotation, upper-opening values and central lip gap from those records.
- `motion_state_checks.json`: existing reported PASS, 9,023 checks and 121 ordered states. Independently recomputed smoothstep plus the existing 0.30-second restart blend. Maximum control error was **2.8423027931268052e-08**. All six-channel, symmetry, timing, aperture, neutral-hold and bounded-step assertions pass.
- Current `rig/expressions/EXP-064.json` and `EXP-004.json`, plus actual existing `shocked_gasp_work/capture/shocked_gasp_detail.png`, `delighted_discovery_work/capture/round_discovery_detail.png`, and `delighted_discovery_work/capture/delighted_discovery_detail.png`. These are historical comparator captures, not fresh approved36 parity evidence or candidate captures.
- Baseline registry and approved integration status establish EXP064 and EXP004 as members of the approved36 set. Historical `UNAPPROVED` strings inside their preserved original profile JSON are not the current integration approval record.

## Reference fidelity

The inspected sheet starts with the neutral/narrower eye shape and closed lips, then shows a small mouth opening, increasingly lifted brows and rounder/wider eyes. Panel 5 is the clearest peak: both brows are high, the eyes are visibly more exposed, and the mouth is an open rounded cavity. Panel 6 reduces the mouth opening while retaining the alert eyes; panels 7–9 return toward neutral. It is surprise without the upturned spread smile of delight.

The candidate follows that broad relationship: symmetric whole-brow rise and increasing upper-eye opening accompany an opening mouth, followed by coordinated release. It uses no smile, spread, inner-only brow lift, gaze, blink, hair or body action. This is a reasonable semantic translation within the existing controls.

It is **not a close anatomical reproduction** of the reference:

- The rig opens the upper eye region by at most four source pixels. It does not reproduce full upper/lower-eye expansion or a changed iris/pupil treatment. The existing comparator captures show why a bounded upper-opening control should not be described as the source's fully rounded eyes.
- At peak, both whole brows translate upward by 10 source pixels without rotation or scale changes. This plausibly conveys bilateral surprise, but the exact painted brow shape cannot be inferred from translation alone.
- The 27.735-source-pixel central split-lip gap (13.59015 pixels at bust scale) approximates an open mouth. There is no jaw/chin drop, new oral anatomy or changing face silhouette. A broad rounded contour is a hypothesis until candidate pixels are seen.
- BOD-020 and BOD-036 are separate suggested gesture references in the catalogue. Neither is implemented or validated here. The fixed head/body is an intentional facial-only limit.
- The source supplies nine static references with proposed 1.9-second timing, not an animation. The candidate's new four-second interpretation, especially the 1.35–1.85 peak and slow easing through 2.35, is an authored performance choice rather than recovered source timing.

## Distinction from approved expressions

### EXP064 Shocked Gasp

The data has concrete differences: whole-brow vertical travel instead of inner-brow rotation about fixed outer anchors; peak at 1.35 seconds rather than 0.66; mouth purse 0.32 rather than 0.70; and an aperture that stays large through 2.35 instead of dropping to the smaller residual gasp around 1.55–2.25. The existing EXP064 peak image was inspected and has a compact open-mouth/raised-inner-brow read.

The overlap is material: both use the same painted eye and mouth parts, both reach four-pixel upper opening, and mouth-open weights are 0.95 versus 0.90. The central lip-gap difference is only **2.055 source pixels, approximately 1.007 bust pixels**. That numerical increase alone cannot establish a visually broader mouth or a distinct expression. Brow motion, less purse and timing must do most of the work. **Risk of perceptual overlap remains unresolved** until full-size and detail captures and normal-speed playback can be compared.

### EXP004 Delighted Discovery

The early raised-brow/open-eye/rounded-mouth vocabulary overlaps. The stronger distinction is the sustained performance: EXP004 transforms into a spread smile (smile 1.0, spread 0.8), visibly present in its inspected held-delight capture. EXP061 has zero smile/spread throughout and retains a larger surprise aperture before release. This supports data-level nonduplication, but does not prove that the new candidate will avoid an unintended smiling read when rendered.

## Preservation findings

Fresh independent hashing found all **999 pinned files, including 184 PNGs**, unchanged in both the candidate `rig` and pinned production source. The extra approved source manifest, source sheet and source catalogue also match their frozen hashes. Both disk registries retain exactly the 36 approved IDs and exclude EXP061.

The prepared native launcher matches 998 pinned files and has the documented `project.godot` override only. Its preparation copies pinned runtime files, not the extra audit manifest; that manifest remains present and verified in `rig` and the production source. This is not a runtime/capture blocker. Candidate, plans, probes, receipts and launcher inputs reviewed here are pinned in `review_input_freeze.json` to detect later changes.

## Capture blockers and limits

At review time there is no `capture/` directory, no `motion/` directory, no native capture receipt and no `Broad_surprise_review_v1.mp4`. Native capture is **pending**, not denied or attempted by this reviewer. The parent's scheduled supported Godot GUI workflow owns it. No alternate launch route was attempted.

The existing headless logs report the shared custom-sampler shader diagnostic and image-loader export warning. State PASS does not demonstrate successful GPU rendering or export. The prepared launcher also refuses to overwrite an existing capture/motion directory, so any partial run must be preserved and evaluated before retrying. Strict dimensions are 568 × 800 full and 400 × 360 detail.

No native candidate pixels, visual source-match decision, normal-speed continuous viewing, interruption playback, live-engine pacing, lip-sync compatibility, body gestures, export support, fresh approved36 parity, integration or approval are claimed by this report.

## Read-only validation deliverable

`review_validation.py` adapts the Mental Arithmetic evidence review to EXP061. It only reads inputs, runs `ffprobe`/`ffmpeg` decoding, and writes review reports/contact sheets. It never starts a renderer, encodes or modifies input images, changes the rig, or publishes.

Default invocation:

```text
python broad_surprise_work/review_validation.py
```

If the delivered MP4 has another filename, pass `--video PATH`. Expected review-video geometry is 968 × 800, with the native full panel at x=0 and the native detail panel at x=568, y=220. A different layout requires deliberate validator adaptation, not guessed crops.

When captures arrive it checks all 16 stills, all 242 native motion PNGs, all 121 pose/time records, exact ordered filenames, native dimensions and RGBA data hashes, exact neutral holds/bookends, fixed pixels outside the face box, sustained-peak pixels, and static/motion identity at exact sample anchors. It independently recomputes the timeline instead of only trusting PASS receipts. The MP4 path checks the full 121-frame decode, all 30 fps timestamps, same-index panel similarity and nearest-frame face errors; it exports selected decoded pixels for inspection. The latter is lossy frame-order evidence, not proof of unique ordering among identical holds or a substitute for continuous playback review.

Current execution returns **exit 2 / PENDING**, with no failed available checks. It explicitly lists 17 missing static files, 243 missing motion files and the absent review video, and sets `independent_checks_pass` false. Seven helper tests pass, covering timeline math, exact peak/neutral interpolation, out-of-order records, non-finite values, forbidden controls, image dimension/mode guards and out-of-face changes. Full native frame and MP4 stages are implemented but **not yet exercised on EXP061 evidence**.

Outputs: `review_evidence/review_checks.json`, `review_evidence/partial_review.json`, and `review_evidence/validator_unit_tests.log`. Future successful evidence checks do not change the candidate's **UNAPPROVED** status.
