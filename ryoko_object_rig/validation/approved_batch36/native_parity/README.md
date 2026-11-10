# Approved batch36: native parity preparation and separate numeric evidence

Fresh native pixel verification is **BLOCKED**, not passed. No native images were captured and zero of 180 planned image comparisons ran. See `RESULT.json` and `Xorg_launch_failure.log`.

Godot 4.6.3 is installed. DISPLAY and WAYLAND_DISPLAY were unset, no active X server was found, and Xvfb is absent. The installed Xorg dummy driver and existing `/etc/X11/xorg.conf` were tried locally on display :96 with TCP disabled, first ordinarily and then with the sandbox override. Both attempts failed at local/Unix socket creation. An independent Python `socket.socket(AF_UNIX)` probe raised `PermissionError: [Errno 1] Operation not permitted` before bind. No software was installed, no network transport workaround was attempted, and no remote machine was used.

## Prepared native harness

`native_parity_harness.gd` loads the actual production registry36 without injecting profiles. It resets and plays each registered expression at 10 selected 30fps checkpoints, spanning neutral bookends, onset/build, peaks/holds, and release. Focused determination includes the closed refocusing blink and reopened eyes. Creeping dread uses its actual 4.8-second duration; quiet contentment uses 4.6 seconds. The other profiles use 4 seconds.

Full view is 568x800. Detail view is 400x360 with the exact source capture transform. `expected_checkpoints.json` contains all 180 expected SHA-256 hashes of raw RGBA bytes, plus source profile and original motion-check file digests. These are expected source hashes, not newly measured production hashes.

The harness passes Godot `--headless --check-only` parsing. It explicitly rejects actual headless execution; dummy rendering must not be interpreted as pixel parity. With an authorized functioning local X11 display, run from the project root:

```
godot --rendering-method gl_compatibility --audio-driver Dummy --path . --script res://validation/approved_batch36/native_parity/native_parity_harness.gd
```

Use writable XDG_DATA_HOME, XDG_CONFIG_HOME and XDG_CACHE_HOME paths if the environment requires them. Preserve the current BLOCKED receipt before rerunning. A successful native run replaces RESULT.json and writes captures. Native frame samples still do not establish normal-speed live pacing or coverage of the earlier 27 expressions.

## Separate nonvisual evidence

`byte_identity.json` verifies each of nine production profile files against its approved source. It also compares 39 root/parts GDScript, shader, scene and project files against each candidate baseline. All nine profiles remain byte-identical. After the bounded transition repair, 342 of 351 runtime comparisons are byte-identical; expression_rig.gd differs in each of the nine baseline comparisons. byte_identity.json records the prior source and current production hashes. Overall runtime byte identity is therefore false. Pre-repair receipts are archived in pre_repair/ and are not final evidence. Tests, validation, tools and generated import caches are outside this runtime comparison.

`numeric_source_parity.gd` independently samples actual production registered neutral cycles against every 30fps pose in the original native motion records. `expected_states.json` preserves those source poses. Its result and log are separate from the BLOCKED native result. Numerical parity cannot establish fresh renderer output or human-observed timing.

This validation worker did not edit production runtime, profiles, or existing tests. A separate transition-safety repair changed expression_rig.gd before the final numeric rerun.

Final numeric result is recorded in numeric_source_parity.json after rerunning against the repaired runtime. The headless log contains a shader compiler custom-sampler diagnostic, but this complete numeric run exits successfully with code 0. That diagnostic is not evidence of a stall or crash and is not established as the cause of slow or uncompleted broader scene suites. Numerical checks do not establish native renderer output.

Final post-repair numeric result: PASS; 1,131 frames, 33,930 channel comparisons, 36,194 checks, zero failures. Maximum absolute error 4.88498130835069e-15 (<1e-9). Validated expression_rig.gd SHA-256: 9f964e8eb2765e3bccc087992a6001768a546fef2f670f7587c1045416268bf8. Fresh native comparisons remain zero and BLOCKED.
