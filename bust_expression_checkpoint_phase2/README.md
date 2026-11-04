# Ryoko facial expressions phase2: approved checkpoint

This isolated local 2D project preserves the three approved expressions and adds quiet sadness (EXP-021), knowing smirk (EXP-102), and cheeky wink (EXP-181). The new expressions were visually approved before publication.

Open project.godot here. The --demo option cycles all six expressions with speech/blink states. Source commands and speech-release semantics match the approved first expression phase.

Review previews/EXP-021_approval_comparison.jpg, EXP-102_approval_comparison.jpg, and EXP-181_approval_comparison.jpg. Each uses the exact reference crop beside actual assembled rest/speech/blink combinations. These are sprite composites, not graphical runtime captures.

The cheeky wink closes viewer-right (character-left) at rest. Its closed eye uses identical artwork during blink, so releasing blink cannot reopen it. Both-eye blink additionally closes viewer-left. Speech changes only the mouth.

No head/neck/body deformation, continuous eyelid motion, audio phoneme analysis or secondary physics is added. Prior published checkpoints remain untouched; this is a separate self-contained project.
