# EXP-061 Broad Surprise: independent native evidence review

**Outcome: suitable to show as a qualified, UNAPPROVED preview. The rendered candidate is coherent and visibly different from the inspected comparator peaks, but source fidelity is partial.**

Reviewed 2026-11-10 UTC. This follow-up supersedes the *missing native capture/video* status in `INDEPENDENT_SOURCE_REVIEW.md`; that document's anatomical and timing limitations remain applicable. It does not grant approval or authorize integration/publication.

## Pixels actually inspected

I inspected `review_evidence/static_faces.png` (all eight anchors), `review_evidence/encoded_keyframes.png` (decoded frames 0, 15, 27, 41, 55, 70, 86, 111 and 120), and the original `capture/broad_surprise_bust.png` at 568 × 800 and `capture/broad_surprise_detail.png` at 400 × 360. I compared the latter directly with the previously inspected EXP061 source-sheet pixels and actual existing EXP064 `shocked_gasp_detail.png` and EXP004 `delighted_discovery_detail.png` captures.

These are image inspections, not a claim that I watched the video continuously at normal speed. No UI or renderer was started by this review.

## Native appearance and source fit

- The contact sheet shows a clear closed-mouth neutral, a small initial separation, a larger opening, a sustained broad aperture, then closure back to the same neutral. The decoded keyframes preserve that progression. No gross head/body displacement or unexpected new expression appears in those sampled images.
- At peak, both brows visibly sit higher than neutral. The opening is wider and less pinched than the inspected EXP064 gasp. The native bust view retains a readable open-mouth reaction, although the facial differences are necessarily smaller at that scale.
- The eyes remain relatively narrow and close to their underlying painted shape. They do **not** reproduce the reference sheet's conspicuously rounded, widely exposed eyes. The existing four-source-pixel upper-opening control provides a restrained change, not full reference eye expansion.
- The mouth reads as a broad dark split-lip opening with a thin upper-teeth strip. It is not the source painting's rounded oral anatomy, and there is no dropped jaw/chin or altered face silhouette. The dark opening and small corner-edge details are plainly visible in the detail view. This should be presented as the current layered-rig interpretation, not anatomical equivalence.
- The still/decoded sequence supports a sustained surprised/open-mouth read rather than a delighted smile. Some interpretation remains subjective because the eyes are restrained and the mouth is assembled from the existing parts.

## Comparison with EXP064 and EXP004

**EXP064 Shocked Gasp:** the actual peak images are not visually identical. EXP061 has more whole-brow elevation, including the outer brow portions, whereas EXP064's inner ends rise around more stationary outer anchors. EXP061's mouth is wider/less pinched. The eyes remain substantially shared. The detailed peak comparison has 3,992 differing pixels, localized to the brow/mouth region, which confirms pixel nonidentity but is not a semantic distinctness threshold. The central lip-gap increase is still only about one bust pixel; the more convincing differences are brow configuration, mouth width and the authored slower/sustained timeline. This is a subtle distinction, not a separate facial construction. Continuous normal-speed comparative viewing remains unclaimed.

**EXP004 Delighted Discovery:** its inspected held expression has a conspicuous spread, upturned toothy smile; EXP061 retains a more compact open cavity without that smile conversion. This is the clearer static distinction. Their earlier round-opening/raised-brow vocabulary still overlaps.

Comparator captures are historical native evidence, not newly rendered same-baseline parity tests. Their approved36 membership is established by the integration record, but these comparisons should not be described as a fresh production-wide parity run.

## Independent mechanical verification

I reran the read-only `review_validation.py` against the completed evidence. It returned **PASS / exit 0**, with no failures or pending stages. The rerun log is `review_evidence/independent_native_validation.log`.

Verified:

- All 999 pinned source files, including 184 PNGs, remain unchanged in both source and isolated rig; the reference sheet/catalogue and approved manifests match. Disk registries remain approved36 with EXP061 absent. Reviewed candidate and capture inputs match the independent input freeze.
- Native static receipt: PASS, 870 checks. Native motion receipt: PASS, 9,508 checks, X11/llvmpipe capture, 121 states at 30 fps. All native poses equal headless states; independent interpolation error remains 2.8423027931268052e-08.
- All 16 stills and all 242 motion PNGs have the required native dimensions. Every recorded motion RGBA hash matches. Ordered filenames/timestamps and selected exact static-to-motion anchors pass.
- Neutral bookends/holds match exactly; sustained peak frames match. All full-frame pixel changes stay within `[215, 282, 345, 402]`, inside the face guard. Body/background pixels outside the guard remain fixed.
- `Broad_surprise_review_v1.mp4` fully decodes without errors: H.264, 968 × 800, 121 frames, 30 fps, 4.033333 seconds including the final sample. All 121 presentation timestamps and same-index source-panel comparisons pass. Mean RGB absolute errors are about 1.293 for the full panel and 2.039 for detail; maximum expected-minus-nearest face error is 0.003727. Identical or near-identical held poses cannot be uniquely ordered from lossy pixels alone.
- MP4 SHA-256: `66fafc481ccc35fd19e6a5024cc94c7f95aa69a20a3a4f287868053f51584cf3`.

The editor-only `project.godot` reordering/whitespace incident is recorded separately in `review_evidence/launcher_config_restore.json`; the restored file matches its original frozen hash. The successful rerun reports no reviewed-input changes. This review made no configuration restoration or other input changes itself.

## Remaining qualifications

The previous capture blocker is resolved. No normal-speed continuous observation, live-engine pacing measurement, lip-sync compatibility, export validation, body gesture performance, fresh approved36-wide parity or approval is established here. Automated evidence PASS and representative image inspection are not user approval.

**Recommendation:** deliver the preview with a short description of the slower whole-brow surprise and the existing-rig limitations. Do not describe it as a faithful jaw-drop/full-eye reproduction or as approved. Candidate remains **UNAPPROVED**.
