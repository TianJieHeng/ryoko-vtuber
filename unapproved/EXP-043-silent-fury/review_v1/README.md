# Silent Fury EXP-043 review v1

UNAPPROVED preview, not integrated. Approved main remains at 27 expressions.

Native capture passed 828 static and 7,784 motion assertions. The delivered MP4 is H.264, 968x800, 121 frames at 30 fps (4.033333 seconds). Independent review verified all 242 native frame hashes, decoded chronological order, exact neutral return, fixed body and all 1,124 frozen baseline files including 184 PNGs in the original workspace.

The acting reads as a restrained stern stare, weaker than the painted reference's knitted fury and close to Focused Determination v2 without the onset blink. Local brow knitting, horizontal convergence and jaw tightening are unsupported. Inherited lash/hair seams remain visible in detail; no clear new brow/eye collision was found. See REVIEW.md, REVIEW_SUMMARY.json and PLAYBACK_REVIEW.json.

## Reproduce

Use repository baseline commit 816d77fafb6e016dc70f0802743d444e618f7b0f. Copy its ryoko_object_rig into a local rig directory beside this package; import with Godot as needed. Capture scripts load EXP-043 only into memory and leave the production registry unchanged. Godot 4.6.3 OpenGL compatibility and FFmpeg were used.

Run `python3 run_gate.py --rig rig` and `sh run_motion.sh --state` for numerical tests. On a supported desktop run `python3 run_gate.py --rig rig --capture` then `sh run_motion.sh --capture`. Finally run `python3 encode_preview.py`. Preserve the included MP4 elsewhere first because encoding refuses overwrite. Captures also refuse overwrite.

The compact BASELINE_FREEZE.json is rendering metadata only. Full original-workspace inventories, image sequences and private machine paths are omitted. Original preservation checks require the retained full local manifest and are not portable here. Scoped review receipts describe checks already performed; REVIEW.md references additional original-workspace evidence. Source sheet and catalogue remain at their repository-relative paths recorded in SOURCE_REFERENCE.json. The original preparation README is historical, not the final render status. No CI or production changes.
