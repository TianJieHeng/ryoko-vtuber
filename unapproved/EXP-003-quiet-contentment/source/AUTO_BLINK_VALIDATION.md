# Published auto-blink restoration correction: historical receipt

This section preserves the focused correction review at publication 8c349e29, before EXP-003 integration. Its historical six-profile counts and execution receipts are not claims about the current seven-profile candidate. The current EXP-003 descendant inherits this exact runtime correction; see CONTENTMENT_SCOPE_VALIDATION.md for fresh validation. This is not a replacement for the existing cumulative source archive. Saved review checkpoints and the historical final-review receipt retain their original pre-publication wording. Exact parent: `e4369727e7597894d6c2747d06e3cb7ff5b119ca`; parent inventory SHA256 `dfe5c6023d09215812561c6ae52a30949c7d64c5cfae8f8ad166f5ee454dd9fd` (442 files, 182 PNGs).

## Correction and boundaries

The shared player now retains enabled auto-blink intent while an authored performance or release owns the face. It restores blinking only after completed exact-neutral recovery. Retrigger, cross-profile handoff, repeated release and interrupted release retain intent; the temporary false actual state is not a new preference. Initially disabled stays disabled. No new default-on behavior.

Manual takeover, explicit `auto_blink:false` and reset cancel deferred intent, including false-to-false disabling during suspension. Empty, invalid, read-only and genuine no-op calls retain it. `auto_blink:true` remains an immediate manual-control write, not a queued preference. Reset plus an explicit enable still enables after resetting. The viewer's checked preference and actual active/paused/off label make these different states visible. Unchecking a suspended preference takes manual ownership immediately; no separate cancel-only command is added.

At neutral completion, the existing base cycle restarts at elapsed zero. It retains its 4.2-second period and final .34-second sinusoidal closure, avoiding a jump back into the captured mid-blink. The `elapsed` field is used only for this base blink policy, not unrelated body/hair motion. The existing player discards completion-call overshoot at the recovery boundary; the next idle advance starts the cycle. Pausing processing cannot cause timer-driven restoration. `advance(0)` preserves pose/time/ownership and intent, although its inherited phase-label refresh remains. Zero-duration profile definitions remain invalid.

All 182 PNGs, six authored profiles and timing, registry, object face, base renderer/blink policy, shaders, geometry, gaze, mouth purse, 30.8-source-pixel physical mouth limit and fixed white enamel anchor remain byte-identical. No extra eye-family selector exists in this parent: zero smile-eye controls restore the ordinary lid owners. No new deformation, opacity crossfade, body motion or artwork is introduced.

## Executed checks

- Godot 4.6.3 headless import and all 19 runtime suites passed, including all 18 prior suites. The new lifecycle suite passes 24,716 checks. Two prior tests are narrowly updated where they explicitly asserted obsolete non-restoration after initially enabled blinking; disabled cases remain unchanged.
- Coverage includes both prior preferences, all six profiles, completion and release, all 36 cross-profile transitions, repeated release/retrigger, partial release handoff, exact floating-point recovery threshold, zero elapsed, paused processing, invalid transactions/no-ops/read-only calls, manual/disable/reset cancellation, later retrigger after cancellation, UI preference/actual-state reporting, and bounded callable bridge parser/dispatch. No listener is opened by the new tests.
- The new exact-hash source scope guard and the existing relief, reassurance, giggle, welcome, closed-smile and blush validators pass. Old migration receipts are unchanged; two legacy guard entry points follow an exact pinned correction, not a broad allowlist.
- An isolated rebuild passes build_object_face, object base, yawn, teeth, gaze assets/coverage, lid handoff, smile support, spread support, closed smile and blush checks.

## Actual rendering

The supported existing graphical desktop Terminal launched Godot 4.6.3, Compatibility OpenGL 4.5, Mesa 25.0.7 / llvmpipe. No display server or listening transport was created. Both exact-parent and candidate processes exited 0.

Candidate: 147 native 1136 × 1384 images, 13,273 assertions, zero failures. One direct idle-blink reference supplies nine phase samples at elapsed 3.86, 3.9025, 3.945, 3.9875, 4.03, 4.0725, 4.115, 4.1575 and 4.2 seconds. After each of six profiles, for both completion and release, all 108 blink phase images are pixel-exact with that ordinary-idle reference. All 12 immediate recovery images equal open neutral. Three before/after cancellation pairs remain pixel-identical after 4.03 seconds and later performance cannot resurrect the canceled preference.

Against the exact parent, all 12 disabled-mode raster samples are pixel-exact: one .6-second pose and one completed release for each profile. Additionally, 1,416 controller/object-state samples over two complete 30-Hz cycles per profile match exactly after removing only the additive pending-intent field. This state comparison is not a claim that all 1,416 frames were rendered. The sampled resumed blinks include the full close/reopen progression and return to ordinary family/hair behavior, including after laughter. Native eye crops were inspected; inherited fine hair/lash raster edge traces remain, not an artifact-free-art claim.

Reproduce state tests with `godot --headless --path . --script res://tests/test_auto_blink_lifecycle.gd` using writable HOME/XDG. The real-render harness is `tools/review_auto_blink.gd`; launch through the supported existing graphical Terminal with `--output=/absolute/output`, without `--headless`. `--baseline-only` executes the unchanged disabled comparisons on a separate exact-parent copy with only this harness added. Do not modify the immutable parent itself. Full per-frame state, pixel hashes, comparisons and logs are supplied as external review evidence rather than runtime artwork.

## Honest limits

The nine-point images are deterministic phase samples, not a normal-speed video. No normal-speed playback, actual AI model, TTS integration or real-process socket test is claimed. At review time, no CI, remote-machine execution, hardware flashing, paid resource, dependency installation, external push or EXP-003 integration had occurred. Publication changes current status wording and its dependent hashes only; runtime, art, profiles, tests and historical review receipts remain the independently verified source. The repository commit records publication.
