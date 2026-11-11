# New Ryoko expression reconstructions: unapproved source backup

These are **new 11 November 2026 candidates**, not restored versions of the lost
local freezes. This review-branch package backs up source preparation only.
**No new MP4 exists or is included. No native Godot parse, render, capture,
normal-speed review, independent source-fit review or user approval is claimed.**
The previous native-launch denial remains unresolved. Nothing here authorizes a
launch, removes a guard or integrates a candidate into the approved rig.

## Candidates

- [EXP-046 Exasperated Sigh](snapshots/EXP-046/README.md): 20 Python tests pass.
  This approximates an unsmiling exhale and only a subtle upward glance. The
  approved rig cannot reproduce the reference's full eye roll; partial-fit
  acceptance is still required after native visual review.
- [EXP-091 Overly Sweet Taste](snapshots/EXP-091/README.md): 34 Python tests pass.
  A generic bashful smile is a source-fit failure. The tiny sealed smile-pucker,
  strained brows, closed curved eyes and perceptual comparisons remain pending.
- [EXP-092 Sour Taste](snapshots/EXP-092/README.md): 35 Python tests pass.
  Purse contraction is a numerical prediction, not proof of distinctness from
  Headache or Overly Sweet Taste. Both native comparisons remain pending.

The exact original source maps, profiles, tests, numerical receipts, freeze
manifests, fail-closed gates and preparation reports are preserved. Large JSON
or checksum files use deterministic gzip storage, not lossy conversion.
Superseded Exasperated Sigh draft material is explicitly a historical checkpoint.
Read `BACKUP_SCOPE.json` for this package's scope and `packaging_checks/` for fresh
offline round-trip and Python-test results.

## Thin archive and pinned dependencies

- Approved39 baseline: `419450d2302d471aa009557289ad509ffb413349`.
- Existing EXP-096 review backup: `85a8bcd62a428087eb5702cb8cdee9d7594a072e`.
- Each candidate's 1,124-file rig, including 184 PNGs, is byte-identical to the
  pinned baseline. It is referenced rather than uploaded three more times.
- Existing reference artwork, comparator profiles and historical capture-source
  scaffolds are also pinned by commit, repository path, Git blob and SHA-256.
- `RECONSTRUCTION_MANIFEST.json.gz` maps all 4,745 files in the three candidate
  snapshots, Sour audit and relevant recovery sources/provenance to exact bytes.
  This includes 1,242 previously recovered dependency files. Any historical
  Headache video referenced by that recovery inventory is already at its old
  pinned commit; it is **not** a new preview or a video uploaded by this backup.
- The archive stores new source/receipts once and deduplicates identical data.
  The approved registry, production files, original candidate freezes and all
  existing branch histories are outside the intended change scope.

## Offline restoration and integrity check

Use an existing local Git object database containing both pinned commits and the
required blobs. `restore_sources.py` never fetches, signs in, changes Git refs or
runs candidate code. Missing objects fail instead of using an alternate route.
The output must be a **new, nonexistent** directory. It preserves the original
workspace-relative layout and verifies source size, SHA-256, pinned commit/path
and Git blob identity. It refuses to overwrite an existing destination.

    python -B restore_sources.py --git-dir /path/to/repository/.git --output /new/workspace
    python -B restore_sources.py --git-dir /path/to/repository/.git --output /new/workspace --verify-only

For a bare repository or read-only object cache, pass its directory directly.
The second command checks the exact existing bytes without modifying files.
This backup was actually restored into a separate scratch directory and all
4,745 files / 184,947,435 bytes matched. The three restored Python suites then
passed 20, 34 and 35 tests. These checks do not invoke Godot, FFmpeg or network
services. Some historical provenance contains original absolute paths; those
strings are preserved as evidence, not rewritten to pretend a new identity.

## Frozen reports and remaining work

Original candidate reports say publication was not attempted because that was
true when they were frozen. Their exact bytes remain unchanged. This enclosing
review-branch checkpoint is the later source-only backup, not a rewrite of those
reports or an approval of the expression source fit.

Native parsing/runtime tests, fresh native capture, independent reference and
perceptual review, valid MP4 encode/decode, normal-speed playback and user
approval remain pending. The guards are retained. No CI, remote-machine work,
main update or production integration is part of this checkpoint.
