# Shared backbone validation

This migration reuses the approved v6 separate-part rendering and yawn data. It is a shared application/controller foundation, not completion of the remaining expression catalogue or a full VTuber/voice integration.

## Frozen inputs and deliberate changes

The original approved project was read-only throughout. A 652-file baseline hash inventory was recorded before creating the working copy; a later comparison found zero changes to the approved source.

Within the working copy, all existing artwork, shaders, `object_face.gd`, `object_rig.gd`, original tests, yawn-stage review code and `yawn_performance.json` remain byte-identical. The only changed pre-existing files are:

- `project.godot`: generic one-rig default app.
- `yawn_rig.gd`: thin compatibility wrapper.
- `README.md`, `CONTROL_API.md`: current app and contract.
- `tools/verify_object_base.py`: default-scene expectation intentionally changes to the generic viewer.
- `tools/verify_teeth.py`: explicitly separates the `project.godot` application migration from unchanged artwork/rendering hashes. The historical baseline identity file itself is unchanged.

New source comprises the registry, shared player, one-rig viewer, registry data, backbone tests and parity tools. The packaging manifest must be regenerated for the actual selected package; the inherited historical source manifest is not a current-backbone checksum claim.

## Tests run on Godot 4.6.3

- Existing base suite: **8,034 checks passed**.
- Existing yawn/stage suite, unchanged through compatibility wrapper: **55,975 checks passed**.
- Existing teeth/cap suite: **17,017 checks passed**.
- New backbone suite: **101,890 checks passed**.
- Python source checks: **131 base**, **29 oral**, **295 focused teeth/cap** checks passed.
- Default app starts successfully. Actual rendered neutral/peak/release images were captured. Slider/checkbox signals and actual engine keyboard-event routing were tested.

The new suite covers registry/schema/ID/alias errors, time ordering, unknown channels, finite bounded values, neutral endpoints, defensive copies, atomic failed catalogue loads and control transactions, hostile public API argument types, no-op commands, deterministic repeats, ownership, release/retrigger/manual interruption/reset, auto-blink handover, all supported channel endpoints and 10,001 bounded samples. A second test-only definition is loaded transiently to prove generic dispatch; it is not a new authored emotion or shipped registry entry.

## Actual renderer parity

An isolated copy of the original v6 project and the candidate ran the same capture harness with Godot OpenGL compatibility rendering and fixed 30 Hz control steps. The original project was never imported or modified in place.

- **10,001 dense sampled poses: exact equality.**
- **652 recorded poses/phases/times: exact equality.**
- **652 full 1136×800 rendered-frame pixel hashes: exact equality.**

The sequence contains 468 frames covering two complete standard cycles and neutral tail, then 180 interruption/retrigger/release/manual/reset frames plus four immediate command-boundary captures. Candidate PNGs for the complete sequence are saved outside source. This compares same-engine rendered pixels against the approved source replay, not encoded MP4 bytes or a claim that every frame corresponds one-to-one to the older movie's startup encoding schedule.

The prior approved MP4 remains unchanged: SHA256 `c9a7f6d1510bc214529c5fb8aa8cc8a4bb1850784b71f6d1beb631e96be1528b`. No normal-speed playback was performed for this migration. Automated pixel parity, chronological image inspection and playback are distinct checks.

## Explicit lifecycle corrections

These deliberately differ from historical edge behavior and are separately tested:

1. Release reports ownership immediately rather than waiting one tick.
2. Trigger/release capture displayed auto-blink lids before disabling auto blink; release returns without a lingering auto-blink floor.
3. `reset:false` alone does not cancel playback. An empty command does not rewrite internal pose state.
4. Public timing/control forwarding rejects booleans, numeric strings and other wrong types instead of coercing or throwing at a typed argument boundary.

Standard yawn and tested ordinary interruption/release imagery remain identical. Edge behavior fixes are not described as identical historical behavior.

## Reproduce

Run the commands in `README.md`. For graphical parity on a Linux host with the supplied Xorg dummy-display setup, Godot and xauth:

    bash tools/capture_backbone_parity.sh /path/to/approved-v6/project /tmp/ryoko-backbone-parity

The helper copies the baseline before adding the capture harness, leaves its input untouched and writes outputs outside both projects. It compares dense samples, controls and all frame pixel hashes. The harness/comparison were executed against both project copies; the convenience shell wrapper was syntax-checked separately.

Generated captures, movies, `.godot`, Python caches and intermediate diagnostic imagery are not runtime dependencies and must not be included as bulk publication output. A clean source package must regenerate omitted assembly intermediates before source-identity checks.

## Remaining limits

Nonzero gaze, expanded hair range, non-neutral discrete visemes, independent earrings, additional performances, full-body motion and external AI/voice transport are not implemented. The direct shared Godot API is ready for an adapter, but no live integration is claimed. Historical validation/provenance documents remain historical evidence; this file describes the new backbone checks.
