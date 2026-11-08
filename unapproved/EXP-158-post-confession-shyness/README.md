# EXP-158 Post-confession shyness: unapproved backup

This is a completed local review candidate preserved for recovery. User approval is pending. This folder is not an approved release, and it is not integrated into the repository's approved `ryoko_object_rig` project. Backing it up does not approve it.

## Recover

Use a normal clone or an archive of the commit containing this folder. Copy this complete expression folder to a writable local directory, keeping `source/` and `original_reference/` together. No vanished workspace, sibling checkout, private link, Git LFS transfer, or new binary download is required. All runtime artwork and original references are ordinary Git blobs in this repository.

Run `python verify_backup.py` before opening the project. It checks every path, byte count, SHA-256 and Git blob hash, as well as the unapproved state. `BACKUP_MANIFEST.json` gives the exact source inventory and pinned approved base. `source/POST_CONFESSION_SHYNESS_FILES.sha256` and `source/tools/verify_post_confession_shyness_package.py` provide current source-level checks. The inherited `SOURCE_FILES.sha256` is a historical predecessor manifest, not the current EXP-158 inventory.

Read `source/POST_CONFESSION_SHYNESS_SCOPE.md`, `source/POST_CONFESSION_SHYNESS_STATUS.json`, and `VALIDATION_SUMMARY.json` for completed tests and limitations. Historical release and publication documents inside `source/` describe their pinned predecessor versions; they do not approve EXP-158.

For a local editable run, copy this whole folder again, use Godot 4.6.3 and the dependencies in `source/requirements.txt`, then open `source/project.godot`. Keep the verified backup untouched because Godot creates import caches. The source contains all 12 approved predecessor profiles plus the single unapproved EXP-158 candidate for isolated review only. Do not copy this candidate registry into the approved project without approval.

The ten original reference images are exact existing repository blobs. `original_reference/INDEX.json` records their pinned repository paths, original commit and checksums. Preview movies, contact sheets, diagnostic renders, caches, large logs and recovery ZIPs are intentionally excluded; they are not needed to edit or recover this source. No normal-speed playback observation, live AI/TTS connection or real socket test is claimed. No CI or remote-machine execution was used.
