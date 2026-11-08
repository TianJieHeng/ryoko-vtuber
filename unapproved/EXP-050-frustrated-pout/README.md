# EXP-050 Frustrated pout: unapproved source backup

This is an exact captured-source recovery snapshot, not approved-rig integration. The 17-profile source contains twelve previously approved profiles and five explicitly unapproved profiles: EXP-158, EXP-181, EXP-102, EXP-116 and EXP-050. Approval of one later does not approve the others or the shared runtime extensions. The older EXP-003 backup remains separately unapproved and is not in this source. The approved runtime and every prior backup outside this folder are unchanged.

## Recover and verify

Obtain this entire folder from a normal clone or archive. Keep its layout intact in a writable local directory. Run `python verify_backup.py`, then `python source/tools/verify_frustrated_pout_scope.py`. No original workspace, private link, new binary upload or LFS transfer is required. The first checks exact file inventory, sizes, SHA-256, Git blob identities, source/plan/gate bindings and approval boundaries. The second checks the source freeze, the append-only registry change, exact predecessor/runtime/art bytes and accepted anchor values.

`source/` contains exactly 617 files: 616 indexed files and their self-excluded freeze, including 182 PNGs. It is byte-identical to the reviewed capture source, without a delivery overlay. `BACKUP_MANIFEST.json` is the backup inventory. Earlier READMEs, releases, manifests, test counts and status sidecars remain unchanged historical provenance. In particular, the frozen EXP-050 status retains pre-capture wording; the outer `VALIDATION_SUMMARY.json` and unchanged actual-review record state the later technical PASS.

## Reproduce locally

Keep the backup pristine and make a working copy. Use Godot 4.6.3 and the packages in `source/requirements.txt` locally. Import `source/project.godot`, open the existing expression viewer, select Frustrated pout and play. Godot creates caches only in the working copy. Do not copy this registry into the approved runtime without user approval.

Run Godot `--headless --path source --script res://tests/test_frustrated_pout_runtime.gd` for the current runtime test. Use `--headless --path source --script res://tools/review_frustrated_pout_trajectory.gd -- --validate-only --plan=<absolute capture_plan.json path> --output=<new absolute output directory>` for deterministic preflight. To reproduce renderer samples locally, remove `--headless` and `--validate-only`, reserve the local display exclusively and add `--coordinator-display-lease-granted` after `--`. Do not run concurrent graphical captures. Keep outputs outside this backup. The helper produces 541 full/native checkpoint pairs; original raw frames and movies are deliberately excluded.

## Gate records and limits

`original_reference/INDEX.json` pins the nine original panels and sheet to commit `7693d1b8718c3bb1c717bd586fb472a7efc42403`; all ten files reuse exact existing Git blobs. The 4.13-second performance is newly authored from these still panels, not recovered source animation. Accepted combined anchors and duplicate holds gather to the compact sealed peak, sustain, broaden without smiling, then return to exact neutral at 3.91 seconds through the final 0.22-second hold.

Independent actual-performance review passed the bounded trajectory: 541 states, 1,082 actual images, all 219 unique native mouth images, static-anchor matches, lifecycle/handover coverage and exact neutral returns. This backup does not claim a new render of every prior profile or normal-speed playback. It retains the smoother/rounder mouth arch, weaker localized brow knit and lower-intensity peak relative to the painting. The historical component-only whole-face HOLD was superseded by combined static evidence; that does not erase these interpretation limits.

`gate_records/` contains unchanged concise reports, review freezes and small receipts. `gate_records/INDEX.json` identifies their provenance. The freezes intentionally name omitted external/raw evidence and are historical audit records, not manifests claiming that all original capture artifacts are packaged here. The current backup manifest specifies the complete recovery payload. This backup worker verifies source and recovery identity, not a new visual acceptance.

Technical PASS and backup publication do not grant user approval. Media delivery and archive review are separate. No normal-speed live/encoded playback, live AI/TTS, real socket test, CI, paid resource, hardware flashing or remote-machine execution is claimed. Raw capture dumps, diagnostic images, video, ZIPs and generated caches are excluded.
