# EXP-177 focused closing refinement

Current publication checkpoint: the user approved the revised smoother-closing preview. See MEDITATIVE_PUBLICATION_VALIDATION.md and RELEASE.json. The following review-stage evidence and its then-current approval wording are retained as historical provenance.

The user asked: “its good make her lids close a little smoother please”. The revised preview subsequently received user approval and is published with the containing commit.

## Diagnosis and narrow change

The existing shared sampler eases every adjacent pair of keys independently with cubic smoothstep. The original closing keys at 0.4 and 0.85 seconds therefore each stop the lid velocity before it accelerates again. Dense actual v0 frame inspection and numerical derivatives confirm the two pauses and faster final descent. No integer snapping of the rigid upper-lash position was found; spatial clip masks and pigment remain unchanged.

Only the EXP-177 timeline is refined: remove those two intermediate closing keys and use the existing single smoothstep interval from closure 0 at time 0 to closure 1 at 1.2 seconds. Its start phase is labelled settling. Seven authored timeline keys still pass through nine source-comparison poses. The same .36 and .55 source poses now occur at .4866515881418201 and .6400595242051585 seconds rather than .4 and .85. This retiming is deliberate and is not represented as unchanged source timing or recovered motion.

Every key object from 1.2 seconds onward is unchanged from v0, including full closure through 2.35, the calibrated .64 first reopening at 2.85, .42 at 3.35 and neutral at 3.9. All non-blink coordinates remain zero. The renderer, shared player, registry behavior, prior nine profiles, anatomical layers, textures, UVs, scale, gaze/brows and automatic-blink restoration are byte-identical.

## Provenance and verification

Preserved v0: 538 files, inventory 27194683cd21c95c2bdbd6bc469c0d637872c8c40163af2014e44229e27bef6c; original profile SHA-256 581c3d34be7b99dc8dbf5df3d68b46e9014eed9fd60dae52d70ce38ea48afa6f. Its inventory and original profile are retained under source_references. Published parent remains main 70655752bc82ba01b3fe8f64923360da60c578c9. The original saved files and primary cumulative archive v19 are not overwritten locally.

The dedicated source guard enforces the exact correction scope and unchanged later keys. Runtime tests check the continuous closing curve, derivative bounds, source-pose crossings, exact hold/opening samples, neutral and interruption behavior. Fresh actual closing frames and complete revised movies must pass independent review before same-identity file replacements. Unaffected v0 evidence is reused only with explicit unchanged-input proofs; it is not labelled freshly rerun.

The tools provide still-frame inspection but no genuine temporally streamed playback observation. Dense frame sampling and decoded video frames are not normal-speed playback. The revised preview is user-approved and published with the containing commit. No normal-speed viewing, real-socket testing or AI/TTS connection is claimed.
