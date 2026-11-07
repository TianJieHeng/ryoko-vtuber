# Clean shared-expression review package

This is the same assembled character, shared registry, controller, viewer and opt-in loopback bridge. It contains four authored performances: EXP-163 yawn, EXP-005 hearty laughter, EXP-001 bright welcome and EXP-006 suppressed giggle. The other 89 historical catalogue IDs remain references. No new expression-specific application or controller is introduced.

The historical laughter runtime and artwork were frozen at local checkpoint d4a84324a30c0f0730c93dc49fc080b109f189aa. Later commits contain tests, provenance and review packaging. The complete 255-file corrected gaze baseline is preserved. Ordinary-lid correction F is integrated explicitly; see SOURCE_PROVENANCE.json and validation/smile_runtime_migration.json. Those historical review receipts retain their original wording. The exact approved laughter predecessor is now published at `6a61452e29ffbfcd4f7c5afe9b728b367f145f3e`; current scoped welcome validation is documented separately.

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

The 24-second actual-Godot review movie and its face crop are delivered separately, not in the repository. `source_references/laughter_predecessor_RELEASE.json` records their verified identities; `source_references/welcome_predecessor_RELEASE.json` preserves welcome evidence; current `RELEASE.json` records the scoped giggle source. SMILE_VALIDATION.md and validation/laughter_final_review.json distinguish completed checks, material inferred artwork, intentional ordinary-lid changes and finite raster limitations. No normal-speed audiovisual playback is claimed.

This package is local. A local commit, successful test or source archive is not evidence of remote publication or user approval. Existing unrelated repository paths must remain untouched when applying the overlay. No CI, paid service, external model/TTS connection, remote execution or Git LFS migration was performed. Any future genuinely large asset should follow the repository's authorized LFS workflow.

## Scoped EXP-001 overlay

The current package retains every approved laughter predecessor path and adds only EXP-001 with its required lateral-mouth support. The 17 new PNGs preserve their exact reviewed source bytes. No wide-eye assets, held expression definitions, diagnostic frames or movies are included. `WELCOME_SCOPE_VALIDATION.md` records current scope and newly executed checks, including exact rendering against the approved welcome source.

## Scoped EXP-006 overlay

Base: verified main `69e74ce5049a13ad5aa33014cacb1287f494787a`, repository subtree `ryoko_object_rig/`. All 357 predecessor paths remain present, and all 174 parent PNGs remain byte-exact. The two pressed-lip PNGs are explicitly inferred hidden continuation; six additional blush PNGs comprise two exact original FX sources, two fixed registered textures and two cheek masks. No source face-expression swap is used.

Run `python tools/verify_giggle_scope.py` and `python tools/verify_welcome_scope.py` on the clean package before generating diagnostics. Run the closed-smile and blush source verifiers and the runtime suites in `GIGGLE_SCOPE_VALIDATION.md`. The blush builder defaults to this shipping rig root and does not need sibling source trees. It regenerates optional diagnostic PNGs not included in the lean package. Run builders in an isolated copy, then retain the clean package for inventory checks.

The pre-review checkpoint is an expression-specific delta, not a replacement cumulative source archive. Its apply script first verifies every published base hash, applies exact changed/new files, and validates the reconstructed full candidate inventory.
