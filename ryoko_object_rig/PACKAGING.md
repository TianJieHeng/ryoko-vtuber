# Clean shared-expression package

This directory contains the shared expression registry, controller and viewer,
the opt-in loopback control bridge and Python client, the EXP-163 approved-art
compatibility path, runtime assets, rebuild inputs and regression support. It does not add another authored expression.

All previously tracked object-rig paths are preserved. Existing unrelated
repository paths must remain untouched when applying this additive overlay.
The historical review_object_rig.gd is retained from the recorded main commit.

## Generated files and evidence

The three rig_assets/canonical_brows, canonical_eyes and canonical_hair trees
are reproducible builder output, not playback inputs. They are deliberately
untracked. The builder regenerates their intermediate masks and diagnostics
before the unchanged-art regression gates run. Assembled diagnostic previews,
comparison images, raw logs, superseded reports and ancillary capture scripts
are omitted. Runtime textures and every required source input remain included.

Review movies are separate artifacts, not stored in this source package.
RELEASE.json distinguishes the historical approved yawn movie from the current
local gaze review movie. Neither record claims a movie is a repository file.

SOURCE_FILES.sha256 covers the packaged files only, excluding itself. It is
not the old source archive inventory. There is no claim that all 310 historical
frozen entries or all generated baseline PNGs are tracked here. Historical
validation reports retain their original context; they do not establish a new
package validation or publication result.

## Clean local rebuild and checks

Use Godot 4.6.3 and the Python dependencies in requirements.txt. From this
directory, with no sibling project, run:

    python tools/build_object_face.py
    python tools/verify_object_base.py
    python tools/verify_yawn.py
    python tools/verify_teeth.py
    python tools/verify_gaze_assets.py
    python tools/verify_gaze_coverage.py
    python tools/verify_lid_handoff.py
    godot --headless --editor --path . --quit
    godot --headless --path . --script res://test_object_rig.gd
    godot --headless --path . --script res://test_yawn.gd
    godot --headless --path . --script res://test_teeth.gd
    godot --headless --path . --script res://test_expression_backbone.gd
    godot --headless --path . --script res://tests/test_gaze_runtime.gd
    godot --headless --path . --script res://tests/test_viewer_layout.gd
    python tools/test_control_bridge.py --output /tmp/ryoko-bridge-evidence
    sha256sum -c SOURCE_FILES.sha256

The generic backbone's BACKBONE_VALIDATION.md describes its parity and viewer
checks. LOCAL_CONTROL_BRIDGE.md and AI_CONTROL_VALIDATION.md describe the local
transport, its tests and remaining integration limits. Any rendered results belong outside the repository. The legacy yawn
capture command remains available as tools/capture_yawn.sh.

## Storage and publication boundary

This overlay contains no movies or multi-megabyte diagnostic sheets. Ordinary
small source PNGs and runtime assets remain normal Git objects. No Git LFS
migration or new LFS configuration is performed here. Existing repository
attributes are preserved; any future genuinely large asset should use the
repository's authorized LFS workflow rather than individual blob approvals.

This packaging operation is local. A manifest or successful local test is not
evidence of a remote commit, push, CI run, or user approval of new artwork.

## Bounded-gaze candidate import configuration

The two new runtime iris sidecars, `rig_assets/gaze_eyes/iris_screen_left.png.import` and `iris_screen_right.png.import`, are required source configuration. Keep them even if other generated `.import` files are omitted. They disable Godot alpha-border RGB repair only for the deliberately unmatted iris textures; mipmaps remain disabled. Do not substitute a global importer default or discard these files. A fresh import must reproduce the reviewed result. Other gaze mask sidecars are generated and are not shipped.

All original 103 PNGs are preserved and hashed in GAZE_SOURCE_ORIGINALS.json. New art, masks and provenance live in rig_assets/gaze_eyes. Generated movie frames, captures, caches and developer scratch files stay outside source. GAZE_VALIDATION.md records the current local candidate checks and the measured eye-edge changes. RELEASE.json identifies this enabled review candidate and keeps the prior approved yawn evidence explicitly historical. User approval and remote publication remain pending.

The focused near-closed lash correction is documented in LID_HANDOFF_CORRECTION.md. It changes only the ordinary eye shader at runtime and preserves all delivered artwork.
