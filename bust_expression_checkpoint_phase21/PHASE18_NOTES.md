# Phase 18: approved checkpoint

Adds EXP-097 secondhand embarrassment, EXP-107 confident reassurance and EXP-194 mock crying using exact peak references. Built-in image generation supplies raster facial artwork; extraction registers independent eye/brow, blink, rest-mouth and cheek effects on the approved fixed bust.

Embarrassment preserves viewer-right closed eye, viewer-left narrow amber eye, worried brows, prominent blush hatching and wavy closed lips. Its closed side uses identical artwork through blink reset; the remaining eye fully closes. Reassurance uses relaxed half-open eyes and a modest open warm smile. Mock crying keeps both eyes shut, peaked inner brows and downturned open mouth, without invented tear streams.

Speech overrides rest mouths independently and restores them upon release. Cheek effects persist while speaking and hide on expression switch. Headless Godot4.6.3 passed 89 baseline and 33,906 expression checks across 54 profiles; all 298 prior artwork PNGs remain byte-identical.

Comparison boards are static registered-sprite composites, not live graphical runtime captures. No audio wiring, transitions, physics or CI. User approved comparisons before publication.

## User-requested cheek correction
The initial comparison revealed split/doubled blush from eye-tile and cheek-tile boundaries, plus a detached curved base-hair tip below the viewer-left eye. Corrected generated cheek artwork now covers each cheek continuously; eye tiles end above that area. Each of these three profiles uses exactly one cheek surface per side, persistent through blinking and speech, rather than stacked blush patches. The original base and all 298 prior expression artwork PNGs remain unchanged. Superseded unpublished blush tiles are kept outside the runnable project.

Updated headless results: 89 baseline and 33,906 expression checks pass, including explicit two-cheek-layer and speech/blink visibility checks. Corrected exact-reference comparisons visually inspected; User approved corrected comparisons before publication.
