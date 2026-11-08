# EXP-050 independent actual-performance review

## Decision

**PASS for the bounded, local EXP-050 Frustrated pout performance and its tested integration paths.** The actual stepped viewport images preserve the accepted frustrated-pout acting through onset, peak, sustained hold, broader unsmiling release and exact neutral return. No new visible mouth seam, natural-profile tooth leak, owner-activation pop or stranded pose was found.

This is technical and acting acceptance of the exact source and captured trajectory below. It is not user approval, approval of any prior unapproved expression, publication approval, final-media verification or proof of normal-speed playback. The source still contains 17 profiles, with all prior sixteen approval states unchanged and EXP-050 locally unapproved pending the user's review.

## Exact reviewed identity

- Source freeze: `c2f4d0ff703f9caf418bf2a72ff117a294730a75f0be2ae3de4ba9c24577fd8a`.
- Profile: `e1b775d34244bf1a1f05fac351170062657b0b12d11acf2edf08bf8f3ec9e630`.
- Capture plan: `9b3bfb0991d6bfe87438eb4da006e1832ed3e2161a3a35bfc902b8473dfb1e6e`.
- Capture binding: `a0d25e0b909a19f2a21c8714726858a8b431c001b7c0e2940cc37ec6efc0a031`.
- Actual capture receipt: `032d4c9f8322e106c5dd366c0dafd484a66c67f5a91b399c544b14c6a9058bc9`.
- Pre-capture independent review freeze: `cff337f3c98697be997dc384b9477b21bebc78696bd4fb998d699480728a87b9`.

One actual X11/llvmpipe run produced 541 checkpoints and 1,082 PNGs: 568×800 full presentation and 1136×1384 native presentation at each checkpoint. Its 361,534 harness checks report zero failures. The process exited and the builder released the display lease. This reviewer used no display and launched no Godot process during actual review.

## Independent evidence checks

`audit_actual_capture.py` independently verifies every actual state and mouth-bridge record against the previously independently reproduced bound preflight. All 541 match exactly. Every image's decoded RGBA hash matches its actual renderer receipt, its dimensions and mode are correct, and its PNG hash matches the separate capture verification. All recorded anatomical objects retain unit scale and full opacity.

- All 140 common timestamps in the two natural cycles are pixel-identical in both presentations.
- All nine key/duplicate-hold native images equal their accepted combined static captures exactly: neutral at 0, KP3 at 0.73, KP5 at 1.57/1.99, KP6 at 2.34/2.65, KP7 at 3.22 and neutral at 3.91/4.13 seconds.
- Every natural changed pixel is inside the bounded eye/brow or mouth regions. Hair, face base, nose, clothing, head and background do not drift.
- All sixteen chapters which specify a neutral ending return to exact full and native neutral images. Manual takeover deliberately retains its manually set purse and is pixel-stable at all three samples. The restored idle blink is exactly equal to the initially captured idle blink in both presentations.
- Near-zero entry at 1 ns through the dense tiny-onset samples, and recovery immediately before 3.91 seconds, differ from neutral by 35 pixels with a maximum of one channel level. The native owner-activation difference is not a visible shape jump. At 3.91 seconds the image is exact neutral, not a near-zero approximation.
- `audit_actual_supplement.py` rehashes every protected file in both the clean delivery and launched source: 617 per tree. It also independently rehashes all 605 original baseline files. All match their frozen hashes. The 31 capture-binding pins and pre-capture review evidence remain exact.

The clean payload retains 182 PNGs. Its only inherited file change is the already-reviewed registry append. No runtime, shader, art, UV, opacity, control bound or prior profile was changed. The pre-capture review's 2,661-record exact state/material parity for all sixteen prior profiles remains valid; it is not represented as a new render of every prior profile.

## Visual coverage and acting findings

All 541 native mouth crops were hashed into **219 distinct actual mouth images**, indexed in `actual_review/MOUTH_VISUAL_INDEX.json`. Every distinct image, indices 000–218 across all ten `UNIQUE_MOUTHS` sheets, was visually inspected at 2× nearest-neighbor diagnostic size. The deduplication is by actual pixels, not by control values, and the index maps every checkpoint to a reviewed crop. No synthetic/interpolated pose image was generated.

I also inspected all 29 builder analysis sheets: 401 native face crops covering the entire first natural cycle and every nonduplicate lifecycle/integration chapter, plus fourteen full-context views. Every crop and full-context cell was independently compared to its raw actual PNG using the documented crop/resize recipe. The remaining 140 second-cycle images are exactly equal to the reviewed first-cycle timestamps. The raw full and native peak frames were inspected separately at their supplied sizes.

