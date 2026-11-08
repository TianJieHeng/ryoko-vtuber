# Independent final review

The focused EXP-163 correction passes visual and functional review. Teeth read white, retain subtle divisions and stay attached beneath the fixed upper lip. The maximum opening is close to the reference and slightly shallower. Original fuller lips and likeness are preserved. This result is ready for the user's review of one expression; user approval remains pending.

The actual reference screenshot and final Godot source/native/oral views were inspected. Independent facial alignment estimated scale 0.79133, matching the implementation estimate of approximately 0.79184. Effective aperture 0.55 gives a conservative near-reference limit. Candidate dark-mouth area is 825 pixels versus reference 832, with bottom y451 versus y453. The central opening band is 48 versus 47 pixels, within approximately one pixel of resampling/compression uncertainty. Fixed fuller lip endpoints are deliberately unchanged.

Only the two tooth RGB derivatives differ among the original 270 artwork PNGs. Their alpha channels and dimensions are exact; all 268 other original PNGs are byte-identical to the preceding release. Upper teeth remain at (533,626). Independent oral sprites retain unit scale and full opacity. No feature deformation, UV warp, face patch or opacity crossfade was introduced.

333,283 independent actual-engine checks pass with zero failures. They cover 1,001 manual values, invalid inputs, discrete aliases, finite numeric direct calls, 3,600 fine timeline steps, seven release points and seven retrigger points. Shader opening never exceeds 0.55. Supported normalized controls remain 0–1. Non-neutral legacy visemes are rejected atomically; REST, RELEASE and NEUTRAL remain available.

126 targeted actual-engine frames cover 21 forward/reverse values at source 1×, native 0.49× and oral 2×. All 63 reverse pairs are exact. At all scales, the two smallest positive values are identical to zero and 0.0001 differs by at most one channel value. No neutral tooth leak or opening pop is visible.

All 468 decoded final-movie mouth frames were viewed chronologically. Full decode has no errors. All 156 raw stage frames match the preceding release exactly outside conservative mouth bounds. All 59 repeat-cycle pairs are exact outside the changing footer; initial and final neutral are exact.

341 actual release/retrigger frames were checked. All four command-boundary image pairs are exact, released/final neutral is exact, and every frame matches the preceding release outside the mouth bounds. Enlarged chronological release and retrigger views show no detached row, residue or abrupt handover.

Native normal-speed playback was not performed. This review does not claim unrestricted controls, pristine hidden artwork or approval of other expressions. The previous eye/hair/crossing limitations remain. See final_movie_review.json, reference_peak_metrics.json and ../VALIDATION.md for numerical results, source rebuild and packaging checks.
