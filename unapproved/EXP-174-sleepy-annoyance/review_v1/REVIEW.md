# EXP-174 Sleepy Annoyance: independent review

**Disposition: ready to share as an UNAPPROVED review MP4. Not approved or integrated.**

The expression is visibly readable at the delivered 568×800 full-bust size, not only in an enlarged face crop. Heavy, still-open amber eyes establish sleepiness; the lowered and inward-tilted brows add annoyance; the compact, downturned sealed mouth is plainly different from neutral. No new mouth opening, broken lip contour, or face/body seam was observed in the inspected material. Existing small lash/hair-edge fragments remain visible, especially in the detail view.

## Source fit and limitations

I inspected the actual nine-panel EXP-174 source sheet and verified its SHA-256, `cd149911dfd8c7309f25ed828772e739f6a79f859e824b69c98a0c87281cfcca`. Its middle row combines heavy lids, sharply drawn lower inner brows and a small downturned mouth. This candidate follows that emotional progression coherently. The unchanged model retains its identity and stable body.

This is a **partial interpretation**, not a reproduction of every source feature:

- The existing rigid brow lowering and tilt give a visibly annoyed angle but cannot reproduce localized brow knitting or inward horizontal convergence.
- The existing whole-mouth purse produces a narrow, closed pout. It does not independently project or push out the lower lip. The lower-lip shading remains part of the inherited artwork.
- Both irises remain visible at peak. There is no new full blink, smile-eye squint, gaze movement, head/body acting, or added lip anatomy.
- Existing hard/fragmented lash edges near foreground hair are evident in neutral and remain evident during closure. This review does not claim those inherited artifacts were repaired.
- The four-second performance is newly authored from static reference panels. It is not recovered source animation.

## Actual visual review

Inspected all six native static face-detail anchors, native neutral and peak full-bust images, the decoded peak composite at its actual delivered size, and decoded chronological samples **0, 6, 10, 16, 25, 34, 50, 66, 70, 80, 89, 100, 111 and 120**.

The selected samples show lids becoming heavy before the strongest brow action, a coherent peak, an unchanged hold, and a gradual release to neutral. Brow and lash changes remain separated sufficiently to read; no eye disappears. The peak looks sleepy and irritated rather than smiling. Inspection of the chronological montage of **all 121 native mouth crops** found a connected closed contour throughout, without an exposed oral cavity, new mouth gap, disconnected corner, or transient lip seam.

The native full-bust peak changes **2,274 pixels** versus neutral. Across the entire timeline, all changed full-bust pixels fall within the face rectangle **x=209–355, y=287–389**; 2,309 pixels change at least once. These measurements support localization, not an automatic judgment of expression quality. Perceptibility and source fit above are based on viewing the actual images.

## Independent technical evidence

`INDEPENDENT_REVIEW.json` records **34 passed independent checks**. `independent_review.py` reproduces them without modifying source artwork, rig code, controls, or registries.

- Native static capture: **684 checks, PASS**. Native timeline: **7,542 checks, PASS**, 121 endpoint-inclusive samples at 30 Hz, X11 with llvmpipe.
- Independently recomputed **all 242 native raw-RGBA hashes** and matched every chronological record. Both views contain exactly 0000–0120 PNGs, with 73 unique images each.
- Every full-bust body pixel below y=430 is identical across all 121 frames. All image alpha remains opaque. Changes are confined to the face.
- Frames 0–6 and 111–120 are exactly the same neutral pixels in both native views. Frames 34–66 are exactly the same peak pixels. Static neutral, peak and neutral-return images exactly equal their timeline counterparts.
- All 121 recorded poses keep excluded channels at zero, including mouth opening and all head/body/hair/gaze controls. Lids are symmetric and bounded at approximately 0.4, allowing the documented float32 rounding.
- Rehashed **all 1,124 frozen source files, including 184 PNGs**, in both the original baseline and copied rig: unchanged. Both registries preserve the same 27 IDs; EXP-174 is absent from disk and exists only in the capture harness's loaded memory.
- MP4: H.264/yuv420p, **968×800, 30 fps, 121 frames, 4.033333 seconds, 196,718 bytes**. Full decode completes without error; all presentation timestamps match frame index / 30.
- Decoded every video frame and compared its full-bust and detail panels with the same-index native image. Mean absolute RGB channel differences are 1.288–1.295 for the bust and 2.005–2.071 for detail, consistent with the lossy conversion. These are diagnostics, not visual acceptance thresholds.
- Independently rebuilt the composite from the explicitly numbered native sequences. The resulting MP4 is **byte-identical**, verifying ordering even through visually identical holds and nearly identical neighbors.

**MP4 SHA-256:** `b9a27864a8d8fb0085d063f0978522249d0275d8b84c0df2bf613954a48151a6`.

An initial exploratory RGB-MAE bound of 2 rejected even the unchanged neutral detail, because the video uses lossy YUV420 conversion. That inappropriate gate was removed rather than treated as a rig failure; the initial result is preserved in `independent_review/exploratory_history/initial_rgb_mae_threshold.json`. Frame correspondence is established by complete decode comparisons and the stronger exact chronological re-encode match.

## Remaining review boundaries

**No GUI or continuous normal-speed playback was performed.** The evidence covers native rendered frames, selected decoded-frame viewing, all native mouth crops, exact chronology and codec validation. It does not establish normal-speed subjective timing, live interaction, lip-sync compatibility, exported-build packaging, or approval. This was not a rerun of the full production release suite.

No approval, registry integration, source-art change, CI, purchase, hardware flashing, or remote-machine execution was performed by this review. The video can be shared for the user's next unapproved candidate review with the lip-projection and inherited edge-artifact limitations intact.

## Evidence files

- `INDEPENDENT_REVIEW.json`: complete independent results and per-frame diagnostics.
- `independent_review/raw_frame_hashes.json`: all 242 recomputed pixel hashes.
- `independent_review/decoded_detail_timeline.png`: the 14 inspected decoded timeline samples.
- `independent_review/all_121_native_mouths.png`: every native mouth crop in chronological order.
- `independent_review/decoded_0034.png`: actual-size peak MP4 composite.
- `independent_review/order_reconstruction.mp4`: byte-identical chronological reconstruction, a validation duplicate rather than a second deliverable.
