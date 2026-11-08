# Clean shared-expression review package

Eighteen approved performances share one rig. This integration adds EXP-158 Post-confession shyness, EXP-181 Cheeky wink, EXP-102 Knowing smirk, EXP-116 Confident denial, EXP-050 Frustrated pout and EXP-186 Smug cat smile to the twelve already approved profiles. The accepted cumulative runtime, all eighteen profile files, scenes and all 182 runtime PNGs are byte-identical to the completed reviewed source. No new fitting, artwork or motion is introduced.

Current checks: `python tools/verify_approved_integration.py` and `sha256sum -c APPROVED_SOURCE_FILES.sha256`. APPROVED_SOURCE_MANIFEST.json and APPROVED_INTEGRATION_STATUS.json describe the current 18-profile source. Original SOURCE_FILES.sha256, PUBLICATION_SOURCE_MANIFEST.json, CURRENT_SOURCE_MANIFEST.json, capture freezes, expression-local status files and original reports remain byte-exact historical contracts, not current aggregate guards. Their earlier approval or candidate wording describes the checkpoint when written; the current status file is authoritative. See APPROVED_INTEGRATION_VALIDATION.md for changes, test coverage and limits.

EXP-003 remains unapproved historical work, not user-rejected, and is not replayed or registered. Unfinished EXP-097 and all private dental, gaze and eye-opening experiments are excluded. Independent positive corners retain default zero and the shared 12-pixel cubic budget. Positive independent width requires mouth_open exactly zero. General open-plus-width is unsupported. The inherited full-open/full-spread/max-corner warm wedge is unchanged and is not claimed fixed. No CI, paid resources, hardware flashing or remote-machine execution is performed.

## Historical documentation and continuing API details

Twelve user-approved performances share one rig: EXP-163/005/001/006/107/007/002/152/160/177/164/021. EXP-021 Quiet sadness is the approved 3.65-second, five-key data-only performance, available through the existing API and quiet-sadness / quiet_sadness aliases. All eleven predecessor profiles, shared runtime, scenes, shaders and 182 PNGs remain byte-identical to main 2d46f72704ddf2a329b44a87cd24c66d5fe92568. Only EXP-021 profile status changes from its reviewed source; all other fields, times and control values are exact. EXP-003/139/170/153/161 and every other unregistered draft remain excluded.

Current publication checks: python tools/verify_quiet_sadness_publication.py and sha256sum -c SOURCE_FILES.sha256. PUBLICATION_SOURCE_MANIFEST.json is the current manifest. CURRENT_SOURCE_MANIFEST.json, tools/verify_quiet_sadness_package.py, QUIET_SADNESS_CAPTURE_FREEZE.json, historical_capture_metadata/ and inherited exact-scope receipts remain byte-exact historical contracts for their original source trees; do not run them as current publication guards. The historical backbone fixture also remains unchanged and is not a twelve-profile smoke test. Use tests/test_quiet_sadness_runtime.gd for the actual twelve-profile registry. See QUIET_SADNESS_PUBLICATION_VALIDATION.md for scope, evidence and limits.

## Historical EXP-164 publication documentation

Eleven user-approved performances share one rig: EXP-163/005/001/006/107/007/002/152/160/177/164. Fighting sleep adds the approved 3.47-second data-only performance. All ten predecessor profiles, shared runtime, shaders, scenes and 182 PNGs remain byte-identical to main 958eb944a37ce836fec5acf369f12b89f47b6656. Only the EXP-164 profile status text changes from its approved review; all other fields, times, phases and values remain exact. EXP-003/170/139, inner-cover experiments and all other unregistered drafts remain excluded. RELEASE.json and FIGHTING_SLEEP_PUBLICATION_VALIDATION.md record current status. Earlier explicitly marked checkpoints and frozen review receipts are historical provenance. No normal-speed playback observation, AI/TTS or real-socket validation is claimed.

Historical EXP-177 publication checkpoint:

Ten user-approved performances share one rig: EXP-163/005/001/006/107/007/002/152/160/177. Revised EXP-177 Meditative calm adds a single continuous 1.2-second closing arc, with unchanged hold/opening keys from 1.2 seconds onward. All nine prior profiles, gaze_down_extra, rigid outer-anchor brow controls, automatic-blink restoration, runtime and all 182 PNGs remain exact. EXP-003/164 and all other unregistered drafts remain excluded. See MEDITATIVE_PUBLICATION_VALIDATION.md for approval, source identities and verification. Earlier explicitly marked checkpoint descriptions below are historical provenance. The EXP-177 publication profile changes only its status text; every other reviewed field and motion value is exact.

