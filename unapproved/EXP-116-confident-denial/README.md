# EXP-116 Confident denial: unapproved source backup

This cumulative source is preserved for recovery, not approved integration. It contains twelve previously approved profiles and four explicitly unapproved profiles: EXP-158, EXP-181, EXP-102 and EXP-116. Approval of one later does not approve the others or silently approve shared runtime extensions. The approved runtime outside this folder remains unchanged.

## Recover and verify

Obtain this entire folder from a normal clone or archive. Keep `source/`, `original_reference/` and the top-level verification files together in a writable local directory. No original workspace, private link, LFS transfer or new binary upload is required. Run `python verify_backup.py`, then `python source/tools/verify_confident_denial_scope.py`. The first verifies exact paths, sizes, SHA-256 and Git blob identities, cumulative approval boundaries and plan binding. The second validates the frozen 604-file inventory, the only inherited registry edit and the unchanged fifteen prior profiles and 182 PNGs.

The complete source contains 605 files: 604 indexed files plus their self-excluded freeze. `BACKUP_MANIFEST.json` is the current backup inventory. It is byte-identical to the captured source with no delivery overlay. Historical README, release records, manifests, capability documents and test counts inside `source/` remain historical provenance. The frozen status sidecar retains pre-capture wording; `VALIDATION_SUMMARY.json` records the later technical review and its evidence hashes.

## Reproduce locally

Keep this backup pristine and make a working copy. Install Godot 4.6.3 and the packages listed in `source/requirements.txt` locally, then import `source/project.godot`; Godot creates caches only in the working copy. Open the existing expression viewer, select Confident denial and play. Do not copy this registry into the approved runtime without user approval.

Run the current headless runtime test with Godot `--headless --path source --script res://tests/test_confident_denial_runtime.gd`. For deterministic trajectory rehearsal, use `--headless --path source --script res://tools/review_confident_denial_trajectory.gd -- --validate-only --plan=<absolute path to capture_plan.json> --output=<new absolute output directory>`. To reproduce actual renderer samples locally, remove `--headless` and `--validate-only`, reserve the local display exclusively and add `--coordinator-display-lease-granted` after `--`. Never run concurrent graphical captures. Put all outputs outside this backup. The harness records source/plan/profile hashes and 330 full/native checkpoint pairs. The original 660 PNGs and movies are deliberately excluded.

## Source, scope and limits

`original_reference/INDEX.json` pins the nine original EXP-116 panels and source sheet to commit `7693d1b8718c3bb1c717bd586fb472a7efc42403`, reusing exact existing Git blobs. The 2.85-second performance is authored from these still panels, not recovered animation. Firm brow/lid attention precedes a brief screen-right corner and width release. The mouth turns off before the brow/lid recovery; exact neutral begins at 2.65 seconds and holds for the final 0.20 seconds.

The shared sealed-only width capability requires `mouth_open == 0` whenever either independent width is positive. General open-plus-width remains unsupported: its epsilon activation and worsened open-wedge failures remain HOLD. All runtime, shaders, artwork and fifteen prior profile bytes are exact to the independently reviewed sealed-width baseline. EXP-116 adds only its profile, additive registry entry, tests, evidence and documentation.

The actual trajectory and independent review status are recorded in `VALIDATION_SUMMARY.json`. Technical acceptance or preservation does not imply user approval. No normal-speed playback observation, live AI/TTS connection, real socket test, CI, paid resources, hardware flashing or remote-machine execution is claimed. Encoded media and recovery archive delivery are reviewed separately. Raw frames, diagnostic images, videos, ZIPs, caches, credentials and private conversation notes are excluded.
