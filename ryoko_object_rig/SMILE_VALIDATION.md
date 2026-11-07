# EXP-005 shared-rig laughter review

Status: complete authored **local review candidate**, not user-approved or published. One application, one separate-part character assembly, one registry and one generic player. No expression-specific controller was added.

## Scope and performance

EXP-163 remains registered with its original 13-key, 5.8-second data unchanged. EXP-005 adds 15 smoothstep keys over 5.4 seconds and aliases `laugh` / `hearty-laughter`. All 93 historical catalogue IDs are preserved as reference metadata; the other 91 are not counted as implemented performances.

The exact historical beat times are retained: 0,.30,.44,.66,1.02,1.30,1.62,1.91,2.19,2.53,2.92,3.48,4.28,4.50,5.40. Mouth peaks are deliberately unequal (.94, 1.00, .88) with intervening compressions (.62, .66). Brows rebound with the laugh. The old source used a pre-open painted mouth with negative scale parameters; those values are not copied into the new normalized aperture control.

Real smiling-crescent lash/lower-contour owners, smiling lip/corner articulation and all three laugh pulses are implemented. It is not ordinary blinking plus mouth pulses. Head, jaw, nose, cheeks, neck, torso and chin stay fixed. The historical subpixel head bob is omitted rather than approximated by moving only the face. No hand gesture, gaze performance, external AI model, TTS, tracking or full-body motion was added.

All lifecycle behavior remains in the generic player: 0.30-second retrigger, 0.45-second release, atomic validation, manual takeover and reset. The new finite [0,1] channels are `eye_smile_R`, `eye_smile_L` and `mouth_smile`.

## Separate owners and geometry

### Smiling eyes

The first half of a smile-eye control closes the existing ordinary lid assembly. After it is closed, separate rigid joints articulate the ordinary closed-lash and the extracted historical crescent pigments onto a common closed contour. Incoming pigment is spatially revealed while outgoing pigment is spatially occluded. Final crescent lash, lower contour and explicitly inferred hidden continuation are independent owners, behind the retained foreground hair. RGB sampling uses fixed source UV; joints translate/rotate with unit local scale and full node opacity.

The ordinary-lid path incorporates correction F (`canonical_eye_alpha.gdshader` SHA-256 `fae2f82caa7b672ae43773507efa1c625dfff4159357784207c7bfe91875a026`). It fixes the separately reported ordinary opening/closed-lash overlap and outer fragment. Its partial-lid rendering intentionally changes; source artwork, full-open/full-closed endpoints and role meanings are preserved. Do not compare partial ordinary-lid frames to V7 and call those intentional corrections a laughter regression.

### Smiling lips and corners

The existing `upper_lip.png` and `lower_lip.png` are byte-identical full-lip source images, SHA-256 `f6e47353877a727ee41905d0b8ff11a7700d42a86d6c5416e06b2a567e774a00`. Both contain the approved native upper AND lower lip pigment. The existing static seam formula assigns the upper/lower contributions; the names do not mean lower-lip anatomy was invented from upper-only art.

Fourteen native horizontal bands form separately rigged upper/lower owners. The outer bands are independent corner owners. They move rigidly along an inferred smile contour. A wide open smile needs more contour material than the closed native lip provides. Twenty-six explicitly inferred hidden joint owners fill the variable-depth gaps between neighboring rigid pieces. Their atlas records retain each owner's native 12×45 region, source columns, exact RGBA hash, quantized alpha count and a separate all-inferred mask region. At peak, independent rendered measurement attributes 167.6920 source-pixel alpha area out of 1431.9149 (11.711033%) to inferred joint fill. This is a meaningful reconstruction, not negligible alpha cleanup or recovered original lip artwork.

The joint material is packed into one ordinary texture atlas and one inference-mask atlas. Logical owners remain separate nodes. Every atlas region is byte-identical to its prepacked RGBA. In the initial 55-frame packing comparison, 38 frames were pixel-identical; 17 had only 1–2 pixels of 1 RGB rounding difference. The final 402-state independent comparison against unpacked reference geometry is exact in 329 states; the rest differ by at most 1 RGB. All 402 forward/reverse pairs are exact. No visible shape change or neighboring-cell bleed was found in that comparison. The final atlas source is the tested/shipped representation.

Native lip RGB is not dynamically recolored or warped. No full painted mouth, skin/chin patch, animated texture scale, UV displacement or emotion-opacity crossfade is used. The cavity, white teeth and tongue remain existing independent owners.

### Bounded aperture

