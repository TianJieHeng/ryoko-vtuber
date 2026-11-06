# Approved performance preset validation

Date: 2026-11-06. Baseline: approved main `93b39bb03918be0f73aa73465ec196f34bbb32e4`.

Status: implemented and tested locally; actual runtime review approved by the user on 2026-11-06. No new expressions, artwork or full-body changes. No CI or paid resource used.

## Automated checks

All 27 Godot suites passed with zero reported failures, comprising 205,497 explicitly counted checks. The existing bounce suite also passed but does not print a numeric count. New performance-preset checks: 380. Inherited pose-store checks: 165. The full suite used separate writable HOME/XDG directories and completed in 113.46 seconds.

The focused suite covers strict slot and complete-snapshot validation, corrupt/oversized files, failed writes, deep-copy isolation, exact persisted snapshots, easing, pointer/attention release, complete effects restoration, both body-follow modes, existing expression/gaze behavior, live mouth/wink/gesture coexistence, active/paused clip takeover, invalid recall atomicity, explicit patch ordering, reset, legacy keyboard separation and real local UDP takeover/timeout. Existing UDP and clip persistence exclusions are tested.

Source comparison against the approved baseline found no missing files. All 631 inherited PNGs and all shaders are byte-identical. The only existing source files changed are `motion_rig.gd` and the documentation index `README.md`. All inherited motion drivers, registrations, demo clips and tests are unchanged.

## Render and runtime evidence

Godot 4.6.3 rendered the candidate using its OpenGL movie writer. FFmpeg encoded the result to H.264 MP4: 568 × 760, 30 fps, 781 frames, 26.033333 seconds. This is actual runtime footage, not composited still images.

The review performs a real disk round trip, recalls both saved configurations, combines existing mouth/wink/greeting controls, cancels a paused clip through recall, receives one real loopback UDP command, and retains both saved slots after the normal input timeout.

Three default runtime comparisons against the approved pendant project use neutral, gaze-supported EXP-064 and authored EXP-035, with body/head/gaze/effect controls and pendant dynamics active. All three images are pixel-identical. During the paused section, the original Godot movie-writer frames at 18.2 and 18.7 seconds have zero changed character pixels. The encoded MP4 contains minor compression differences in that comparison; the original AVI verifies exact pause stability.

Decoded chronological full-bust frames and enlarged face crops were inspected at save, reset, recall transitions, wink/mouth layering, pause, takeover and recovery. The inspected frames show registered facial features and coherent neck/collar/body motion; no new detached pieces or visible transition gaps were identified. The original expression swaps remain discrete; they are not interpolated or redrawn.

## Limits and next step

Native-speed playback is unavailable to the assistant. Frame inspection does not verify perceived naturalness at playback speed or real-time performance on the user's hardware. The synthetic normalized audio-level command demonstrates existing mouth control only, not microphone capture or phoneme detection.

These presets store configured targets, not transient animation or pointer-attention offsets. Existing live-input timeout behavior is intentionally unchanged, including timeout after a local recall while a UDP lease is still active. The user approved the reviewed MP4 before this checkpoint. Native-speed playback and user-hardware performance remain unverified.

Reproduction: run `godot --headless --path . --script res://test_performance_presets.gd` in this project, then all inherited `test_*.gd` suites. Review harness: `review_performance_presets.gd`, with Godot movie writer at fixed 30 fps and an isolated writable user-data directory. See `README_PERFORMANCE_PRESETS.md` for usage and lifecycle details.
