# Clean shared-expression package

This directory contains the shared expression registry, controller and viewer,
the EXP-163 approved-art compatibility path, runtime assets, rebuild inputs and
regression support. It does not add another authored expression.

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

Approved yawn and other review movies remain in the existing Space. They are
not stored in this Git package. RELEASE.json records the approved movie identity
without claiming that the movie is a repository file.

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
    godot --headless --editor --path . --quit
    godot --headless --path . --script res://test_object_rig.gd
    godot --headless --path . --script res://test_yawn.gd
    godot --headless --path . --script res://test_teeth.gd
    godot --headless --path . --script res://test_expression_backbone.gd
    sha256sum -c SOURCE_FILES.sha256

The generic backbone's BACKBONE_VALIDATION.md describes its parity and viewer
checks. Any rendered results belong outside the repository. The legacy yawn
capture command remains available as tools/capture_yawn.sh.

## Storage and publication boundary

This overlay contains no movies or multi-megabyte diagnostic sheets. Ordinary
small source PNGs and runtime assets remain normal Git objects. No Git LFS
migration or new LFS configuration is performed here. Existing repository
attributes are preserved; any future genuinely large asset should use the
repository's authorized LFS workflow rather than individual blob approvals.

This packaging operation is local. A manifest or successful local test is not
evidence of a remote commit, push, CI run, or user approval of new artwork.
