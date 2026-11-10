# Approved integration: 39 performances

Mental Arithmetic (EXP-129), Controlled Anger (EXP-041) and Broad Surprise (EXP-061) are user-approved and registered alongside the prior 36 performances. Exact reviewed profile JSON and MP4 bytes are retained. Historical candidate labels remain untouched; RELEASE.json records current approval.

Base main: 3ce98774282ad6c20dfbd7018d20838ff861b762. This integration changes no runtime code, artwork, scenes, shaders or existing profile bytes. Only the production registry gains three entries and aliases mental_arithmetic, controlled_anger and broad_surprise. All 184 baseline PNGs remain byte-exact. Prior release metadata and the source guard are archived under historical_capture_metadata/approved36_before_mental_arithmetic.

## Current 39 validation

- Actual instantiated scene: 111,359 checks passed. All 363 chronological state samples match approved preview records, aliases work, 33 keyframe restart/repeated-release/reset cases pass, and all 225 directed pairs involving a new profile pass at 2,475 handoff checkpoints with exact neutral face/control completion.
- Dense production controller with rendering setters stubbed: 1,990,743 checks passed. All 8,560 prior36 standalone samples at 60 Hz are exact, 4,611 key/midpoint handoffs pass 50,721 boundary samples, and 9,222 interrupted lifecycle cases complete safely.
- Native Godot desktop: all three new profiles replayed for 121 chronological frames each at 30 fps. All 726 full/detail RGBA hashes match their approved previews. Independent PNG decode, dimensions and hashes also passed. This proves deterministic frame parity, not live pacing or rendered cross-transition review.
- Completed intermediate37 and38 state checks are retained with their original scope. They do not substitute for current39 tests.

## Dated native recovery for the prior release

On 2026-11-10, the supported desktop UI route passed 731 checks and 180 exact full/detail native comparisons at 90 checkpoints across the nine profiles added in the prior36 release. Evidence is preserved in validation/approved_mental_arithmetic/prior36_native_parity. It supersedes the historical display-socket-blocked claim for that specific checkpoint scope only. Historical documents and failure receipts remain unchanged. Neither that recovery nor this integration proves full-trajectory native parity for all prior36 profiles.

## Limits retained

Mental Arithmetic uses rigid lowering and opposing tilt to approximate brow pinching; it adds no horizontal convergence. Controlled Anger uses existing rigid brow lowering/tilt, narrow ordinary lids and sealed lip pressure. Its 0.65-to-0.38 pressure easing is numerical only: peak/easing images are pixel-identical, so no visible lip-first release is claimed. Broad Surprise has more restrained eye opening and jaw movement than its reference. No new anatomy, speech capability, head/body motion or automatic blink behavior was added.

Whole-rig full-trajectory native parity, rendered cross-transition review and continuous live pacing remain unverified. Inherited EXP-114 pacing HOLD, EXP-148 qualifications, known eye-edge fragments and other documented rig limits remain. Headless state logs may retain the inherited custom_samplers dummy-renderer diagnostic; native pixels were captured through the supported desktop route. No CI, remote execution, export, paid resources or production artwork changes were used.

## Reproduce

Run python3 tools/verify_approved_integration.py and sha256sum -c APPROVED_SOURCE_FILES.sha256. Run tools/test_approved_guard_negative.py with a new external output directory for disposable tamper probes. Run Godot headlessly with tests/test_approved_batch39_actual.gd and tests/test_approved_batch39_dense.gd for current39 state checks. Historical tests retain their original registry counts. Native launcher code and expected hashes are under validation/approved_batch39/native_parity. Prepare a separate project with tools/prepare_batch39_native_parity.py, import it in Godot's desktop, disable Game Embed Mode, reload, and run standalone. Restore the previous embedding preference afterward. Run the generated verify_native_result.py for independent PNG and source-preservation verification.
