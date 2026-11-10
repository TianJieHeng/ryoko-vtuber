# EXP-061 Broad Surprise: approved preview backup

**Current approval: USER_APPROVED.** The user approved the delivered preview with “looks good”, under the clarification “if i say its good its approved”. APPROVAL_STATUS.json binds this approval to the exact profile and video hashes. Historical profiles, source and native reviews, playback receipts, and authoring notes retain their earlier UNAPPROVED/pending/no-publication wording unchanged. Those statements describe prior stages, not the current approval. This backup does not write main or register EXP061 in production. Production integration is a separate task.

The package is based on frozen approved36 commit `3ce98774282ad6c20dfbd7018d20838ff861b762`, not a moving branch head. All 999 pinned files, including 184 PNGs, remain unchanged. The registry remains the original 36 profiles with EXP061 absent.

## Reviewed evidence and qualifications

The approved MP4 is `Broad_surprise_review_v1.mp4`, SHA-256 `66fafc481ccc35fd19e6a5024cc94c7f95aa69a20a3a4f287868053f51584cf3`: H.264, 968 × 800, 30 fps, 121 frames, 4.033333 seconds including the final sampled endpoint. It preserves the native bust panel on the left and face detail on the right. The exact profile SHA-256 is `aa2200fc77caefb887d2e6115e062d5e2ca47c95cc56b56c5f536b926c57fbbf`.

Both independent reviews, final native and playback receipts, static and motion check records, all native motion PNG/RGBA hashes and decoded ordering evidence are included. Native static validation passed 870 checks; native motion passed 9,508 checks. The read-only independent validator passed all available stages. Its earlier missing-evidence report and the config-only failed report are preserved as chronology. Godot reordered only launcher project.godot whitespace/sections; exact frozen bytes were restored without changing values or weakening guards, followed by a complete PASS.

The raised whole brows and less-pinched mouth visibly differ from the inspected historical Shocked Gasp peak. Delighted Discovery has a clearer spread-smile conversion that this candidate does not use. These are not fresh full approved36 parity comparisons. Source fidelity remains partial: eyes stay relatively narrow, mouth anatomy is assembled from existing parts, and jaw/chin silhouette does not drop. Upper teeth and the existing mouth contour may give individual frames a mildly speaking or cheerful read. Zero smile control does not prove every viewer reads surprise.

Supported Kdenlive Play was invoked twice with sampled early progression and final neutral observed. This is not continuous normal-speed full-motion observation or complete pacing validation. Live-engine pacing, cross-expression interruption playback, speech/lip-sync, body gestures and export remain unvalidated. User approval does not remove these qualifications.

## Reproduce locally

Preserve this package as immutable historical evidence. Make a separate fresh reproduction copy. Use an existing local Git checkout of TianJieHeng/ryoko-vtuber containing `3ce98774282ad6c20dfbd7018d20838ff861b762` and run:

1. `python3 prepare_baseline.py /path/to/checkout`
2. `python3 prepare_native_launcher.py`
3. `sh run_state.sh`
4. Import the launcher headlessly, then run `godot --headless --path native_launcher --script native_launcher/NAME.gd --check-only` for NAME launcher, static and motion with the same local HOME/XDG variables used in run_state.sh.
5. `python3 refresh_review_freeze.py`

The bootstrap uses local Git archive at the pinned commit, disables Git network protocols/lazy fetch, exports only the rig and relevant reference assets, verifies 999 source files/184 PNGs, the source manifest, 36-profile registry, and sheet/catalogue hashes, then reconstructs BASELINE_FREEZE.json. It never uses a checkout's mutable working tree. Path relocation affects only the reproduction copy. The refresh script requires all non-path candidate/probe/state hashes to match, archives the historical input freeze, and records a new freeze of the relocated inputs before new capture. This is new reproduction evidence, not a redefinition of the approved artifact. Keep historical review reports separate from newly generated reports.

Requires Godot 4.6.3, Python with Pillow and NumPy, ffmpeg/ffprobe with libx264, and the DejaVu Sans font path used by the encoder. Numeric headless checks are not native visual validation. For a separately permitted native capture, first move the package's historical capture receipt directory, motion_checks.json, review_evidence and MP4 into an evidence archive. Then use the supported existing Godot desktop UI to open native_launcher/project.godot and Run Project with Game Embed Mode Disabled, reloading if required and restoring its prior setting afterward. The launcher refuses existing capture/motion output. Do not create a display server or use shell-native rendering/remote execution. Strict image dimensions remain 568 × 800 full and 400 × 360 detail. Once native receipts pass, run `python3 encode_preview.py`, `python3 review_validation.py` and inspect actual pixels/playback. Regenerated encodes may differ by platform; the supplied video hash identifies the exact approved review.

The authoring directory contains historical construction context, not portable entry points. Raw capture PNG sequences, contact sheets, duplicate baseline files and caches are omitted for size; hashes and exact MP4 are retained. The pinned commit contains the full reference art. No CI, paid resources, hardware flashing or remote execution is part of this backup.
