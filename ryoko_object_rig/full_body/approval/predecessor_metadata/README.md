# Current approved release: 47 performances

Overly Sweet Taste is integrated as one exact approved expression, with prior46 profiles, production runtime and 184 PNGs byte-exact. Source/Python-model/media checks pass; current engine/native integration checks were NOT RUN. Source-fit concerns remain. The user directed this single-expression publication without waiting for backup, which remains unverified. Counts become effective with the containing release commit. See [validation, qualifications and publication scope](ryoko_object_rig/APPROVED_OVERLY_SWEET_TASTE_INTEGRATION.md). Earlier release notes below are historical.

## Historical release notes

# Current approved release: 46 performances

Exasperated Sigh is integrated as one exact approved expression. All prior45 profiles, production runtime and 184 PNGs remain byte-exact. Current source/Python-model/media checks pass; current engine/native integration checks were NOT RUN. The bounded-glance and visual qualifications remain. See [current validation and limits](ryoko_object_rig/APPROVED_EXASPERATED_SIGH_INTEGRATION.md). Original review labels and earlier release notes below are historical.

## Historical release notes

# Current approved release: 45 performances

Puzzled, Mild Disgust, Sleepy, Irritated Side-eye, Triumphant Grin and Headache Tension are selectively integrated from their exact approved previews. Prior39 runtime, profiles and all 184 PNGs remain byte-exact. Current source/Python-model/media checks pass; current Godot/native integration checks were NOT RUN. See [current validation and limits](ryoko_object_rig/APPROVED_BATCH45_INTEGRATION.md). Original review labels and earlier notes below are historical, not current approval or validation status.

## Historical release notes

# Current approved release: 39 performances

Mental Arithmetic, Controlled Anger and Broad Surprise are integrated with unchanged prior36 profiles, runtime and artwork. Full native frame parity passed for all three. See [current validation and limits](ryoko_object_rig/APPROVED_BATCH39_INTEGRATION.md). Earlier progress notes retain historical scope.

# Current approved release: 36 performances

Nine more user-approved previews are integrated with the prior 27 standalone performances and artwork preserved, plus a bounded eye-transition repair. See [current validation](ryoko_object_rig/APPROVED_BATCH36_INTEGRATION.md). Earlier progress notes below retain historical scope.

# Current approved release

The shared rig now has 27 user-approved performances, including EXP-153 Hiding a Smile. See [current release and evidence limits](ryoko_object_rig/APPROVED_HIDING_SMILE_INTEGRATION.md). Earlier progress notes below retain historical scope.

# Current approved release

The shared rig now has 26 user-approved performances, including EXP-090 Queasy. See [current release and evidence limits](ryoko_object_rig/APPROVED_QUEASY_INTEGRATION.md). Earlier progress notes below retain historical scope.

# Current approved release

The shared rig now has 25 user-approved performances, including EXP-063 Stunned silence. See [current release and evidence limits](ryoko_object_rig/APPROVED_STUNNED_INTEGRATION.md). Earlier progress notes below retain historical scope.

# Current approved release

The shared rig now has 24 user-approved performances, including EXP-125 Sudden insight. See [current release and evidence limits](ryoko_object_rig/APPROVED_INSIGHT_INTEGRATION.md). Earlier progress notes below retain historical scope.

# Current approved release

The shared rig now has 23 user-approved performances, including EXP-040 Recovering composure. See [current release and evidence limits](ryoko_object_rig/APPROVED_COMPOSURE_INTEGRATION.md). Earlier progress notes below retain their historical scope.

# Ryoko — full-body 2D cutout VTuber

**Build a layered 2D character from the supplied artwork, then rig that artwork.** This repository is not a volumetric 3D character project. Previous 3D build instructions and implementation files have been removed from the current branch.

All retained assembly inputs are in [avatar_build_assets/](avatar_build_assets/). Read [the 2D assembly guide](avatar_build_assets/docs/ASSEMBLY_2D.md).

## What is retained
- 69 separated transparent character/effect PNGs and 18 useful source atlases.
- Six original character reference PNGs.
- 273 reference sheets: 200 facial expressions, 40 full-body gestures, 22 facial-control studies, seven character construction references and four detail sheets.
- 2,352 extracted reference panels and 200 peak copies, plus useful expression/gesture/crop catalogues.
- Five contact sheets showing the separated parts.

## Actual readiness
The shared [Godot 4.6.3 application](ryoko_object_rig/README.md) now contains one assembled separate-part character and one bounded, data-driven controller. **Six user-approved performances are authored: EXP-163 (Yawn)**, 13 beats over 5.8 seconds, **EXP-005 (Hearty laughter)**, 15 beats over 5.4 seconds, **EXP-001 (Bright welcome)**, nine keys over 3.0 seconds, **EXP-006 (Suppressed giggle)**, 13 keys over 2.8 seconds, **EXP-107 (Confident reassurance)**, 11 keys over 3.0 seconds, and **EXP-007 (Relieved smile)**, nine keys over 3.2 seconds. All use the same rig and [shared control API](ryoko_object_rig/CONTROL_API.md). See [scoped welcome validation](ryoko_object_rig/WELCOME_SCOPE_VALIDATION.md) for the preserved approved rendering and measured predecessor mouth-edge changes. See [laughter validation](ryoko_object_rig/SMILE_VALIDATION.md) for artwork provenance and review limits. See [scoped giggle validation](ryoko_object_rig/GIGGLE_SCOPE_VALIDATION.md) for the rigid closed-smile controls, separate original cheek FX, exact predecessor preservation and reference differences. See [scoped reassurance validation](ryoko_object_rig/REASSURANCE_SCOPE_VALIDATION.md) for the bounded rigid oral-lift control, unchanged artwork, predecessor parity and reference timing differences. See [scoped relief validation](ryoko_object_rig/RELIEF_SCOPE_VALIDATION.md) for the rounded rigid exhale, unchanged artwork and five-profile parity. All six performances are user-approved; frozen review receipts and descriptive profile metadata retain their pre-publication wording. Current approval status is recorded in [release metadata](ryoko_object_rig/RELEASE.json). Other catalogue entries remain acting references, not implemented performances.

Bounded separate-eye gaze and the near-closed lash transition are implemented and locally verified; see [gaze validation](ryoko_object_rig/GAZE_VALIDATION.md) and the [lash correction](ryoko_object_rig/LID_HANDOFF_CORRECTION.md). Additional performances, full-body motion and authored speech visemes/lip-sync remain unfinished. The head, neck and body stay fixed. The optional [local external-process bridge](ryoko_object_rig/LOCAL_CONTROL_BRIDGE.md) lets a separate process control the same rig over loopback; no AI model, Ryoko agent service or TTS provider is connected by this phase.

The runtime is a layered 2D Godot rig. Do not reconstruct a 3D body, retopologize it, bake fitted character UV atlases or target a VRM character export.

Do not replace this with a generic character. Preserve the human Ryoko design: sage/mint hair, amber eyes, dark trouser suit, white blouse, gold ornaments, green pendant and black pumps.

No CI. No paid services or API calls without approval. This cleanup is an ordinary recoverable Git commit; earlier work remains in history.
