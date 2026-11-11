# Full-body live facial-expression evidence

This harness loads `full_body/full_body_rig.tscn` in Godot 4.6.3, calls the original approved expression controller through `rig.play_expression(id)`, and samples the attached live head and full-body scene. It does not substitute the former neutral head composite and does not implement its own expression/timeline mathematics.

## What the video is

The full-body view and enlarged face view show the **same rig state and sample time**. The larger face is rendered again at a closer camera, rather than enlarging a low-resolution neutral image. All 47 original trajectories are sampled at 15 fps. Each retains its authored duration, with one sampled neutral endpoint and fractional-frame rounding per expression. The total authored time is 186.85 seconds; the combined file is 190.2667 seconds. No trajectory is sped up.

This is a **Godot scene-state + original-shader reconstruction**, not a native Godot screen capture. Its label is embedded in every video frame.

- Godot supplies the actual global transforms, visible draw owners, colors, Sprite2D/Polygon2D/MeshInstance2D geometry, shader parameters and texture pixels.
- The already installed Mesa EGL software renderer executes the original shader bodies in a thin GLSL canvas wrapper. All 10 sampled shader bodies are byte-identical to their current repository sources, recorded in `capture_source_manifest.json`.
- No X server, listening socket, browser, downloaded renderer, new artwork, or external rendering service is used.
- Dense opening meshes are sampled from Godot and stored as compressed binary arrays. Deferred frees are drained between samples with automatic expression and physics processing disabled.
- Static and dynamic draw states and texture assets are deduplicated. Raw sampled data stays local and is excluded from Git.

## Completed checks

- 47/47 expressions produced a visible facial pixel change, ranging from 259 to 4,522 changed pixels in the fixed face ROI. Labels and body pixels are excluded.
- 47/47 returned to a byte-identical neutral face and full canvas, with all final pose values exactly zero.
- All 2,854 video frames decoded without FFmpeg errors. H.264, 1280 × 960, 15 fps, 190.266667 seconds, 4,934,405 bytes.
- The all-47 contact sheet was visually inspected: non-neutral eyes, brows, gaze, mouth and blush changes are present across the catalogue, with no substituted neutral faces or blank/missing heads.
- `all47_summary.json`, `all47_face_pixel_evidence.csv` and the movie's matching JSON contain the compact results.

## Reproduce

From the repository root, using the installed Godot 4.6.3, Python, NumPy, Pillow, Mesa EGL/OpenGL and FFmpeg:

```sh
XDG_CACHE_HOME=/tmp/ryoko-godot/cache \
XDG_DATA_HOME=/tmp/ryoko-godot/data \
godot --headless --path ryoko_object_rig \
  --script res://full_body/face_review/sample_live_faces.gd -- \
  --expression=all --fps=15 \
  --output=res://full_body/face_review/all47_samples

python ryoko_object_rig/full_body/face_review/render_live_faces.py \
  --samples ryoko_object_rig/full_body/face_review/all47_samples \
  --output ryoko_object_rig/full_body/face_review/all47_full_body_live_faces_15fps.mp4
```

For a quick single-expression reproduction, use `--expression=EXP-002` and a different sample/output folder. A still can be generated with the renderer's `--still FRAME_INDEX --output path.png` option.

## Evidence and limitations

- The renderer writes one compact report alongside its video. Its per-profile checks compare **actual face pixels**, excluding labels and body, to that expression's first neutral frame. They record the largest changed-pixel count and whether the final face and pose return to exact neutral.
- Prior native Godot video frames of EXP-061 at neutral and 1.4 seconds were compared to this attached head at the same source-pixel camera. The face and opening-mouth geometry were visually coherent. Numeric comparisons against that lossy video are supporting evidence, **not a native GPU parity pass**. Full-detail differences also include changed full-body neck/background geometry, so those are not isolated facial error measurements.
- Native current-Godot rendering, real-time performance, 30/60 fps display pacing and live UI playback remain unverified here. The installed Godot headless backend renders dummy output and no authorized native display was available.
- This harness does not change approved art, expression profiles, control math, or body registration. It is review evidence, not a replacement production renderer.
- `live_affection_full_body.mp4` and its matching JSON are the earlier frozen short proof. They have not been overwritten by the larger-close-up all-47 run.
