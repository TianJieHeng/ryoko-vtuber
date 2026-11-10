# Bitter Taste EXP-093 review v1

UNAPPROVED preview, not integrated. Approved main remains at 27 expressions.

Native capture completed: 6,978 static and 7,546 motion checks passed. The delivered MP4 is H.264 yuv420p, 968x800, 121 frames at 30 fps, 4.033333 seconds. All 242 native RGBA hashes, exact neutral return, fixed body and 1,124 baseline files including 184 PNGs were verified in the original workspace. Independent review passed for delivery. See REVIEW.md and REVIEW_SUMMARY.json.

The brows lower and eyes narrow into an open grimace, then a closed aftertaste and neutral return. It reads as displeased/disgusted grimacing rather than the source's distinct upper-lip curl. Independent upper-lip rise is unsupported: both contours move downward, the lower farther. Inherited lash/hair seams remain visible. No new artwork or shared runtime modification is included. PLAYBACK_REVIEW.json records sampled displayed phases of default 1x playback at bust size, not continuous observation or live engine performance certification.

## Reproduce

Use repository baseline 816d77fafb6e016dc70f0802743d444e618f7b0f. Copy ryoko_object_rig into a local rig directory beside these files and run Godot import as needed. The candidate is registered only in memory. From this directory run `python3 run_gate.py --rig rig` and `sh run_motion.sh --state` for numerical checks. On a supported desktop display run `python3 run_gate.py --rig rig --capture` and `sh run_motion.sh --capture`, then `python3 encode_preview.py`. Preserve the included MP4 first; encoding and capture refuse overwrite. Original capture used Godot 4.6.3 OpenGL compatibility and FFmpeg.

Compact BASELINE_FREEZE.json supplies rendering metadata only. Original-workspace preservation checks need the full retained local manifest and are not claimed portable here. Native image sequences and broad baseline inventories are not included. Review evidence records original-workspace validation; source images remain in the repository's reference library. The original README and validation history are retained locally. The inherited headless opening-shader diagnostic was reproduced using approved EXP-063 alone, with EXP-093 absent; candidate-specific native capture passed without that error. No CI, paid resources, hardware flashing or remote-machine execution.
