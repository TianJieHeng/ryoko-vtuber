# Approved batch integration: 36 performances

The user approved all nine delivered previews: Focused Determination v2 (EXP-139), Sleepy Annoyance (EXP-174), Creeping Dread (EXP-067), Bitter Taste (EXP-093), Quiet Contentment (EXP-003), Silent Fury (EXP-043), Shocked Gasp (EXP-064), Delighted Discovery (EXP-004), and Cold Glare (EXP-042).

Base main: 816d77fafb6e016dc70f0802743d444e618f7b0f. The exact reviewed JSON bytes and MP4s are retained under validation/approved_batch36. Profile metadata saying UNAPPROVED is the historical review artifact; current approval is recorded by RELEASE.json and APPROVED_INTEGRATION_STATUS.json. Focused Determination is the reviewed v2, not v1.

## Preservation

All 27 prior profiles, scenes, shaders and 184 PNGs remain byte-exact. A bounded runtime transition repair clears incompatible eye controls before introducing early incoming opening; all 36 standalone trajectories and prior27-to-prior27 handoffs are checked against the archived runtime. No new artwork, anatomy, controls, head/body motion, automatic blink or speech capability was added. Previous metadata, changed tests and source guard are archived under historical_capture_metadata/approved27_before_batch36. Registry additions and the scoped incoming-eye transition repair are the only production behavior changes. Initial failure evidence is retained separately.

## Fresh validation

- bridge_lifecycle_checks.json: 519506 checks passed.
- focused_object_checks.json: 20596 checks passed.
- handoff_boundary_checks.json: 34550603 checks passed.
- opening_independent_audit.json: 5016 checks passed.
- regression_recovering_composure_runtime/motion_state_checks.json: 2758 checks passed.
- native_parity/numeric_source_parity.json: 36194 checks passed.
- regression_hiding_smile_runtime/motion_state_checks.json: 5184 checks passed.
- regression_sudden_insight_runtime/motion_state_checks.json: 2368 checks passed.
- regression_queasy_runtime/motion_state_checks.json: 5185 checks passed.

See APPROVED_INTEGRATION_TEST_RESULTS.json and validation/approved_batch36 for precise scopes, hashes and failure lists. Dense tests exercise actual production control code with rendering setters stubbed; actual-object lifecycle tests and exact candidate source/native-record comparisons provide complementary evidence. Fresh native capture could not run because the current session forbids local display sockets; original approved MP4s and native records remain available. This is not a new visual parity pass, normal-speed playback check or rendered cross-transition review.

## Limits retained

Fresh native production rendering is BLOCKED by display socket restrictions. Any time-bounded actual-rig suite that did not complete is listed as uncompleted in the validation receipts; it is not a pass. The inherited headless custom_samplers diagnostic also occurs in a successfully completed prior27 smoke run, so it is not claimed as the cause of unfinished runs.

Existing outer eyelid/hair edge fragments, rigid facial approximations and each candidate's documented source-fit limits remain. Whole-rig full-trajectory native parity was not rerun. Live engine pacing and continuous normal-speed observation remain unverified. Inherited EXP-114 pacing HOLD, EXP-148 limitations, dummy-renderer custom_samplers diagnostics and runtime-image export warning are unchanged. No export, remote-machine execution, CI or paid resource was used.

Run python3 tools/verify_approved_integration.py for inventory, predecessor preservation, profile identity and receipt verification. Run sha256sum -c APPROVED_SOURCE_FILES.sha256 for the pinned source manifest.
