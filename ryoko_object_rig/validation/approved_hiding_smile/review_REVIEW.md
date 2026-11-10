# EXP-153 Hiding a smile: independent candidate review

## Disposition

**Ready to show as a bounded, unapproved review candidate.** No blocker was found to presenting this preview with its limits. This is not expression approval, production registration, whole-runtime sign-off, or source-perfect certification.

The candidate conveys a small, contained smile with visible amber eyes and a sealed mouth. Its source fidelity is partial: ordinary upper-lid narrowing substitutes for the source's lower-lid crinkle, and the peak can read as a relaxed or knowing half-lidded smile rather than an unmistakable effort to suppress one. The source's exact brow curvature and tightly compressed painted lip contour are not reproduced. Whether that interpretation is sufficient remains a visual judgement for the user.

No candidate, timing, runtime, artwork or production-registry changes were made during this review. No GUI or normal-speed playback was used.

## Material and provenance

- Source sheet: `../insight_integration_work/avatar_build_assets/reference_library/assets/expressions/EXP-153_hiding-a-smile/RYO_EXP-153_hiding-a-smile_sheet_v001.png`.
- Source SHA-256: `e3d1d6c86522e8eaa82874a224b0d0d88a13b075ed37e4403de8ddd08875eb5c`.
- Candidate: `EXP-153.json`, SHA-256 `8a6b61f41a7d6e619f7bcbee188008d5c454cb2295e2c22460829c40f1b87b76`.
- Movie: `Hiding_a_smile_review_v1.mp4`, SHA-256 `9642f1afbef44680cc81b2a32a8c49d00a7b6c87f6ba266f39a4f44bf0addfbd`.
- Evidence: native static captures; `motion/full/0000.png` through `0120.png` and matching detail captures; static and motion result files; candidate plan; capture and encoding scripts; shared sampler and face-control implementation; `BASELINE_FREEZE.json`.
- Independent measurements and reproduction script: `review/checks.json` and `review/check_review.py`. Visual comparison sheets are `review/motion_samples.png` and `review/all_mouth_frames.png`.

The copied baseline contains **26 production profiles** and the existing shared-runtime handoff ordering fix. Its inherited `RELEASE.json` still lists 25 profiles. This is a 26-profile integration snapshot with preserved older release metadata, not evidence of a finalized26 release. EXP-153 is absent from the on-disk registry and from candidate JSON files inside the rig; review harnesses add it only in memory.

## Visual observations

The original nine-panel sheet was inspected directly. Its middle panels show slightly narrowed but visibly open amber eyes, relaxed brows and an upward-curving, closed mouth. The four-second candidate timeline is newly authored from those static panels, not a recovered animation or an implementation of the catalogue's proposed 1.9-second timing.

Inspected native static neutral, onset, build, peak and soften detail images, the peak bust, motion detail frames 0, 7, 16, 28, 42, 61, 81, 103, 113 and 120, all 121 native mouth crops, and the decoded MP4 peak frame. The sampled face progression covers onset, build, held peak, recovery and neutral return.

- Mouth corners lift symmetrically into a small smile. Across the inspected all-frame mouth contact sheet, the lip boundary remains closed: no exposed teeth, dark oral cavity, new detached lip piece or conspicuous new mouth seam was observed. Existing white lip highlights remain on the lip surface, not exposed teeth.
- Lip pressure is visibly subtle. It reveals existing inner-lip tissue under the shared control; it is not a new compression simulation and does not exactly reproduce the source's painted pressed-lip shape.
- Ordinary lids narrow while the amber irises remain visible. This does not reproduce the source's lower-lid crinkle. The existing closed crescent smile-eye component was not substituted, and no new eyelid anatomy or artwork is present.
- The small rigid brow offsets/lifts soften the brow presentation but cannot reproduce painted curvature. Together with upper-lid lowering, the result is more half-lidded than the source's amused eye crinkle.
- Small jagged edge fragments at the outer eyelid/hair intersections are visible in neutral and active detail views. They are not a new mouth seam or evidence of new artwork, but remain a local polish limitation. This review does not certify the whole face as seam-free.
- Hair silhouette, earrings, neck, clothing and body show no acting or displacement. No residual expression is visible at the final neutral frame.

Selected-frame inspection and temporal measurements do not constitute continuous normal-speed observation. `normal_speed_observed` remains false.

## Independent all-frame checks