### Natural performance

The mouth progressively gathers and turns down as the brows lower/slant and the lids become slightly heavier. The combined peak reads as an annoyed/frustrated pout, rather than a neutral face merely demonstrating a lip control. The held images remain settled and exact. The sustained pose softens the peak slightly while retaining its family, then the release broadens without smiling or opening. Recovery returns to the original neutral face without residual gathering.

The 4.13-second profile uses the six accepted vectors and duplicate holds only. The 0.42-second peak hold, 0.31-second sustained hold and 0.22-second final neutral hold are distinct in the authored timestamps and captured states. Smoothstep progression at the sampled intervals, including dense joins, introduces no observed contour discontinuity. This is a newly authored interpretation of still reference panels, not reconstructed source animation. Pacing was assessed from the timed trajectory and ordered actual frames, not watched as a normal-speed movie.

### Lifecycle and integration

- Release and repeated release ease the actual pout back to exact neutral. Retrigger preserves the visible starting state, relaxes toward the early phase during the existing 0.30-second bridge, then rebuilds the accepted peak. It is a restart, not a command to maintain the peak indefinitely. Interrupted release similarly restarts without a visible discontinuous pose replacement.
- The incoming EXP-005 open-laughter path closes its inherited mouth while small purse values become active; the actual mixed opening/purse samples remain joined, with teeth disappearing as opening closes. Outgoing laughter first relinquishes purse, then opens according to EXP-005's own timing. Neither incoming/outgoing nor the 75/225 ms reversals show a new mouth seam.
- EXP-116's incoming sealed width/corner shape relinquishes its width as the pout gathers. Outgoing and active-width reversal images remain sealed and joined. Testing this inherited profile does not approve its acting or change its approval status.
- Manual takeover visibly holds the requested manual purse while cancelling the performance. Reset immediately restores neutral and stays neutral. Auto-blink begins from a captured closed-eye state, hands over through the existing trigger bridge, remains suspended during the performance and resumes afterward. Its inherited high-closure eye rendering is unchanged; this review did not redesign or newly approve that old eye shape.

## Retained source interpretation limits

The exact EXP-050 source sheet and all nine panels were audited in the pinned static review against commit `7693d1b8718c3bb1c717bd586fb472a7efc42403`. Native performance anchors equal those accepted static images, so no new fit or shape refinement was smuggled into this phase.

The canonical mouth remains a smoother, rounder continuous arch than the source's short flatter center and pinched/downturned ends. The localized inner-brow knit is weaker, and the peak has less sharply concentrated frustration than the painting. Those contour/intensity residuals remain explicit. The inherited fuller lower lip and absence of a painted crease are not by themselves acting failures. In combination with the lowered/slanted brows and open heavier lids, the compact sealed downturn still communicates the requested frustrated-pout family at face and bust scales.

The earlier component-only whole-face HOLD remains preserved as history but was corrected as provisional and superseded by actual combined static evidence. This performance PASS neither restores that premature conclusion nor erases the measured residuals.

## Scope of acceptance and next gate

The exact local performance may proceed to the parent's separately controlled final-media/backup phase. Any final encoded preview or archive still needs its own verification and exact linkage to this source. No new shapes, controls, wider bounds or refinement are recommended or authorized by this review.

No normal-speed live or encoded playback, socket test, AI/TTS connection, final-media approval, user approval, Git write, Library write, CI, paid resource, hardware action or remote execution is claimed. Earlier approved and unapproved work remains separate.

## Evidence files

- `evidence/ACTUAL_INTEGRITY_AUDIT.json`: all 1,082 image receipts, 541 state matches, cycle/anchor/neutral checks and epsilon measurements.
- `evidence/ACTUAL_SUPPLEMENT_AUDIT.json`: final 617/617/605 source rehashes, 401 exact native crop cells, fourteen full-context cells and lifecycle pixel equalities.
- `actual_review/MOUTH_VISUAL_INDEX.json`: all 219 unique mouth crops and the complete checkpoint mapping.
- `audit_actual_capture.py`, `audit_actual_supplement.py`: reproducible offline verification.
- `REPORT_PRE_CAPTURE.md` and `PRE_CAPTURE_REVIEW_FREEZE.json`: unchanged earlier source, authored trajectory, cold runtime, lifecycle and prior-profile parity review.
