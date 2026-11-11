# Approved integration: 45 performances

Six exact user-approved previews are registered on pinned main39 (`419450d2302d471aa009557289ad509ffb413349`): EXP-123 Puzzled, EXP-081 Mild Disgust, EXP-161 Sleepy, EXP-045 Irritated Side-eye, EXP-104 Triumphant Grin and EXP-096 Headache Tension. Aliases are `puzzled`, `mild_disgust`, `sleepy`, `irritated_side_eye`, `triumphant_grin` and `headache_tension`.

## Exact preservation and authorization

All six profile JSONs and MP4s are byte-exact to their pinned review commits. The original historical pending/unapproved labels remain untouched; `validation/approved_batch45/current_user_approvals.json` records subsequent conversation approval, including Puzzled's later “yah thats good.” Full review packages remain on their existing review commits. This is selective integration, not a merge/cherry-pick of entire review branches.

All 39 prior profiles, production runtime, scenes, shaders, controls, and all 184 PNGs remain byte-exact. Candidate baseline comparisons show no required runtime or artwork delta. Prior release metadata/guards are archived under `historical_capture_metadata/approved39_before_batch45`. Review identities, exact retained source paths, Git blob IDs, hashes and compatibility evidence are under `validation/approved_batch45`.

EXP-046 Exasperated Sigh, EXP-091 Overly Sweet Taste and EXP-092 Sour Taste reconstructions are not registered or included. Skipped and other unapproved candidates remain excluded. This release does not merge backup branches, remove historical failures, or alter old review claims.

## Current checks actually run

- 27,453,131 assertions PASS in a source-backed Python mathematical model. It compares 9,369 prior39 standalone samples at 60 Hz plus exact keys, all 726 historical approved pose records, and 42,864 samples across all45 profiles at 240 Hz plus exact keys. Maximum review control error is 2.915e-8 (tolerance 1e-7).
- All 504 directed expression pairs involving a new profile pass 10,356 source key/midpoint cases and 745,632 boundary samples. 51,780 modeled release, restart, repeated-release, reset and manual-takeover cases pass. These exercise modeled pose/ownership/blink-intent mathematics, not actual rendered blink behavior.
- All 28 Python model unit/negative tests pass.
- All 184 unchanged PNGs fully decode. The six byte-exact historical MP4s fully decode: 121 frames each, 726 total, H.264 at 30 fps and 968 x 800. This is current integrity checking, not a new visual or playback review.
- Current source guard and complete SHA-256 inventory pass. All 12 disposable tamper probes are rejected, with clean restored copies passing. Source guards also inspect old records; they do not rerun historical native tests.

## Checks not run and retained limits

**No current Godot engine/scene test, native render, UI launch, RGBA parity replay, rendered cross-transition review, or continuous playback/pacing test was run for this integration.** The Python model is not the production GDScript runtime and cannot establish those results. Engine access was outside this worker's allowed scope. Two updated actual-scene and dense-controller Godot test scripts are provided for a future authorized run; their existence is not a test pass.

Historical review evidence is preserved with its original scope. The existing EXP-114 pacing HOLD, EXP-148 qualifications, fine eye/lash/hair artifacts and other documented limitations remain. No new anatomy, independent lip lift, downturned corner, central furrows, jaw control, speech, head/body gesture, or automatic blink capability is claimed.

New expression qualifications:

- EXP-123: Subtle sideways pout only; no whole-mouth translation or diagonal source contour. No head tilt. Intermittent playback samples do not establish continuous normal-speed observation.

- EXP-081: Reads as restrained smirk or skeptical objection. Independent upper-lip curl/lift and nose detail are unsupported. User approved after that limitation was disclosed. No continuous playback observation or source-faithfulness claim.

- EXP-161: Heavy partial lids with a small tooth-visible horizontal opening approximate Sleepy; no anatomical jaw movement. Operator sampled normal playback; no continuous observation claimed.

- EXP-045: The independent downturned mouth corner is unavailable and omitted. All mouth controls remain neutral and sealed; the sideways glance, lids and unequal brows approximate the reference. Operator sampled ordinary playback; continuous observation and formal perceptual A/B comparison are not claimed.

- EXP-104: Native grin is softer, narrower and less intense than source. Existing upper tooth arch; exact opposing-teeth clench unsupported. Operator normal Play reached the neutral endpoint, but only that endpoint was observed. No continuous playback observation claimed.

- EXP-096: Restrained tense closure with still-closed softening. No true central furrows, horizontal brow convergence or independent downturned mouth corners. Not unmistakable headache/pain. Operator sampled ordinary-speed playback; continuous observation is not claimed. Meditative Calm comparator is verified historical single-anchor evidence, not a new all-frame or playback comparison.

## Reproduce the checks that are available

Run from this rig directory:

    python -B tools/verify_approved_integration.py
    sha256sum -c APPROVED_SOURCE_FILES.sha256
    python -B tools/test_approved45_model_unit.py -v
    python -B tools/test_approved45_model.py /new/external/path/python_model_checks.json
    python -B tools/test_approved_guard_negative.py /new/external/path/guard_probes

The dense model accepts an external output path so a rerun need not alter frozen receipts. The tamper runner uses disposable copies only. Future authorized engine suites are `tests/test_approved_batch45_actual.gd` and `tests/test_approved_batch45_dense.gd`; run in a disposable project copy and preserve new provenance. Neither is claimed executed here. No CI, remote-machine execution, paid resources or artwork changes were used.
