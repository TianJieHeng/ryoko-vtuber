# Approved Overly Sweet Taste integration: 47 performances

Exactly one new approved expression, EXP-091 Overly Sweet Taste, is registered as `overly_sweet_taste` on pinned main46 `4a2d632e54b23ae8c3477940b5d4aed325232028`. The profile and delivered MP4 remain byte-exact, including historical UNAPPROVED and pre-render metadata. Subsequent user approval is recorded separately and does not erase visual qualifications. EXP-092 and other unapproved/skipped candidates remain excluded. Publication is effective with the containing release commit; local source preparation does not itself assert remote push success.

## Preservation and provenance

All 46 prior profiles, all production runtime, scenes, shaders, controls and all 184 PNGs remain byte-exact. Changed release metadata and guards are archived under `historical_capture_metadata/approved46_before_overly_sweet_taste`; every other predecessor file remains unchanged. No whole review branch was merged. The candidate was captured against approved39; current source hashes verify production runtime and artwork identity with main46 without a runtime delta. Review-only editor adapter/configuration is not integrated.

Profile SHA-256: `67cae056cbc90fe0de20820131d750a97ada4ccc0340575ee43ec18963bbda6a`.

Delivered MP4 SHA-256: `035ed33369ba957d2e2c1275cee377b0f9a21d3b6b2c529ea88592dbddfb4d19` (225,487 bytes).

Exact selected review files, historical native receipt, source manifests, original public QA and later user approval are in `validation/approved_overly_sweet_taste`. Original timestamps/receipts were not rewritten. The original exact-float preflight failure and subsequent finite 1e-12-second tolerance are documented in preserved QA, validator lineage and diff. Current integrity checks use that same tolerance.

## Current checks actually run

- 6,613,546 pure-Python numerical checks PASS: all 47 profiles, 11,104 prior46 standalone samples at 60 Hz plus exact keys, all 121 historical EXP-091 chronological pose records, all 270 historical lifecycle poses and nine static anchors, plus 44,978 all47 samples at 240 Hz and exact keys. Maximum historical-pose error is 2.980e-8, below 1e-7.
- All 93 directed pairs involving EXP-091, including self-retrigger, pass 1,917 key/midpoint starts, 138,024 handoff boundary samples and 9,585 modeled interruption cases (release, restart, repeated release, reset and manual takeover).
- All 28 unchanged numerical-model unit/negative tests PASS.
- All 184 protected PNGs fully decode. All 242 existing native motion images and 18 static anchors match both file and RGBA hashes. All 1,175 original frozen inputs match. Native frames 0–6 and 113–120 have exact neutral pixel identity. The exact 121-frame H.264 MP4 fully decodes at 968×800 and 30 fps, 4.033333 seconds. These are current integrity checks of historical local images, not a new visual or playback review.
- The completed source/identity/preservation guard, complete SHA-256 inventory and 12 disposable-copy tamper probes passed before the publication-only metadata update. Predecessor tests/receipts retain historical scope, not a claimed rerun.

## Checks not run and retained qualifications

No current47 Godot engine or scene test, native render, UI launch, rendered transition review, native parity replay or continuous normal-speed playback was run. The mathematical model does not execute GDScript or rendering setters and cannot prove displayed auto-blink or visual pacing. `tests/test_approved_overly_sweet_taste_actual.gd` is prepared for future authorized execution only and is NOT RUN.

Source fit NOT PASSED: peak reads pleased/bashful more than unmistakably overloaded by sweetness. Raised-inner-brow strain and pinched-mouth tension remain weaker than the source. Jagged lash/hair edges and small bust-scale mouth changes remain. No continuous normal-speed playback or native comparator review against Kiss, Shy Laughter, Queasy and Headache. User approval is distinct from these retained review qualifications.

The historical reviewer sampled native and decoded MP4 frames rather than continuous normal-speed playback. Numeric differences do not prove perceptual distinctness. EXP-046 bounded-glance qualifications, EXP-114 pacing HOLD, EXP-148 qualifications and all other historical limits remain. No new anatomy, artwork, head/body movement or unrestricted gaze is implemented.

## Publication and backup scope

The user explicitly directed this single-expression main publication without further validation or waiting for a backup. Remote exact-version backup is NOT VERIFIED. No commit or push was attempted by this integration worker; the publisher verifies remote success separately. Raw native PNGs are not included in this patch, and local image verification does not establish a complete remote capture archive. Counts describe 47 approved profiles in the containing release commit once published.

Only publication metadata and matching source-guard expectations were updated after the completed checks. Model, media, unit and source-tamper receipts remain unchanged. Dependent inventories were regenerated; no model/media/unit/guard test replay was run for this metadata update, as instructed.

## Reproduce current checks

Run from the rig directory, writing new outputs outside the frozen source tree:

    python -B tools/verify_approved_integration.py
    sha256sum -c APPROVED_SOURCE_FILES.sha256
    python -B tools/test_approved45_model_unit.py -v
    python -B tools/test_approved47_model.py /new/external/path/model.json
    python -B tools/verify_overly_sweet_taste_media.py --output /new/external/path/media.json
    python -B tools/test_approved_guard_negative.py /new/external/path/guard_probes

The media verifier optionally accepts `--native-attempt` for the original local attempt02 folder. Without it, protected PNG decode, selected receipt identity and complete MP4 decode are checked, but omitted raw images/frozen inputs are not reverified. The original reviewed attempt is not reconstructed by this patch. No CI, paid resources, remote execution or production artwork changes were used.
