# Shocked Gasp EXP-064 review v1

UNAPPROVED preview, not integrated. Approved main remains at 27 expressions.

Native capture completed: 496 static and 7,541 motion checks passed. The delivered MP4 is H.264, 968x800, 121 frames at 30 fps (4.033333 seconds). Independent review verified all 242 native frame hashes, chronological decoded frames, exact neutral return, fixed body and 1,124 baseline files including 184 PNGs. Native logs contain inherited warnings only, no rendering errors. See REVIEW_SUMMARY.json and PLAYBACK_REVIEW.json.

The open gasp and inner-brow rise are readable at bust size. Whole-eye oval expansion and jaw movement remain unsupported; eyes are less round than the painted reference. Inherited lash/hair edge seams remain. Playback inspection sampled phases of default 1x ffplay, not continuous observation or live engine pacing. No user approval is implied.

## Reproduce

Use repository baseline commit 816d77fafb6e016dc70f0802743d444e618f7b0f. Copy its ryoko_object_rig into a local rig directory beside these files, preserving source files, and run Godot import as needed. Candidate registration is memory-only; no production registry changes.

Run `python3 run_gate.py --rig rig` and `sh run_motion.sh --state` for numerical checks. On a supported desktop display run `python3 run_gate.py --rig rig --capture`, then `sh run_motion.sh --capture`. Encode using `python3 encode_preview.py`; preserve the included MP4 first because encoding refuses overwrite. Original capture used Godot 4.6.3 OpenGL compatibility and FFmpeg.

The compact BASELINE_FREEZE.json supports rendering, not original-workspace preservation checks. Those checks require the full retained local manifest and source snapshot. Broad baseline inventories, imported rig copies and image sequences are intentionally omitted. REVIEW.md references original-workspace review images; this backup includes scoped receipts and hash/order evidence, not those optional contact sheets. README.preparation.md records the earlier pre-render stage and does not supersede this completion status. No CI, paid resources, hardware flashing or remote-machine execution.
