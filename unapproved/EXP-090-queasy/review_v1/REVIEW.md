# EXP-090 Queasy: independent candidate review

## Decision

**Ready to show as an unapproved, limited-scope review candidate. Not approved, not production-integrated, and not evidence that the full 25-profile runtime is release-ready.**

The isolated neutral-to-Queasy-to-neutral performance is technically consistent with its existing controls. Source fidelity is partial: narrowed lids and a pursed, pressed, sealed mouth are represented; the source's strongly worried brow curvature and cheek tension are not. At the peak the result can also read as tired or pouty. The user must judge whether this approximation conveys Queasy sufficiently.

This review did not modify artwork, the rig, candidate controls, timing, or the production registry. The only written deliverable is this report. No GUI or normal-speed playback was used.

## Reviewed material and identity

- Source: `../insight_integration_work/avatar_build_assets/reference_library/assets/expressions/EXP-090_queasy/RYO_EXP-090_queasy_sheet_v001.png`.
- Source SHA-256: `785b45abad9297a18294d4a3fbf93ab52d8577e05556fc2279cbd223a7d2c4ce`.
- Candidate: `EXP-090.json`, SHA-256 `08813729222c8231500233ec6952459b6549e5fd534e87516fb1f99efa17676c`.
- Movie: `Queasy_review_v1.mp4`, SHA-256 `6597d8405fec550a0a9dec4b206e97608cc14a6686fd023a7a0ed928a8198e81`.
- Native capture: `motion/full/0000.png` through `0120.png` and matching `motion/detail/` frames.
- Supporting evidence inspected: `render_motion.gd`, `check_and_capture.gd`, `plan.json`, `motion_checks.json`, `motion_state_checks.json`, static captures, `BASELINE_FREEZE.json`, shared sampling/restart implementation, and encode implementation.

The copied baseline has 25 profiles. Its freeze describes a 25-profile integration snapshot with inherited approved24 release metadata at copy time, not a finalized approved25 release. The preparation-only label in that freeze is historical; completed capture evidence is in the separate motion checks. The parent's report of an unresolved cross-profile sealed-mouth integration issue is outside the isolated Queasy evidence and remains a release limitation.

## Source fidelity and visual inspection

The nine-panel source is a static expression sheet, not a recovered animation. The candidate's 4.0-second timeline and 0.7-second peak hold are a new interpretation. The proposed 1.9-second catalogue timing has not been reconstructed or claimed.

Viewed the full source sheet and actual rendered static neutral, build and peak detail plus peak bust. Viewed motion detail frames 8, 16, 28, 39, 68, 79, 95, 112 and 113, and motion full frame 39. These cover first onset, build, peak, recovery, nearly recovered and exact-neutral states. Static neutral, peak and returned-neutral captures were independently found pixel-identical to motion frames 0, 39 and 120 in both views.

Observed:

- Lids narrow progressively, hold, and recover. The mouth narrows into a closed pursed/pressed contour without an obvious exposed oral cavity in the inspected peak and intermediate images.
- Available inner-brow controls act on rigid existing brow parts. The peak brows become more level than neutral, but do not reproduce the prominent curved, inner-raised worry shape in the source's middle panels. This is a substantive fidelity limit, not proof that the inner-brow controls are absent.
- Cheek tension and a newly painted forward lip contour are unsupported. They must not be described as implemented deformations.
- The existing hair, clothing, jewelry and body retain their neutral rendering. Small edge fragments at hair/lash intersections are visible in the neutral crop and remain visible in active crops. No cosmetic repair was attempted, and this review is not a general artwork-polish sign-off.
- The selected frames show a coherent progression and recovery. Temporal statistics and frame inspection do not substitute for watching the performance at normal speed; normal-speed observation remains false.

## Independent all-frame checks

All 121 PNGs in each view were opened and compared programmatically. This is all-frame pixel/state coverage, with visual inspection of the selected frames listed above, not a claim to have visually watched every frame.

