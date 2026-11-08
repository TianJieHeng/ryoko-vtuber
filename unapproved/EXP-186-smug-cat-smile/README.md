# EXP-186 Smug cat smile: unapproved source backup

This is an exact captured-source recovery snapshot, not approved-rig integration. The 18-profile source contains twelve previously approved profiles and six explicitly unapproved profiles: EXP-158, EXP-181, EXP-102, EXP-116, EXP-050 and EXP-186. Snapshot inclusion does not approve any profile or shared runtime extension. The older EXP-003 backup remains separately unapproved and is not in this source. Approved runtime and every prior backup outside this folder are unchanged.

## Recover and verify

Obtain this entire folder from a normal clone or archive. Keep its layout intact in a writable local directory. Run `python verify_backup.py`, then `python source/tools/verify_smug_cat_smile_scope.py`. Neither command needs Godot, a network connection or the original workspace. They verify exact inventory, sizes, SHA-256, Git blob identities, source/plan/gate bindings, approval boundaries, append-only registry and exact predecessor/runtime/art bytes.

`source/` contains exactly 628 files: 627 indexed files and their self-excluded freeze, including 182 PNGs. It is byte-identical to the reviewed actual-capture source, with no delivery overlay. `BACKUP_MANIFEST.json` is the complete recovery inventory. Inherited READMEs, releases, manifests, test counts and statuses remain unchanged historical provenance. In particular, frozen EXP-186 status retains pre-capture wording. The outer `VALIDATION_SUMMARY.json` and unchanged actual-review records state the later technical PASS.

## Reproduce locally

Keep the backup pristine and make a working copy. Use Godot 4.6.3 and the packages in `source/requirements.txt` locally. Import `source/project.godot`, open the existing expression viewer, select Smug cat smile and play. Godot creates caches only in the working copy. Do not integrate this registry into the approved runtime without user approval.

Run Godot `--headless --path source --script res://tests/test_smug_cat_smile_runtime.gd` for runtime checks. Use `--headless --path source --script res://tools/review_smug_cat_smile_trajectory.gd -- --validate-only --plan=<absolute capture_plan.json path> --output=<new absolute output directory>` for deterministic preflight. To reproduce renderer samples locally, remove `--headless` and `--validate-only`, reserve the local display exclusively and add `--coordinator-display-lease-granted` after `--`. Do not run concurrent graphical captures. Keep outputs outside this backup. The helper produces 582 full/native checkpoint pairs; raw frames and movies are deliberately excluded.

## Gate records and limits

`original_reference/INDEX.json` pins the nine original panels and sheet to commit `7693d1b8718c3bb1c717bd586fb472a7efc42403`; all ten reuse exact existing Git blobs. The 3.40-second timing is newly authored from still panels, not recovered animation. The corrected sequence retains watchful amber/pupil windows, an amused broad screen-right-biased sealed grin, and exact neutral return.

Independent actual-performance review passed the bounded trajectory: 582 states, 1,164 actual images, all 237 unique native mouth crops, ten static-anchor timestamps, 118 matching repeated-cycle timestamps, lifecycle/bridge contexts and exact neutral returns. The 111 epsilon pairs differed by at most two channel levels. This backup does not claim a new render of all prior profiles or observed normal-speed playback. Canonical lower-lid/lash curvature and fuller lips remain approximations of the source painting. The original overclosed static v1 HOLD and the permitted refinement remain historical records, not erased by later PASS. Earlier runtime verification reused completed imports after a disclosed cold-import exit 137; no fresh cold-import success is claimed.

`gate_records/` retains concise unchanged reports, gates and receipts. Its index describes provenance. Gate verdicts name omitted external/raw evidence and are historical audit records, not claims that every original capture file is packaged. The backup manifest alone defines the complete recovery payload. The backup worker verified source/recovery identity, not a new visual acceptance.

Technical PASS and backup publication do not grant user approval. Final media delivery is separate. No normal-speed playback observation, live AI/TTS, real socket test, CI, paid resource, hardware flashing or remote-machine execution is claimed. Raw render dumps, diagnostic images, movies, ZIPs and generated caches are excluded.
