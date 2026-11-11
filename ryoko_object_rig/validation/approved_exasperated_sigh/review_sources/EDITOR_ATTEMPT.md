# Separate native editor attempt, UNAPPROVED

All frozen preparation originals remain untouched at the original path and in the existing GitHub backup. The original capture script and baseline rig bytes are unchanged in this copy. Preparation-only status files describe the old preparation, not execution results for this new attempt. See EDITOR_AUTHORIZATION.json for the narrow denial resolution, ATTEMPT_LINEAGE.json for source hashes, and preparation_history for original freeze/guards.

Import rig/project.godot using Godot Project Manager itself. Open native_capture_runner.tscn in Godot and press F6 (Run Current Scene), with embedded game disabled if it forces viewport dimensions. Do not use F5: baseline main scene is intentionally unchanged. Never use Thunar, a shell Godot command, shell display setup, headless, or another environment.

The runner writes native PNGs and evidence only after input and native display checks. No external processes are launched by the GDScript. Existing/partial capture output is refused. Preserve failed/partial attempts; create a new named attempt for any source correction or rerun. Do not overwrite frozen manifests after native execution begins. Editor-generated .godot and .uid metadata are not frozen input sources; existing rig source files are.

Native parse/capture has NOT RUN during preparation. New freeze is explicitly a new input identity, not a repaired old receipt. All images, pose and lifecycle receipts must be validated by the unchanged encoder. Sour also requires an attributed independent native visual review against EXP-096 and EXP-091 before encoding. Review decoded frames and normal-speed playback; no numeric test constitutes visual approval.

## Attempt02 correction
Godot import automatically reordered project.godot sections. Attempt01 had no native capture output and its input guard correctly rejects the changed bytes. This separate attempt explicitly pins the already normalized configuration and transparently updates the local baseline project.godot hash only. Exact section/key/value equality against the original was verified. All other baseline files remain byte-identical. See attempt01_history and ATTEMPT_LINEAGE.json. EDITOR_RUNTIME.log is a diagnostic, not native passing evidence.