- Full view: 568 × 800. Detail view: 400 × 360. Both sequences have exactly frames 0–120.
- Every PNG's decoded RGBA SHA-256 matches its corresponding native capture record. No record/image mismatch.
- Native full and detail first/last images are byte-exact at decoded pixel level. Frames 0–7 and 113–120 are exactly neutral in both views.
- Frames 39–60, inclusive, are exactly identical throughout the peak hold in both views. Each sequence has 85 distinct images.
- Across the complete full sequence, the union of all differences from neutral is confined to `[209, 286, 356, 390)` in x/y half-open coordinates. No changed pixel exists outside that facial rectangle. In particular, every body pixel at y ≥ 420 is unchanged in all 121 frames.
- Detail difference union is `[34, 60, 333, 272)`. Peak changed-pixel counts are 2,260 full and 9,047 detail. These are coverage measurements, not visual-quality scores.
- Independent evaluation of all 30 control channels across all 121 recorded poses matches the authored cubic smoothstep with the existing 0.30-second displayed-pose entry blend. Maximum absolute difference is `2.9660142453e-08`. Ignoring that existing entry blend would produce a small expected mismatch at the first active frame; it is not a candidate defect.
- The provided native harness reports 3,536 passing checks with no failures; headless state harness reports 3,293 passing checks. The inspected harness checks sealed-mouth and scoped validity, excluded channels, fixed head/body transforms, auto-blink off, final exact object neutral, five same-expression restart/release/reset points, and unchanged on-disk registry.
- Same-expression restarts/releases are checked at the state level after capture. They are not rendered interruption movies and do not establish arbitrary cross-profile handoff correctness.

## MP4 verification

Independently ran a complete strict decode using `ffmpeg -nostdin -v error -xerror -i Queasy_review_v1.mp4 -map 0:v:0 -f null -`. It returned success with no decode error. A separate `ffprobe -count_frames` confirmed 121 readable frames.

- H.264, yuv420p, 968 × 800, 30/1 fps, 198,488 bytes.
- Container duration 4.033333 seconds: expected for 121 samples at 30 fps, including the timeline's exact 4.0-second endpoint.
- Stream-decoded every movie frame to RGB and compared both displayed image regions to their same-index native PNGs. The full image occupies x 0–567; the detail image occupies x 568–967, y 220–579.
- Mean absolute RGB error averaged across frames is 1.290/255 for the full view and 2.039/255 for detail; worst per-frame averages are 1.293 and 2.068. This is consistent with the lossy H.264/yuv420p encode. All frames correspond in order to the intended native frames.
- Exact neutral/body pixel identity is established on native PNGs, not asserted for lossy MP4 pixels.

## Preservation and remaining limits

All 990 files listed by the copied baseline freeze exist and still match their frozen SHA-256 values, including all 184 frozen PNGs and the production registry. This establishes preservation of that snapshot, not that the snapshot already passes every integration requirement. EXP-090 is loaded only through the review harness's in-memory catalogue.

The repository-dependent baseline verification log is a failed attempt: its Git inventory command cannot run in this non-repository copy. It must not be reported as a passing whole-baseline validation. The independent 990-file hash check above provides narrower preservation evidence. The native log also contains an inherited resource-loading warning that `uneasy_clear_parting.png` loaded via `Image.load_from_file` will not work on export. No exported build was tested here.

Outstanding before stronger claims:

1. User judgement/approval of Queasy's partial source fit and timing.
2. Normal-speed playback review if that claim is needed.
3. Resolution and verification of the separate cross-profile sealed-mouth integration issue before calling the containing runtime production-ready.
4. Appropriate final-baseline/export/integration checks if this candidate is later integrated or packaged.

No whole-production pass, arbitrary cross-expression guarantee, new cheek/brow artwork, or new animation capability is implied by this candidate review.