Every native PNG was opened and compared. This provides all-frame pixel/state coverage, plus the stated visual inspections, not a claim to have watched real-time playback.

- Exactly 121 chronological frames in each view: full 568 × 800; detail 400 × 360.
- All 242 decoded RGBA SHA-256 hashes match the corresponding native capture records.
- First and final frames are pixel-identical in both views. Frames 0–6 and 113–120 are exactly neutral. Frames 42–61 are an identical held peak. Each view contains 88 distinct images.
- Static neutral, peak and neutral-return captures are pixel-identical to motion frames 0, 42 and 120 respectively, in both views.
- The union of full-view differences from neutral is confined to the half-open rectangle **[209, 287, 356, 388)**. Every pixel outside this facial rectangle is unchanged throughout all 121 frames; specifically, all pixels at y ≥ 420 are unchanged.
- The detail difference union is **[34, 62, 333, 268)**. Peak difference counts are 1,982 full-view pixels and 7,786 detail pixels. These are coverage measurements, not quality scores.
- Independent evaluation of all 30 controls at all 121 timestamps matches the shared cubic smoothstep sampler, including its existing 0.30-second entry blend, to a maximum absolute error of **1.404 × 10⁻⁸**.
- Only the intended eight controls become nonzero: left/right ordinary lid narrowing, left/right brow offsets, left/right inner-brow lifts, bilateral mouth-corner lift and lip pressure. Mouth opening, scoped opening, ordinary smile/spread and all other excluded channels remain zero.
- The inspected native motion report records **3,536 checks passed**, no failures. The headless motion report records **3,293 passed**; static native capture records **372 passed**. These are reviewed execution reports, not an independent Godot rerun.
- Harness coverage includes scope, sealed-mouth compatibility, excluded channels, fixed head/body transforms, auto-blink off, exact final object neutral, five sampled same-expression restart/release/reset points, and unchanged on-disk registry. Its sealed-mouth predicate is a control compatibility check; the no-visible-opening finding also relies on the rendered mouth inspection above.

Restart/release/reset assertions are state checks after capture, not rendered interruption movies. They do not establish arbitrary cross-expression handoff behavior.

## MP4 decode and order

Independently ran a strict full decode with `ffmpeg -nostdin -v error -xerror -i Hiding_a_smile_review_v1.mp4 -map 0:v:0 -f null -`. It exited successfully with no decoder errors. An independent frame-count probe and RGB stream decode both yielded 121 frames.

- H.264, yuv420p, **968 × 800**, **30 fps**, **188,875 bytes**.
- Duration **4.033333 seconds**, expected for 121 endpoint-inclusive samples at 30 fps. The authored performance ends at 4.0 seconds.
- All 121 presentation timestamps equal their frame index divided by 30, within the probe's printed precision.
- Both displayed regions were compared against every same-index native PNG: full view at x 0–567; detail at x 568–967, y 220–579.
- Average absolute RGB error is **1.292/255** for full view and **2.038/255** for detail. The worst frame averages are **1.294/255** and **2.063/255**. These are consistent with the lossy H.264/yuv420p encode.
- The encoded facial-activity curve correlates with the native curve at **0.999376**. Same-index image comparisons, ordered timestamps, inspected samples and the numeric input sequence in the encoding script agree with the intended chronological capture. Lossy compression and repeated holds do not uniquely distinguish every nearly identical adjacent frame.
- The decoded peak preserves the intended full/detail layout and the visible “Review candidate” label.

Exact neutral/body identity applies to the native PNGs, not to compressed movie pixels.

## Preservation and remaining limits

All **1,059 frozen files**, including **184 PNGs**, still match the baseline SHA-256 manifest. No frozen file is missing or changed; no extra non-cache rig files were found. The registry's 26 IDs match the freeze exactly. The review adds only its report, measurements, comparison images and checking script outside the rig.

Native evidence uses Godot 4.6.3 on X11/Mesa llvmpipe. The existing warning about `uneasy_clear_parting.png` being loaded as an image file remains relevant to exported builds. No export packaging, another renderer, full production regression, interactive pacing or normal-speed viewing was tested here.

Before stronger claims: obtain the user's judgement of the partial source fit and timing; perform normal-speed observation if that claim is needed; and run the appropriate final-baseline/integration/export checks if the candidate is later registered or packaged. No new art, anatomy, animation capability or whole-runtime approval is implied.
