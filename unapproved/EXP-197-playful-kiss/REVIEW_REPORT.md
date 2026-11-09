# EXP-197 Playful kiss review candidate

## Result and approval boundary
The approved 44×42 kiss-mouth artwork is assembled into one 7.2-second shared-rig performance. The full animation is unapproved and belongs only in the unapproved backup. Twenty production profiles and the protected source are unchanged.

The performance moves from neutral through a modest blushing anticipation, compact native lips, the forward kiss, bilateral soft closure, unequal amber-eye reopening, a small sealed smile and exact neutral. The head and body remain fixed. Timing is a new review interpretation of source KP1–9, not the source’s nominal 1.9-second timing. KP2 and KP8 are restrained transitions, not new acting gestures.

## Shared-rig changes
- `mouth_kiss` is a bounded [0,1], zero-default shared control and timeline channel. The approved mouth PNG is a fixed sprite at canonical [543,618], with unit scale and no deformation.
- Native mouth owners retain their original visibility, including `spread_lower_oral_surface`. The kiss owns only a reversible native opacity factor. Zero restores the original self-opacity and shader weight, avoiding the prior preview’s blanket-hide leak.
- Five existing mouth shaders now have `native_part_weight`, default 1. Their geometry, textures and UV equations are unchanged. This explicit alpha multiplier is required because their fragment code overwrites COLOR and does not honor sprite self-opacity. The initial visual check caught that limitation; the corrected blend was checked at 0, .25, .5, .75 and 1.
- Positive kiss weight requires `mouth_open=0`. Manual validation includes retained fields. Timeline validation rejects segments mixing open mouth and kiss. The existing staged sealed-mouth handover includes kiss so transitions to/from older opening profiles remain bounded.
- The normal viewer includes a kiss-blend slider. The bridge reports its range and static-art limitation. No production registry was changed; only this candidate registry adds EXP-197.
- The eye sprite and shader samplers load the exact approved repaired iris PNGs directly. This prevents stale copied import-cache textures from overriding the approved artwork. Both rendered iris images were verified pixel-exact to the source files.

## Focused checks
The focused state check covers the complete 30 fps cycle, control validation, rejection atomicity, repeated trigger, release at kiss formation/hold/recovery, exact neutral snapshot and self-opacity restoration, and bidirectional mouth-domain handovers with all twenty existing profiles. Source texture identities, unit scale, regions and head/body transforms are checked through the cycle. This is focused qualification, not a claim that every legacy test suite was rerun.

The corrected native static check establishes exact equality with the previously approved full-kiss KP4 image, exact neutral pixels before/after, and exact equality to the approved neutral preview. Both irises bind to the repaired source PNG pixels. The part stays fully present through KP6; both amber irises remain visible, with screen-right a narrow slit. KP7 recovers to a small sealed smile, without an open laugh.

## Limits
The mouth is one static approved artwork part, not independently articulating upper/lower anatomy. Speech/TTS mixing with positive kiss weight is deliberately unsupported. Cross-expression transition checks are state-level; the delivered clips show the full standalone EXP-197 cycle. The neutral and full-kiss images are exact proofs at their respective checkpoints, not a claim that source reference artwork was copied into an animation.

The first 2× viewport streaming render ended before completion; its incomplete files are not deliverables. Separate native-size views reduce capture load. All runs are local. No CI, hardware, paid resources or remote execution was used. Development diagnostics are retained outside the candidate source.

## Final delivered previews
Both MP4s contain 217 frames at 30 fps, 7.233333 seconds including the final neutral frame. Full view is native 568×800; face detail is native 400×360. Actual public-player captures and FFmpeg encodes both exited successfully. Their capture logs verify exact neutral pixel and face-state restoration, fixed head/body and source texture/scale/region identities throughout the cycle. Recorded capture durations were 30.80 seconds and 21.15 seconds; these are offline captures, not real-time performance benchmarks. No engine remains.

Independent sampled visual review finds coherent anticipation/kiss/recovery without obvious double lips or patches. The small screen-right KP6 amber slit is present but reads almost closed at body size. KP7’s smile is deliberately restrained and much subtler than the source sheet; do not describe it as strongly readable. Sampled visual review does not establish every-frame temporal smoothness.
