# Production36 transition validation

The initial expanded matrix exposed invalid opening + residual eyelid blends into Shocked Gasp and Delighted Discovery. Original failure receipt and reproduction are in `initial_failure/`. Approved profiles, artwork and registry constraints were not changed.

The shared runtime now prepares a trigger-fixed, eye-only three-stage bridge when a source has incompatible eye controls and the target opens its eyes within the first 0.3 seconds. It clears source aversion, then incompatible ordinary eye controls, then introduces target opening. Neutral starts and prior targets retain their prior paths. Mouth composition remains unchanged.

## Completed numeric checks

- Dense matrix: PASS, 34,550,603 checks; 25,848 source/target cases; 594,504 transition samples; 4,677 exact standalone samples across all36. Source authored keys and segment midpoints, all directed targets, and epsilon neighbors of 0.1/0.2/0.3 seconds.
- 15,946 changed samples, restricted to new-target eye-domain controls. Zero mouth changes; exact old-target parity. No scoped/bounds/mouth failures.
- Lifecycle: PASS, 519,506 checks across 19,604 cases. All source keys into the two early-opening targets, restart/release at all stage boundaries and neighboring samples, jumps, C0 continuity, exact neutral and lifecycle clearing.
- These two suites exercise production control code with face setters stubbed. They do not establish rendered pixel or native-app parity.
- Runtime SHA256 is recorded in each JSON receipt; the final-byte dense rerun completed successfully. Final runtime: `9f964e8eb2765e3bccc087992a6001768a546fef2f670f7587c1045416268bf8`.

## Actual-scene checks and limitations

`test_batch36_runtime.gd` uses the complete scene and actual face setters for 30/60Hz trajectories, authored keys, aliases, restarts/releases/resets, head/body transforms, exact face neutral and all directed midpoint transitions. Its first run was interrupted; bounded retry status is separate and must not be described as a pass without its completed JSON. Six prior-profile regression harnesses were archived byte-exact before changing only count expectations and output paths.

A bounded archived-prior27 actual-scene smoke reproduces the Godot 4.6.3 dummy-renderer custom_samplers shader error on EXP-144, but returns and exits0. The error is inherited; it does not establish that full-suite slowness is a shader deadlock. Existing direct-image export warning also persists. No rendered/native parity claim is made by these headless checks.

All execution uses workspace-local HOME and XDG locations; final retries also set LP_NUM_THREADS=2. No CI, paid resources, remote execution or publishing was used by this worker.

## Focused complete actual-object suite

PASS: 20,596 checks, all36 expressions, 180 actual trajectory samples (0/25/50/85/100%), all58 aliases, 36 restart/repeated-release/reset lifecycles and 6 cross-domain transitions with 66 boundary samples. Exact actual face snapshot neutral, fixed head/body, scope and mouth bounds checked. This is focused object-state coverage, not exhaustive 30/60Hz actual-object or rendered/native parity. See `focused_object_checks.json`.

## Exhaustive run status

The exhaustive actual-scene runtime test was attempted with a 300-second bound and exited124 (TIMEOUT), with no completion JSON. Do not treat it as a pass. The focused suite above completed successfully on the same final runtime. The approved-pair regression exceeded its 120-second bound (exit124). Composure and insight regression harnesses completed successfully; remaining regression statuses are recorded in execution_status.json after all writers finish.

All worker test processes are now stopped. Final regression outcomes: composure PASS (2,758), insight PASS (2,368), queasy PASS (5,185), hiding-smile PASS (5,184); approved-pair and stunned-silence TIMEOUT at120s. No failed assertion was suppressed. `execution_status.json` is the authoritative completed/timeout status list.
