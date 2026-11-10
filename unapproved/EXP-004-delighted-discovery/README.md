# Delighted Discovery EXP-004 review v1

UNAPPROVED preview, not integrated. Approved main remains at 27 expressions.

Native capture passed 489 static and 7,178 motion assertions. The delivered H.264 MP4 is 968x800, 121 frames at 30 fps (4.033333 seconds). Independent review verifies native frame hashes, decoded chronological order, exact neutral return, fixed body and baseline preservation. See REVIEW.md and REVIEW_SUMMARY.json for the precise completed scope.

A small open discovery becomes a broad, toothy smile while eyes remain open. The rig approximates painted eye and mouth anatomy, and inherited lash/hair seams remain. The source smile is less toothy. Acting shares round-to-smile vocabulary with Sudden Insight; the distinction is sustained eye opening and broader smile, not open eyes versus closed eyes. At its held smile EXP-004 uses opening 2.5, brow lift 0.6, mouth opening 0.7, smile 1.0 and spread 0.8. Approved EXP-125 holds opening 0, brow lift 0.18, mouth opening 0.6, smile 0.8 and spread 0.6; its sealed release uses blink 0.08, not closed eyes. Four-second timing is newly authored from static reference panels.

## Reproduce

Use repository baseline commit 816d77fafb6e016dc70f0802743d444e618f7b0f. Copy its ryoko_object_rig into a local rig directory beside this package and import with Godot as needed. Capture scripts register EXP-004 in memory only; the production registry remains unchanged. Godot 4.6.3 OpenGL compatibility and FFmpeg were used.

Run `python3 run_gate.py --rig rig` and `sh run_motion.sh --state` for numerical tests. On a supported desktop run `python3 run_gate.py --rig rig --capture`, then `sh run_motion.sh --capture`. Run `python3 encode_preview.py` after preserving the supplied MP4 elsewhere, since encoding refuses overwrite. Capture also refuses overwrite.

The compact BASELINE_FREEZE.json is rendering metadata, not the full preservation manifest. Original-workspace inventories, image sequences and private machine paths are omitted. Preservation scripts require the retained original workspace and are not portable here. Scoped receipts document checks already performed; REVIEW.md may refer to additional local evidence. Source references use repository-relative paths. README.preparation.md is historical; this README records completed native capture and review. No CI or production changes.

## Approval update

The user subsequently approved this expression. See APPROVAL_STATUS.json. Historical review statements describe their original capture stage; this branch remains a standalone backup, not production integration.
