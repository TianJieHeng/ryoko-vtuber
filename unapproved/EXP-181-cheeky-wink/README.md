# EXP-181 Cheeky wink: unapproved backup

This is a completed local review candidate preserved for recovery. User approval is pending. This folder is not an approved release and is not integrated into the repository's approved `ryoko_object_rig` project. Backing it up does not approve it or increase the approved count.

## Recover and validate

Use a normal clone or archive of the commit containing this folder. Copy this complete expression folder to a writable local directory, keeping `source/`, `original_reference/` and `reproduction/` together. No vanished workspace, private link, Git LFS transfer or new binary download is required. All runtime artwork and the ten original references are existing ordinary Git blobs.

Run `python verify_backup.py` before opening the project. It checks the complete path set, byte counts, SHA-256 checksums, Git blob identities and unapproved state. Then run `python source/tools/verify_cheeky_wink_scope.py`. The latter validates both the frozen captured identity and the narrowly documented delivery overlay. `BACKUP_MANIFEST.json` records the exact current source inventory and pinned approved base. The inherited generic source manifests are historical predecessor records, not the current inventory.

For an editable local run, make a second copy, use Godot 4.6.3 and the dependencies in `source/requirements.txt`, and open `source/project.godot`. Keep the verified backup untouched because Godot creates import caches. Select Cheeky wink and press Play. The local source has the same twelve approved prior profiles plus the single unapproved EXP-181 candidate. It does not contain EXP-158, which has its own isolated backup. Do not copy this candidate registry into the approved project without approval.

The source is the reviewed 612-file delivery overlay, with all 601 exact captured files recoverable using archived originals. Runtime, artwork, controls, keyframes, timing and registry are unchanged from the actual capture. Read `source/DELIVERY_SCOPE.md`, `source/CHEEKY_WINK_STATUS.json`, `source/CHEEKY_WINK_DELIVERY_OVERLAY.json` and `VALIDATION_SUMMARY.json` for scope, tests and limitations. Historical release and publication documents inside the source describe their pinned predecessors and do not approve EXP-181.

`original_reference/INDEX.json` records the ten originals' pinned repository paths, commit and checksums. `reproduction/capture_plan.json` is the exact plan used by the included `source/tools/review_cheeky_wink_trajectory.gd`; generated performance frames are excluded. The source guard optionally accepts `--capture-root` when a separately preserved capture is available. Frame receipts and normal-speed playback are not part of this backup.

No movies, preview/diagnostic images, frame archives, caches, ZIPs or private conversation material are included. All 182 runtime PNGs are unchanged. No new art, face swaps or head warps were introduced. The inherited maximum-open/maximum-spread/maximum-corner-lift skin wedge is documented and avoided by EXP-181, not repaired. No normal-speed playback observation, live AI/TTS connection or real socket test is claimed. No CI or remote-machine execution was used.
