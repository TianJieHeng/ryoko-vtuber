# Clean shared-expression review package

This is the same assembled character, shared registry, controller, viewer and opt-in loopback bridge. It contains two authored performances: EXP-163 yawn and the new EXP-005 hearty-laughter review candidate. The other 91 historical catalogue IDs remain references. No new expression-specific application or controller is introduced.

Runtime and artwork were frozen at local checkpoint d4a84324a30c0f0730c93dc49fc080b109f189aa. Later commits contain tests, provenance and review packaging. The complete 255-file corrected gaze baseline is preserved. Ordinary-lid correction F is integrated explicitly; see SOURCE_PROVENANCE.json and validation/smile_runtime_migration.json. Neither laughter nor the gaze/ordinary-lid candidates are described as user-approved or published.

## Source versus generated evidence

Keep every packaged path, including the two gaze iris `.import` source configurations. They disable alpha-border RGB repair only for deliberately unmatted irises. Other import sidecars, `.godot`, caches, raw renders, movies, contact sheets, logs and scratch experiments are excluded.

The original canonical brows/eyes/hair intermediate trees and neutral diagnostic previews are reproducible outputs of tools/build_object_face.py. They are not playback inputs and are intentionally untracked. Regenerate them before historical identity checks. Source inputs and active runtime textures are included.

Laughter adds 31 PNG paths, representing 25 unique PNG byte sequences and 1,059,851 unique bytes. Six small source/runtime copies retain separate rebuild and runtime roles. Twenty-six inferred lip joints share two ordinary atlas files; every node retains its own transform, clipping and provenance record. Exact atlas-region checks protect packed pigment and masks. No diagnostic atlas, video or frame sequence is shipped.

SOURCE_FILES.sha256 inventories packaged paths only, excluding itself. It is regenerated after final metadata changes. Original baseline manifests remain historical evidence; they do not assert that all generated historical files are shipped or that rendered derived art is unchanged.

## Rebuild and verification

Use Godot 4.6.3 and requirements.txt. Run from this directory, with no sibling source tree required:

    python tools/build_object_face.py
    python tools/verify_object_base.py
    python tools/verify_yawn.py
    python tools/verify_teeth.py
    python tools/verify_gaze_assets.py
    python tools/verify_gaze_coverage.py
    python tools/verify_lid_handoff.py
    python tools/verify_smile_support.py
    godot --headless --editor --path . --quit
    godot --headless --path . --script res://test_object_rig.gd
    godot --headless --path . --script res://test_yawn.gd
    godot --headless --path . --script res://test_teeth.gd
    godot --headless --path . --script res://test_expression_backbone.gd
    godot --headless --path . --script res://tests/test_gaze_runtime.gd
    godot --headless --path . --script res://tests/test_viewer_layout.gd
    godot --headless --path . --script res://tests/test_laughter_runtime.gd
    godot --headless --path . --script res://tests/test_smile_controls.gd
    python tools/test_control_bridge.py --output /tmp/ryoko-bridge-evidence
    sha256sum -c SOURCE_FILES.sha256

Godot needs writable HOME and XDG cache/data/config locations in a sandbox. The smile verifier performs two deterministic rebuilds and checks original images, protected mouth functions and packed-owner provenance. Existing Python yawn/base reports describe their historical component scope; the combined registry and lifecycle are checked by the shared-controller and laughter suites.

## Review artifacts and publication boundary

The 24-second actual-Godot review movie and its face crop are delivered separately, not in the repository. RELEASE.json records their verified identities. SMILE_VALIDATION.md and validation/laughter_final_review.json distinguish completed checks, material inferred artwork, intentional ordinary-lid changes and finite raster limitations. No normal-speed audiovisual playback is claimed.

This package is local. A local commit, successful test or source archive is not evidence of remote publication or user approval. Existing unrelated repository paths must remain untouched when applying the overlay. No CI, paid service, external model/TTS connection, remote execution or Git LFS migration was performed. Any future genuinely large asset should follow the repository's authorized LFS workflow.
