# Runtime rig publication validation

Validated locally on 2026-11-05 with Godot 4.6.3. No CI was run or added.

- Source: phase31 at c752edde815eaab559d06cf43b7ae0784bf79e1c.
- All 594 artwork files match blobs already present in phase31; no artwork or registration changes.
- Facial controls: 89 checks passed.
- Expression controls: 58,504 checks passed.
- Headless playback smoke test: 93 profiles loaded, all eight highlights completed without errors.
- Existing captured-video validation covered all 93 expressions in three batches. Videos are not included in this source checkpoint.
- Packaging fix: playback transition logs use user:// rather than requiring an adjacent output directory.

This is the discrete layered facial/bust runtime, not a mesh-deformation or full-body rig. No experimental overlays are included.
