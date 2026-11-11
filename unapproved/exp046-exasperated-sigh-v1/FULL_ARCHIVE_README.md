# EXP-046 Exasperated Sigh: exact delivered native preview backup

This package preserves native editor attempt 02, the exact delivered MP4 and
profile, native captures and checks, lineage, frozen inputs, encode evidence,
reference mapping and independent review. The user subsequently approved this
preview; see `APPROVAL_EVIDENCE.md`. All original historical UNAPPROVED labels
are preserved rather than rewritten. Only this expression is backed up here.

## Identity and scope

- Exact profile SHA-256: `1de491628e031953c765a47287d3ac230abb73e6adbdab15a3f8c11d1b41161e`.
- Exact MP4 SHA-256: `ecceb235ec358e99302e78d8b065d0c2f6edf8cb4fdbe7e86a3a1abab0bd0e29`.
- MP4: 229,933 bytes; H.264, 968×800, 30 fps, 145 frames, 4.833333 seconds.
- Frozen source preparation: `d6ce369f7b23b7364a301f7796fe9b26944db654`, under
  `unapproved/rebuilt-expression-preparations-20261111`.
- Approved39 source baseline: `419450d2302d471aa009557289ad509ffb413349`.
- This review branch starts from main45 `17d2efdc7028fb3ec55cc604c19835ca2b7065f4`.
  No production registry, runtime, artwork, other expression or main ref is changed.

The historical editor capture reports PASS with 68,805 checks and no failures.
Original encoder receipt and the later independent decoded-frame inspection
are both preserved. This backup does not rerun Godot, rendering or encoding,
and does not use CI or execute code on another machine.

## Qualifications retained

The performance is a partial reference fit: a bounded upward glance, not the
reference's full eye roll; rigid brow strips do not reproduce the inner hooks.
The independent review records possible sleepy-speech/faint-grin ambiguity,
detail-scale lash/hair intersections and small lip-edge irregularities.
Native and encoded motion were inspected in sampled chronological frames,
not normal-speed continuous playback. Perceptual distinctness from comparable
expressions has not been established. User approval is a choice to accept this
preview, not new evidence that these technical or artistic checks passed.

Attempt 02 transparently freezes the Godot-import-normalized project configuration.
Its sections/keys/values match the original; other baseline source/art remains
unchanged. Attempt 01 history and the original preparation guards are retained.
The original lost local freeze is not claimed to have been recovered.

## Exact offline reconstruction

`RECONSTRUCTION_MANIFEST.json.gz` maps 1,788 retained files / 139,491,435 bytes.
It pins 1,159 existing dependency files rather than duplicating rig artwork.
It includes all 310 native PNGs (145 full, 145 detail, 20 static anchors), stored
as a byte-exact tar.xz archive split into 512-KiB parts for manageable uploads.
`additional_sources.tar.xz` stores unique attempt sources/metadata.
390 regenerable `.godot` cache and Python bytecode files are explicitly excluded;
these are not frozen authored inputs or delivered captures. No retained source,
reference art, captured PNG, receipt or delivered MP4 is converted or re-encoded.

From this package directory, with an existing local Git object database containing
the manifest's pinned commits and blobs:

    python -B restore_preview.py --git-dir /path/to/repo/.git --output /new/attempt
    python -B restore_preview.py --git-dir /path/to/repo/.git --output /new/attempt --verify-only

The restorer never fetches or runs candidate code. It refuses an existing output
unless checking it with `--verify-only`. It verifies pinned commit/path/blob
identities, archive parts, every restored size/SHA-256, and exact stored bytes.
See `RESTORATION_CHECK.json` for the actual local round-trip result.