Historical EXP-160 checkpoint: nine user-approved performances shared one rig: EXP-163/005/001/006/107/007/002/152/160. The published002/152 profiles, hidden-iris support and gaze_down_extra semantics are preserved. EXP-160 adds the approved default-zero rigid outer-anchor brow capability without new artwork. EXP-003/177/161/153 remain excluded. See SHY_MERGED_PUBLICATION_VALIDATION.md for merged scope and evidence; preceding frozen review stages are historical.

Historical EXP-152 checkpoint: eight user-approved performances shared one rig: EXP-163/005/001/006/107/007/002/152. EXP-002 is preserved from published commit 9b10e2f2c70f19fa003169502a73ee935af55480; EXP-152 includes the approved hidden-iris/down-gaze prerequisite. EXP-003/160/177 and new brow channels are excluded. See MERGED_PUBLICATION_VALIDATION.md for exact scope, source identities and focused merge checks. Earlier stage descriptions and frozen review receipts are historical.

The historical laughter runtime and artwork were frozen at local checkpoint d4a84324a30c0f0730c93dc49fc080b109f189aa. Later commits contain tests, provenance and review packaging. The complete 255-file corrected gaze baseline is preserved. Ordinary-lid correction F is integrated explicitly; see SOURCE_PROVENANCE.json and validation/smile_runtime_migration.json. Those historical review receipts retain their original wording. The exact approved laughter predecessor is now published at `6a61452e29ffbfcd4f7c5afe9b728b367f145f3e`; current scoped welcome validation is documented separately.

## Source versus generated evidence

Keep every packaged path, including the two gaze iris `.import` source configurations. They disable alpha-border RGB repair only for deliberately unmatted irises. Other import sidecars, `.godot`, caches, raw renders, movies, contact sheets, logs and scratch experiments are excluded.

The original canonical brows/eyes/hair intermediate trees and neutral diagnostic previews are reproducible outputs of tools/build_object_face.py. They are not playback inputs and are intentionally untracked. Regenerate them before historical identity checks. Source inputs and active runtime textures are included.

Laughter adds 31 PNG paths, representing 25 unique PNG byte sequences and 1,059,851 unique bytes. Six small source/runtime copies retain separate rebuild and runtime roles. Twenty-six inferred lip joints share two ordinary atlas files; every node retains its own transform, clipping and provenance record. Exact atlas-region checks protect packed pigment and masks. No diagnostic atlas, video or frame sequence is shipped.

SOURCE_FILES.sha256 inventories packaged paths only, excluding itself. It is regenerated after final metadata changes. Original baseline manifests remain historical evidence; they do not assert that all generated historical files are shipped or that rendered derived art is unchanged.

## Rebuild and verification

Run builders in an isolated copy. The current complete 22-suite runtime and source-check list is in PRIVATE_PRIDE_SCOPE_VALIDATION.md; the commands below retain the historical base/smile/bridge workflow. Real socket transport remains unrun under the current restrictions.

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

The 24-second actual-Godot review movie and its face crop are delivered separately, not in the repository. `source_references/laughter_predecessor_RELEASE.json` records their verified identities; `source_references/welcome_predecessor_RELEASE.json` preserves welcome evidence; `source_references/giggle_predecessor_RELEASE.json` preserves giggle evidence; `source_references/reassurance_predecessor_RELEASE.json` preserves reassurance evidence; `source_references/private_pride_predecessor_RELEASE.json` preserves the historical relief release; current `RELEASE.json` records the approved merged publication. SMILE_VALIDATION.md and validation/laughter_final_review.json distinguish completed checks, material inferred artwork, intentional ordinary-lid changes and finite raster limitations. No normal-speed audiovisual playback is claimed.

EXP-152, its capability prerequisite and the preserved EXP-002 source are user-approved for publication. The containing repository commit and external remote-verification receipt establish publication; a local commit or successful test alone does not. Frozen pre-publication receipts retain their historical wording. Existing unrelated repository paths must remain untouched when applying the overlay. No CI, paid service, external model/TTS connection, remote execution or Git LFS migration was performed. Any future genuinely large asset should follow the repository's authorized LFS workflow.

## Historical EXP-001 overlay

That historical package retained every approved laughter predecessor path and added only EXP-001 with its required lateral-mouth support. The 17 new PNGs preserve their exact reviewed source bytes. No wide-eye assets, held expression definitions, diagnostic frames or movies are included. `WELCOME_SCOPE_VALIDATION.md` records current scope and newly executed checks, including exact rendering against the approved welcome source.

