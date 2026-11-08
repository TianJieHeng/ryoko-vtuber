# EXP-164 single bounded timing A/B verdict

**Recommend the exact pinned 3.47-second alternative for final capture.** Its KP2 time is **.4436559139784946**, the proportional compression in the actual probe, not the rounded .44 example in the earlier analysis. No additional variant or full preflight repeat is requested by this review.

The choice trades a modestly faster first sink and recovery for shorter unheld hesitations while preserving every accepted pose and all purposeful catches. It does not assert that faster motion is inherently smoother, that the zero tangents are gone, or that normal-speed playback was observed.

## Actual risk comparison

I inspected every regular 30 Hz viewer eye/brow sample in the affected original and alternative spans, plus the adjacent largest-lash-step pairs at actual native and viewer sizes. These are actual saved shared-player frames, not interpolated comparison images.

**Lingering is reduced:**

- At KP2, the captured regular samples within closure ±.01 of .44 decrease from **3 to 2**. Exact profile inversion gives **97.58→73.45 ms** in that band.
- At KP8, the captured regular samples within closure ±.01 of .07 decrease from **6 to 4**. Exact profile inversion gives **169.55→127.17 ms**.
- These are declared diagnostic bands, not perceptual thresholds or literal frozen holds. The intermediate keys still have instantaneous zero velocity. The alternative shortens that effect; it does not repair the shared interpolation or erase every easing beat.

**Edge steps grow, and were examined rather than assumed harmless:**

- First-sink maximum actual 30 Hz upper-lash step: **.920365→1.310191 viewer pixels**, +42.4%. Native step: about **1.878→2.674 pixels**. Maximum brow rotation step: **1.17156→1.66779°**; brow center step: **.47279→.67285 native pixels**.
- Final-recovery maximum lash step: **.241381→.320635 viewer pixels**, +32.8%. Native step: about **.493→.654 pixels**. Maximum brow rotation step: **.38812→.51555°**; brow center step: **.19668→.26121 native pixels**.
- The early first-sink increase is larger than simple 33% time compression because the unchanged .30 s restart envelope overlaps that interval. The audit evaluates actual controls and rendered edges, so this effect is included.
- The first-sink largest pair is .2333→.2667 s in the alternative, versus .2667→.3000 s in the original. Native and viewer crops show a larger but coherent eyelid displacement, without a new contour replacement, opening/closing snap, changed hair occlusion or unexpected brow reversal.
- Recovery remains a small subpixel-per-frame viewer change at its maximum. The two short recovery arcs no longer spend as many captured samples close to the intermediate pose, without adding a visibly different facial shape.

For context, the already retained first effortful reopening has a maximum sampled viewer lash step of **3.00354 pixels**. The alternative's first sink still lasts **.70 s**, versus **.20 s** for that reopening. The source's slow heavy descent followed by a firmer reopening therefore remains distinct. The .08 s deep catch, .08 s second-sink catch, .16/.14 s reopening rests and .12/.16 s neutral rests all retain their exact durations. The shallower second sink, two different reopens, residual droop and sealed-mouth downturn are not reauthored by this option.

The saved evidence supports selecting the shorter option for the final capture. It does not support calling the first sink a completely continuous-velocity arc, a measured perceptual smoothness improvement, or an exact recovery of source timing. The timing remains a newly authored interpretation of static panels.

## Independent integrity results

`AB_CHECKS_AND_METRICS.json` records **18,155 passed independent checks**:

- All **58 alternative actual states / 116 PNG and RGBA hashes** and dimensions.
- Independently calculated actual smoothstep plus restart controls at every checkpoint.
- All **nine accepted source anchor images are pixel-exact at both native and viewer scales**.
- Every original 537-file candidate input remains byte-exact.
- Every alternative runtime input from that original file set is byte-exact except `expressions/EXP-164.json`.
- The only profile changes are duration and key timestamps. All fifteen value vectors and phase labels are identical. All explicit hold durations are preserved.
- Native and viewer framing, fixed anatomical scale/opacity and unchanged pixels outside the eye/brow/mouth regions pass.
- The reused original affected-span images were independently hash-checked again.

Pinned identities:

- Original profile: `6631b955105a84c64d6fca331bdea2a032e52a7d6dbc4159f13e369c92604581`.
- Alternative profile: `528c012c64beaf22ded0bba98cb7a63a3cab14c8133af1b63707e22d44df485c`.
- Probe plan: `5c217aca726b1d75d7e6f1761f9a3f26432ef00280833f72481d97e340492c25`.
- Capture receipt: `ab21f8b7ba51fef31ec95dea841eb06b2afd107ccd31d4ffc8ea1a9644bfc1a2`.
- Builder capture assertion count: **38,683**, zero failures.

## Use of this decision

The alternative is still an isolated diagnostic profile. On coordinator selection, promote the exact pinned timestamps and update inherited 3.90-second timing prose, provenance, tests and final capture expectations to 3.47 seconds. Keep the immutable original as the comparison record. This review did not edit either profile.

The full final capture/lifecycle review is still needed for the selected timeline. This bounded A/B did not run a complete alternative cycle or all interruption, retrigger and auto-blink chapters. In particular, the captured final recovery reaches exact neutral pixels during the final hold; natural idle completion at 3.47 belongs in the final gate. The unchanged middle spans and generic release mechanism remain supported by the preceding original preflight and unchanged code, but are not falsely described as newly captured here.

**Normal-speed observation remains unperformed**, as in the prior bounded reviews. It is not an extra tool prerequisite. No final-performance, user-approval, publication, push, AI, TTS or socket claim is made.

## Evidence paths

- `fighting_sleep_independent_review/timing_ab/AB_CHECKS_AND_METRICS.json`
- `fighting_sleep_independent_review/timing_ab/audit_ab.py`
- `fighting_sleep_independent_review/timing_ab/original_first_sink_all30hz.png`
- `fighting_sleep_independent_review/timing_ab/alternative_first_sink_all30hz.png`
- `fighting_sleep_independent_review/timing_ab/original_final_recovery_all30hz.png`
- `fighting_sleep_independent_review/timing_ab/alternative_final_recovery_all30hz.png`
- `fighting_sleep_independent_review/timing_ab/first_sink_largest_actual_steps.png`
- `fighting_sleep_independent_review/timing_ab/final_recovery_largest_actual_steps.png`
- Actual alternative captures: `fighting_sleep_scope_work/timing_ab_probe/capture/{native,full}/`
- Immutable original captures: `fighting_sleep_scope_work/trajectory_evidence/preflight_capture/{native,full}/`

The reviewer used no display/CUA, wrote no runtime/profile/artwork and made no Git or Library writes. Only isolated audit scripts, comparison crops and receipts were written. The builder reported its display lease released.
