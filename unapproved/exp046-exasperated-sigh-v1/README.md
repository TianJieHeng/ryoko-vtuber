# EXP-046 exact delivered preview: initial backup checkpoint

This review-only checkpoint backs up the exact delivered and subsequently user-approved Exasperated Sigh MP4 and profile, capture/encode receipts, source mapping, independent review, lineage and frozen source identity. Historical UNAPPROVED labels are retained. See APPROVAL_EVIDENCE.md for the later user approval and INDEPENDENT_REVIEW.md for the retained partial-fit qualifications.

MP4: Exasperated_sigh_rebuild_v1_UNAPPROVED.mp4, 229,933 bytes, SHA-256 ecceb235ec358e99302e78d8b065d0c2f6edf8cb4fdbe7e86a3a1abab0bd0e29.
Profile SHA-256: 1de491628e031953c765a47287d3ac230abb73e6adbdab15a3f8c11d1b41161e.

Source preparation dependencies are pinned to d6ce369f7b23b7364a301f7796fe9b26944db654 and approved39 baseline 419450d2302d471aa009557289ad509ffb413349. Unique attempt sources are in additional_sources.tar.xz. The reconstruction manifest records exact hashes for all retained inputs and captures.

The 310 captured PNGs are NOT included in this initial remote checkpoint. Their 25,828,792-byte lossless archive is uploading separately; the full local package has passed exact restoration, but that is not a claim all frame archive parts are remotely backed up yet. NATIVE_FRAME_BACKUP_STATUS.json distinguishes this phase. The full restorer needs those parts and cannot complete from this initial checkpoint alone. FULL_ARCHIVE_README.md documents the intended completed archive, not the current partial upload.

This checkpoint is sufficient to retain the exact approved MP4/profile and input/encode provenance while the separate capture archive finishes. No new native render, playback, perceptual-distinctness result, CI or main integration is claimed. The video remains a partial reference fit with bounded upward glance, rigid brow limitations and the independent review's visual concerns.
