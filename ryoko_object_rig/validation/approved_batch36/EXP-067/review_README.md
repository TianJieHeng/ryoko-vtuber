# Creeping Dread EXP-067 review v1

UNAPPROVED preview. Not integrated. Approved main remains at 27 expressions.

Native capture completed: 496 static and 9,021 motion checks passed. The 145-frame MP4 is 968x800 H.264, 30 fps, 4.833333 seconds. Authored motion spans 4.8 seconds. Independent review verified native frame hashes, exact neutral bookends, preserved body and 1,124 baseline files including 184 PNGs in the original workspace. See REVIEW.md and REVIEW_SUMMARY.json for visual limitations. Headless checks are numerical checks, not a visual-render substitute.

This reads as mild apprehension rather than strongly tense source dread. The retained upper teeth can suggest a nervous smile. No new artwork or runtime modification is included. Normal-speed GUI review was not part of the independent review receipt. A subsequent sampled 1x playback inspection is recorded in PLAYBACK_INSPECTION.md; no continuous playback claim is made.

## Reproduce

Use the repository at baseline commit 816d77fafb6e016dc70f0802743d444e618f7b0f. Copy its ryoko_object_rig into a local rig directory beside these files, preserving production source files. Run Godot import as needed. Candidate tests add EXP-067 only in memory, not in the production registry.

Run `python run_gate.py --rig rig` for static state checks, `sh run_motion.sh --state` for motion state checks. On a supported desktop display, run `python run_gate.py --rig rig --capture` and `sh run_motion.sh --capture`. Then run `python encode_preview.py` (the encoder refuses to overwrite the included MP4; preserve that file first). Godot 4.6.3 OpenGL compatibility and FFmpeg were used for the original capture.

The compact BASELINE_FREEZE.json contains only baseline metadata needed by rendering scripts. Original-workspace preservation checks require the full retained local manifest and are not represented as portable here. Native image sequences and broad unrelated baseline inventories are not copied into this backup. REVIEW.md references evidence retained in the original workspace; this backup includes its conclusions, scoped receipts, source profile, harness, and delivered video. No CI, paid resources, hardware flashing, or remote machine execution.

Original preparation-stage notes are retained locally in README.preparation.md.
