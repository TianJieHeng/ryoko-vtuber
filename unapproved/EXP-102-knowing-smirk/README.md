# EXP-102 Knowing smirk: unapproved source backup

Completed local source and sampled actual rendered performance, preserved for recovery. User approval is pending. This folder is not an approved release and does not integrate the candidate or its independent-corner capability into the approved `ryoko_object_rig` project. The approved count remains twelve.

## Recover and verify

Obtain a normal clone or archive of the commit containing this folder. Copy this complete folder into a writable local directory, keeping `source/` and `original_reference/` together. No original workspace or private link is needed. All artwork and ten original references are ordinary existing Git blobs, not Git LFS transfers or new binary uploads.

Run `python verify_backup.py`, then `python source/tools/verify_knowing_smirk_scope.py`. The first checks the exact path set, sizes, SHA-256 hashes, Git blob identities and unapproved state. The second validates the frozen captured source and its inherited capability, approved profiles, authored timing, accepted static anchors and neutral endpoints. `BACKUP_MANIFEST.json` is the current backup inventory; inherited generic manifests are historical and were not falsely rewritten.

The source contains exactly 608 files and 182 unchanged runtime PNGs. It is byte-identical to the frozen captured source, with no delivery overlay. Pre-capture metadata overrides are documented and their original bytes archived within the source. All twelve prior profiles remain exact. This isolated registry adds only unapproved EXP-102, not EXP-158 or EXP-181.

## Editable local use and reproduction

Keep this verified backup untouched. Make a second working copy, use Godot 4.6.3 and the packages in `source/requirements.txt`, and open `source/project.godot`. Godot will create import caches in the working copy. Select Knowing smirk and press Play. Do not copy this candidate registry into the approved project without user approval.

The exact portable capture plan is `source/source_references/knowing_smirk_capture_plan.json`. For local-only deterministic reproduction after importing the working copy, use Godot with `--path source --script res://tools/review_knowing_smirk_trajectory.gd -- --validate-only --plan=<absolute path to that plan> --output=<new absolute output directory>` for the headless state rehearsal (add `--headless`). For actual renders, remove `--headless` and `--validate-only`, reserve the local display for this capture, and add `--coordinator-display-lease-granted` after `--` to acknowledge exclusive display use. Do not run concurrent graphical captures. Outputs go outside this backup. Then use `python source/tools/verify_knowing_smirk_scope.py --capture-root <output directory>` to verify the new actual receipts. Neither reproduction step is run remotely by this backup process.

`original_reference/INDEX.json` pins the original sheet and nine panels to repository commit `7693d1b8718c3bb1c717bd586fb472a7efc42403`. The natural performance is 3.80 seconds with ten keys, a slow sealed asymmetric smile and gentle ordinary lid/brow attention. The mouth finishes before the last brow attention; the final 0.20 seconds are exactly neutral. Authored timing is not recovered source animation.

## Review scope and limits

`VALIDATION_SUMMARY.json` records completed-source evidence hashes, independent runtime checks and all 319 actual checkpoints / 638 PNG receipts. Both full natural cycles, six accepted static anchors and expected recoveries were independently verified pixel-exact. Sampled actual renders were visually cleared. Normal-speed playback observation, live AI/TTS and socket integration are not claimed. The existing extreme opening/spread/corner skin wedge is documented and avoided by the sealed EXP-102 timeline, not repaired.

Movies, preview/diagnostic images, raw frames, recovery ZIPs, caches and private conversation material are excluded. Final encoded media and recovery-archive review are separate. No new artwork or runtime change beyond the previously reviewed shared independent-corner capability was introduced. No CI, paid resources or remote-machine execution was used.
