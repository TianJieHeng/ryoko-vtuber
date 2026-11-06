# Approved EXP-005 release validation

Date: 2026-11-06. Repository baseline: `c37baf986de6dda1070a768f5d2f4c4df4306130`.

## Approval and scope

The user approved the actual two-cycle EXP-005 hearty-laughter video. This clean release includes only its performance profile, supporting runtime integration, isolated oral derivatives/generator, tests, review harness, and documentation. All 93 static registrations, all 594 original artwork PNGs, all 631 inherited PNGs overall, and baseline EXP-064/EXP-189 gaze assets are byte-identical. Unapproved performances, new gaze candidates, and experimental morph code/assets are excluded.

The production mouth shader, extracted feature pixels, harmonic underpaint, oral-feature mipmaps, and authored EXP-005 profile values are unchanged from the approved render. Unused morph integration was removed. Public live/clip validators use the actual performance registry and reject unsupported registered static IDs before ownership changes. Plain static keyboard cycling still covers all 93 faces; Shift cycling and Enter use supported performances.

## Fresh clean-release regression

All **29 Godot suites passed**, with **206,720 explicitly counted checks**, zero reported test errors/failures. The inherited bounce suite also passes but does not emit a numeric count. This is a new run of the final clean release, not the earlier prototype aggregate.

- 27 inherited suites: 205,497 counted checks.
- `test_hearty_laughter.gd`: 500 checks.
- `test_release_performance_controls.gd`: 723 checks, including every static ID, supported/unsupported live and clip validation, repeated invalid-request ownership preservation, real loopback UDP, static cycling, Shift cycling, Enter fallback/replay, and empty-registry behavior.

Each suite used a separate writable HOME/XDG directory. Machine-readable summaries: [regression.json](validation/exp005/regression.json).

## Exact render equivalence

The clean release rendered two complete cycles in actual Godot 4.6.3 OpenGL, then used FFmpeg with the same encoding settings. The regenerated MP4 is **byte-identical** to the user-approved MP4:

- 568 × 760, 30 fps, 436 frames, 14.533333 seconds.
- MP4 SHA-256: `dded6e1698ce749b664cbf2744ad3834a6aed12a59db56d2ef59a56ee984ff4d`.
- All 436 decoded original movie-writer frames match the approved source movie.
- Canonical EXP-005 profile SHA-256: `2fd32cf71d260fc7aa17b1fcaca503ec253c3cd0d302d91311117abbc8667cdd` (sorted-key compact JSON of the profile object).

See [render equivalence](validation/exp005/render_equivalence.json) and [frame hashes](validation/exp005/approved_video_frames.md5). The video was already delivered for approval; the repository records its exact provenance rather than embedding another copy.

## Fresh oral-pixel gate

The production shader/compositor was rendered at native 1136 × 1384 source resolution with body/eye motion frozen. All **182** rest, sweep, and 30-fps authored oral-timeline PNGs are byte-identical to the approved final-mipmap capture set. The timeline contains **161 distinct oral frames**.

Every capture preserves all pixels outside oral ROI [492,578,644,700], protected nose [530,540,606,586], and protected jaw/chin [430,700,710,755]. The undeformed full-open articulated rest is exact to the original-source legacy render. No authored-envelope or extreme-API pixel failures occurred. Capture input hashes were identical before and after recording. See [pixel gates](validation/exp005/pixel_qa.json), [render source hashes](validation/exp005/render_input_sha256.json), and [preservation](validation/exp005/preservation.json).

The Python generator was rerun independently in the clean project; all five source-derived/reference PNGs match the approved candidate byte-for-byte. It explicitly labels the 9,406 estimated RGB underpaint pixels and never changes original artwork. `EXP-005_feature.png.import` retains `mipmaps/generate=true`, and the shader uses `filter_linear_mipmap`.

## Limits and observed environment notices

The isolated mouth is a transformed 2D cutout, including its existing teeth/tongue. This is not new mouth anatomy or independent tongue articulation. Eyes/non-articulated layers follow opacity handovers, but the approved isolated-mouth shader assigns its own alpha: the mouth enters/exits at the visible boundary rather than opacity-crossfading. That exact approved behavior is deliberately preserved.

The assistant inspected rendered frames and pixel evidence but could not watch continuously at native 1× speed. User-hardware performance remains unmeasured. The user approved the exact rendered video despite that disclosed review limit.

The local graphics driver reported unsupported VSync changes and unavailable shader caching; the editor reported unavailable ObjectDB snapshot storage. Imports and actual captures completed, the fresh runtime suites passed, and exact comparisons succeeded. These environment notices are not counted as successful cache/profiler tests.

No CI, paid resource, hardware flashing, or remote-machine execution was used. Publication uses `[skip ci]`; the baseline repository has no workflow directory. No broader expression-performance batch is approved by this release.