## Historical EXP-006 overlay

Base: verified main `69e74ce5049a13ad5aa33014cacb1287f494787a`, repository subtree `ryoko_object_rig/`. All 357 predecessor paths remain present, and all 174 parent PNGs remain byte-exact. The two pressed-lip PNGs are explicitly inferred hidden continuation; six additional blush PNGs comprise two exact original FX sources, two fixed registered textures and two cheek masks. No source face-expression swap is used.

Run `python tools/verify_giggle_scope.py` and `python tools/verify_welcome_scope.py` on the clean package before generating diagnostics. Run the closed-smile and blush source verifiers and the runtime suites in `GIGGLE_SCOPE_VALIDATION.md`. The blush builder defaults to this shipping rig root and does not need sibling source trees. It regenerates optional diagnostic PNGs not included in the lean package. Run builders in an isolated copy, then retain the clean package for inventory checks.

The pre-review checkpoint is an expression-specific delta, not a replacement cumulative source archive. Its apply script first verifies every published base hash, applies exact changed/new files, and validates the reconstructed full candidate inventory.

## Historical EXP-107 overlay

Base is verified main `4f3deaa2de3eedb691a9f0c795c7b8563663e472`. All 399 published project paths remain; all 182 PNGs and four predecessor profiles are byte-exact. No new artwork is added. The only runtime capability is generic rigid lower oral-surface lift, and the only new playable data is EXP-107. Historical source guards follow exact pinned migration hashes through this extension, not unrestricted allowlists.

Run `python tools/verify_reassurance_scope.py`, `python tools/verify_giggle_scope.py`, `python tools/verify_welcome_scope.py`, then the fifteen runtime suites listed in `REASSURANCE_SCOPE_VALIDATION.md`. Do not run diagnostic builders in the clean inventory tree. The deliverable is a new scoped delta against this verified parent, never a replacement for the cumulative archive. Approval must precede any publication.

## Scoped EXP-007 overlay

Base is approved main `35a7ddc615e7501a9a814ca02d722ddb40f200c9`. All 418 parent paths remain. All 182 PNGs and five prior performances are byte-exact. EXP-007 plus one generic bounded mouth_purse capability add behavior; runtime and shader modifications are pinned to exact source hashes. Historical scope guards follow exact pinned migration hashes. The deliverable is a new reconstructable scoped delta, not a cumulative source replacement. Primary cumulative archive remains version 19. EXP-007 is user-approved for publication. A narrow live-documentation and release-metadata overlay updates approval wording and regenerates the source manifest/migration hashes without changing the approved runtime, artwork, profiles, tests or historical review receipts.

## Current narrow EXP-152 delta

Keep both original review freezes immutable. This publication merges the approved152 capability/profile onto published002, preserving every prior path. The original scoped delta still reconstructs its original478-file review candidate from8c349e; it is not silently rewritten. Media, logs and diagnostics remain external and the cumulative archive stays at version19.


## Preserved EXP-002 affectionate warmth

The approved EXP-002 profile, aliases, reference provenance and capture harnesses are retained. Its default gaze_down_extra is zero. The merged runtime uses the reviewed generic gaze capability and all eleven profiles use the same player. See AFFECTION_SCOPE_VALIDATION.md and MERGED_PUBLICATION_VALIDATION.md.

## Approved EXP-177 meditative calm publication

The user-approved revised EXP-177 (meditative-calm / meditate) is the tenth published performance, based on main 70655752bc82ba01b3fe8f64923360da60c578c9. Its single 1.2-second closing arc and all hold/opening motion match the approved review exactly. All nine prior profiles, runtime, artwork, iris/gaze, brow and automatic-blink behavior remain unchanged. RELEASE.json and MEDITATIVE_STATUS.json record current approval/publication. See MEDITATIVE_PUBLICATION_VALIDATION.md. The primary cumulative archive stays at version 19. No normal-speed playback observation, real-socket test or live AI/TTS connection is claimed.

## Approved EXP-164 Fighting sleep publication

The reviewed 3.47-second fifteen-key performance is the eleventh approved entry, using only existing ordinary lids, rigid brows and a restrained sealed purse. The six holds, source-pose relationships and disclosed timing tradeoffs are unchanged. See FIGHTING_SLEEP_PUBLICATION_VALIDATION.md. The current strict successor guard is tools/verify_fighting_sleep_scope.py; inherited exact-scope guards describe historical parent packages and are run only against their exact reconstructed parent. Primary cumulative archive version 19 and original review media/recovery remain untouched.
