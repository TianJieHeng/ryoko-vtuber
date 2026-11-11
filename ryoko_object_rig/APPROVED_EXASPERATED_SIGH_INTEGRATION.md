# Approved Exasperated Sigh integration: 46 performances

Exactly one new approved expression, EXP-046 Exasperated Sigh, is registered as `exasperated_sigh` on pinned main45 `17d2efdc7028fb3ec55cc604c19835ca2b7065f4`. The profile and delivered MP4 remain byte-exact, including their historical UNAPPROVED and pre-render metadata. Current conversation approval is recorded separately and does not erase visual qualifications. EXP-091, EXP-092 and all other unapproved/skipped candidates remain excluded.

## Preservation and provenance

All 45 prior profiles, all production runtime, scenes, shaders, controls and all 184 PNGs remain byte-exact. Changed release metadata and guards are archived under `historical_capture_metadata/approved45_before_exasperated_sigh`; all other existing files remain unchanged. No whole review branch was merged. The candidate was captured against approved39; source hashes verify that its production runtime and artwork match main45 without a required runtime delta. Editor-attempt project configuration was for review only and is not integrated.

Profile SHA-256: `1de491628e031953c765a47287d3ac230abb73e6adbdab15a3f8c11d1b41161e`.

Delivered MP4 SHA-256: `ecceb235ec358e99302e78d8b065d0c2f6edf8cb4fdbe7e86a3a1abab0bd0e29`.

Selected exact review evidence, the historical native receipt, immutable source files, original independent visual review and current approval record are in `validation/approved_exasperated_sigh`. Remote backup/publication is not claimed by local tests; the publisher must verify the exact-version backup and main parent before publishing this single-expression patch.

## Current checks actually run

- 6,675,775 pure-Python numerical checks PASS: all 46 profiles, 10,815 prior45 standalone samples at 60 Hz plus exact keys, all 145 historical EXP-046 native pose records, and 44,017 all46 samples at 240 Hz plus exact keys. Maximum historical-pose error is 2.870e-8, below 1e-7.
- All 91 directed pairs involving EXP-046, including self-retrigger, pass 1,965 key/midpoint starts, 141,480 handoff boundary samples and 9,825 modeled interrupted lifecycle cases (release, restart, repeated release, reset and manual takeover).
- All 28 unchanged numerical-model unit/negative tests PASS.
- All 184 protected PNGs fully decode. All 290 existing native motion images and 20 static anchors match their recorded RGBA hashes. Native frames 0–9 and 135–144 have exact endpoint pixel identity. The original 145-frame H.264 MP4 fully decodes at 968×800 and 30 fps. This is current integrity checking of historical images, not a new visual or playback review.
- The current source/identity/preservation guard, full SHA-256 inventory and 12 disposable-copy tamper probes verify the package. Archived45 checks/receipts retain historical scope, not a claimed rerun.

## Checks not run and retained qualifications

No current46 Godot engine or scene test, native render, UI launch, rendered transition review, native parity replay or continuous normal-speed playback was run. The mathematical model does not execute GDScript or rendering setters and cannot prove displayed auto-blink or visual pacing. `tests/test_approved_exasperated_sigh_actual.gd` is prepared for future authorized execution only and is NOT RUN.

Subdued bounded upward glance, not a full eye roll; relatively flat brows do not reproduce raised inner hooks. Small tooth-visible opening can read as sleepy speech or a faint grin rather than an unmistakably unsmiling weary exhale. Detail-scale lash/hair and lip-edge artifacts remain. No continuous normal-speed playback or perceptual comparator-distinctness claim; no head/body movement.

The independent review sampled native and decoded MP4 frames rather than continuous normal-speed playback. Numerical differences from other expressions do not establish perceptual distinctness. Existing EXP-114 pacing HOLD, EXP-148 qualifications and other historical limits remain. No new anatomy, art, jaw/shoulder/breathing motion or unrestricted gaze is implemented.

## Reproduce available checks

Run from the rig directory, keeping regenerated outputs outside the frozen source tree:

    python -B tools/verify_approved_integration.py
    sha256sum -c APPROVED_SOURCE_FILES.sha256
    python -B tools/test_approved45_model_unit.py -v
    python -B tools/test_approved46_model.py /new/external/path/model.json
    python -B tools/verify_exasperated_sigh_media.py --output /new/external/path/media.json
    python -B tools/test_approved_guard_negative.py /new/external/path/guard_probes

The media verifier optionally accepts `--native-dir` for the original backed-up native capture folder. Without it, selected receipt identity, protected PNG decode and complete MP4 decode are checked, but raw capture images are not reverified. No CI, paid resources, remote execution or production artwork changes were used.
