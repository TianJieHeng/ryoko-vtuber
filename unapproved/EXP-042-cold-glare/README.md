# Cold Glare EXP-042 review v1

Standalone capture backup. Native MP4 and numerical receipts are preserved. See review_evidence/partial_review.json for independent review scope and limitations.

To reproduce, copy ryoko_object_rig from baseline commit 816d77fafb6e016dc70f0802743d444e618f7b0f into rig beside these scripts. Run python3 run_gate.py --rig rig, then sh run_motion.sh --state. On a supported display add --capture to capture commands. Encoding refuses overwrite of the supplied MP4. Godot 4.6.3 and FFmpeg were used. Compact baseline metadata supports rendering; original workspace preservation inventories are not included.

README.preparation.md is historical and does not describe current capture status. No CI or production changes.

## Approval update

The user subsequently approved this expression. See APPROVAL_STATUS.json. Historical review statements describe their original capture stage; this branch remains a standalone backup, not production integration.