`mouth_open` remains normalized [0,1] and maps to physical aperture [0,.55]. The maximum opening in any source-pixel column is 30.8; the central lower-lip travel remains 29.7. Upper teeth stay at (533, 626), with both approved white tooth PNGs and registration unchanged.

Raised smile corners change the outline: the measured peak whole-aperture bounding box is about 33.625 pixels tall, while the largest per-column opening is 30.75 pixels in the 8× actual-render measurement. Do not report the entire mouth bounding box as ≤30.8, or claim the smile has the yawn's exact outline. No whole face or mouth texture is enlarged.

### Ownership correction and inference

The full source PNGs remain immutable, including the original stationary backing and front fringe. Their active derivatives change ownership at narrow, documented crossings:

- 42 brown neutral-eye pigment cores in the backing are separate eye-owned objects. Explicit harmonic hidden-skin continuation covers 96 pixels beneath their exact source/matte masks. Desired surrounding crease and foreground hair remain.
- 10 opaque mixed hair/eye pixels in the front fringe are split into retained foreground hair coverage, neutral eye pigment behind it and a distinct inferred hidden green continuation. The other 5 semitransparent review candidates are retained unchanged. No hole is punched through the hair. The existing gaze-phase distal hair-tip owner is unchanged.
- Filtered alpha-deficit reconstruction preserves the moving neutral fringe composite, rather than assuming source-pixel algebra also preserves bilinear rotated rendering. Independent native neutral/end captures are exact. Across all 267 yawn/interruption frames against the same corrected ordinary-eye shader, 54 frames are exact; other frames differ in at most 10 pixels, all inside the corrected fringe footprint. Maximum difference is 2 RGB, occurring in one pixel in only four frames. Mouth, body and yawn timing are unchanged.

Exact source-core masks, inferred support and decisions are recorded in `rig_assets/smile_support/manifest.json` and `source_references/smile_preparation`. All 126 PNG files from the final gaze source are hash-checked unchanged. These source hashes do NOT mean the rendered derived artwork is unchanged.

## Validation and honest limits

`tools/verify_smile_support.py` checks source identity, protected original oral functions, tooth anchor/cap, 26 atlas regions/masks/counts, 93 reference IDs versus 2 authored registry entries, all 15 historical timing keys and two byte-identical rebuilds. Dedicated Godot tests cover typed atomic controls, dense trajectory bounds, repeats, release/retrigger, manual/reset, yawn↔laugh handover and unit-scale/full-opacity separate owners.

The actual-Godot movie includes two complete laughs followed by release, retrigger, manual takeover and yawn↔laugh transitions. Before/after transaction captures verify that continuous trigger/release commands do not jump the displayed frame. All 720 movie frames decode cleanly. All 163 repeated-cycle frame pairs and nine command transaction image pairs are exact, as are initial/final neutral frames below the caption. Authored-cycle motion stays within face owners. Full decoded-video review and final test counts are recorded in `validation/laughter_final_review.json`.

A few native pixel edges retain fine raster/alpha-seam aliasing during very small rigid lip motions. The experiment intended to polish that behavior regressed the strict smile 0→epsilon boundary, so it was rejected; the verified continuous near-zero ownership is retained. This finite raster limit is distinct from the corrected detached rims, missing lash boundaries or state-transition jumps. Final review must judge the actual framing, not promise mathematically perfect per-pixel motion.

No normal-speed audiovisual playback has been performed in this environment. Review uses actual Godot rendered frames, decoded MP4 frames, complete decode checks, paired-frame comparison and contact sheets. The movie is silent by design. User visual review is still required before publication.

## Reproduce the complete movie

With a local graphical Godot display available, run the existing shared rig through the review-only capture driver. Choose a writable output folder outside this source tree:

    godot --path . --script res://tools/review_laughter_movie.gd -- --output=/tmp/ryoko-laughter-review
    ffmpeg -framerate 30 -i /tmp/ryoko-laughter-review/frames/frame_%04d.png -c:v libx264 -crf 17 -pix_fmt yuv420p -movflags +faststart /tmp/ryoko_EXP-005_shared_hearty_laughter.mp4

The driver captures deterministic 30 Hz state advances with the actual renderer, not realtime timing or an alternate controller. It also saves before/after command images and a per-frame state report. Rendering must not use headless mode because actual images are required. All generated evidence stays outside the source package.

Final independent review passed on the frozen combined runtime, artwork and data. It repeated the dense mouth/eye grids, epsilon boundaries, geometry/atlas analysis, full yawn comparison, live bridge, UI interactions and complete movie audit. A separate clean source copy rebuilt and imported without changing any tracked source/configuration bytes. User visual approval is still required.
