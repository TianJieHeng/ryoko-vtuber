# Ryoko expression source recovery, 11 November 2026

This is a NEW recovery directory, not a restored November workspace or a recreation of any old frozen candidate identity.

## Recovered source bytes

- Repository: TianJieHeng/ryoko-vtuber.
- Pinned main: 419450d2302d471aa009557289ad509ffb413349. The remote main ref matched this commit when checked.
- `main/ryoko_object_rig/`: all 1,124 tracked files from that exact commit, including the approved 39-profile rig, its 184 PNGs, source assembly tools, tests and historical validation receipts.
- `main/avatar_build_assets/reference_library/`: the full expression catalogue, asset index and frame-extraction catalogue, plus the original sheets, nine panels and peak PNGs for EXP-046 Exasperated Sigh, EXP-091 Overly Sweet Taste and EXP-092 Sour Taste.
- `headache_review_backup/EXP-096-headache-tension/`: all 82 files in this package at 85a8bcd62a428087eb5702cb8cdee9d7594a072e. This is the exact approved review backup, not production integration. Its historical base is 3ce98774282ad6c20dfbd7018d20838ff861b762, which must not be conflated with current main.
- Total: 1,242 files and 57,369,306 bytes. Every file was checked against its pinned commit path, Git blob hash and byte length. SHA-256 inventories are in RECOVERY_MANIFEST.json and RECOVERED_FILES.sha256.

## Checks performed

- Approved39 source guard PASS. This checks current source bytes and historical validation receipts only. Its output mentioning native pairs is a check of stored records, not a new native render.
- All three source sheets match catalogue SHA-256 and 1159 x 1358 dimensions. All 27 panels match their recorded hashes. All three peaks are exact copies of panel 5. PNG structures decode.
- Exact approved Headache profile SHA-256: 21ba5c4393ed672a5496ed28577068bd4b56e3b8ff5d7ac4f9674df03badf1fe.
- Exact approved Headache MP4 SHA-256: 2b410146ed28ec4d6240e3e47c6b6f27d9c33b1a8087c101941da9a6a2d58716.
- Reference evidence: REFERENCE_RECOVERY_CHECKS.json. The target catalogue entries were extracted under metadata/ without editing the source catalogue.
- No Godot process, renderer, UI, CI or remote execution was launched. No remote refs or existing repositories were changed. Nothing was pushed.

## Remaining gaps and safe next step

- The former exasperated_sigh_work, overly_sweet_taste_v2_work and sour_taste_work directories were not found in the searched workspace, /workspace/shared or /tmp. Their local-only candidate profiles, revised authoring scripts, frozen input identities and raw captures are not recovered by this package.
- The new recovery has the exact baseline and reference inputs needed for fresh authoring, but it is not an implementation of those three performances. Their new profiles, checks and approval MP4s still need to be created and reviewed with fresh provenance.
- No reference pixels were visually reviewed during this integrity-only recovery. The author must inspect the recovered originals before authoring.
- Historical omitted Headache capture sequences are still omitted. The lossy approved MP4 cannot recreate their RGBA bytes. The review backup retains its original qualifications.
- Future work should COPY the pinned baseline into a distinctly named NEW candidate work directory. Do not modify this recovery baseline, reuse the old local frozen identities, repin old validation receipts, or claim earlier native tests were rerun.
- Native launch/rendering remains outside this recovery task and subject to the parent's outstanding access blocker.

## Transfer route

GitHub connector reads verified metadata and first materialized 70 small files. Its file-content endpoint returned empty content for files over 1 MB, and its generic fetch rejected oversized/binary content. A normal authorized read-only Git object transfer then fetched the two pinned commits and exact required blobs into a new isolated git_object_cache. No credentials were inspected and no restricted route was retried. This cache has no working checkout and is not a new user-visible repository or branch.
