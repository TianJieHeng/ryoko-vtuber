# EXP-160 local source and performance contract

Nine user-approved performances share one rig: EXP-163/005/001/006/107/007/002/152/160. The published002/152 profiles, hidden-iris support and gaze_down_extra semantics are preserved. EXP-160 adds the approved default-zero rigid outer-anchor brow capability without new artwork. EXP-003/177/161/153 remain excluded. See SHY_MERGED_PUBLICATION_VALIDATION.md for merged scope and evidence; preceding frozen review stages are historical.

## Identity and source

Published parent: main 8c349e29fb1e742231918260d7db56026492a6c9. Immediate immutable capability parent: 462 files, inventory d3d32cea21da2973c711779f201676c8344b409fba966b48ab22832381fae49f. The capability uses separate rigid brows with an additional 26-degree outer-anchor rotation, default zero, preserving all old-domain behavior. EXP-160 uses 32 degrees total at the peak: legacy tilt -1/+1 and new lift 24/26 on each side, with no vertical raise.

Exact nine-panel reference: original catalogue commit 7693d1b8718c3bb1c717bd586fb472a7efc42403, EXP-160 Shy laughter v001. Original metadata SHA-256 ded1b313c36b66daf46f3426288ef4670b04703497323314754bba18e872b2bf. All eleven reference image hashes, including nine panels, peak and sheet, are retained in source_references/shy_laughter_source_manifest.json. References are not runtime textures. The target catalogue contains 93 IDs, not all 200 original entries.

## Authored acting, not recovered animation

The static panels show neutral, closed tender smile, modest opening and blush, ordinary narrowed eyes, tender inner-high brows and smiling crescents, a second similar laughing pose, sealed closed-eye afterglow, reopened-eye afterglow, and neutral. A tiny warm screen-right sliver in source panel 7 does not establish a requirement for perfect zero iris. The rigid source eyebrow silhouette cannot reproduce every curve in the separate low-resolution illustration.

The new proposal is 3.4 seconds and twelve keys: 0, .30, .50, .65, 1.00, 1.35, 1.60, 1.85, 2.20, 2.40, 2.80 and 3.40 seconds. Two small opening accents interpret the source's stated pulse intent; their timing and amplitudes are newly authored. The catalogue's 1.9-second time labels are unimplemented proposals, not recovered source motion.

Aperture closes on one 1.85-to-2.20-second smoothstep while mouth smile/spread/corner, pressure/oral lift, brows, crescents and blush remain held. The sealed pose then relaxes brow intensity before the eyes reopen. Pressure/oral lift at zero opening is not asserted to be visible. White upper enamel is allowed by this laughing reference. Static ablations and played sampling do not establish an anatomical enamel-flash defect. Shared 0.45-second interrupted release and 0.30-second retrigger remain unchanged; they are shortened generic transitions, not copies of the authored afterglow.

## Frozen implementation boundary

Only expressions/EXP-160.json and its registry entry add performance behavior. Core runtime, shaders, all 182 PNGs and six published profiles are byte-exact to the capability parent. No new expression controller, facial scale, UV/pigment editing, opacity emotion blend, flattened face replacement, head-motion acting or body/tracking route. Mouth physical multiplier remains 0.55, maximum 30.8 source pixels. AI/TTS and external socket setup are preparation only.

## Checks and evidence

Run the four root test_*.gd suites and all seventeen tests/test_*.gd suites under Godot 4.6.3 with writable HOME/XDG folders after clean import. The new test_shy_laughter_runtime.gd checks source order and held closure, bounded dense sampling, all prior-profile handoffs in both directions, release/repeated release/retrigger at many phases, exact neutral, manual/reset/disable ownership, restored auto-blink, malformed schema/atomic controls, repeated cycles, rigid owners, fixed UV and physical aperture. Existing tests change only their exact registry expectations and exclude EXP-160 from assertions specifically about old definitions' default-zero channels.

Run verify_shy_scope.py --clean. Run the eight predecessor validators with PYTHONDONTWRITEBYTECODE=1 to keep the clean tree free of Python caches: verify_welcome_scope.py, verify_giggle_scope.py, verify_reassurance_scope.py, verify_relief_scope.py, verify_autoblink_scope.py, verify_brow_inner_lift_scope.py, verify_closed_smile_support.py and verify_blush_source.py. Exact hash-pinned forwarding preserves every historical receipt; it does not replace assertions with broad exemptions. Verify SOURCE_FILES.sha256 and reconstruct the combined delta against the published parent.

Accompanying review evidence provides exact frozen inputs, commands, state/control trajectories, pixel hashes, first-fit 194-state preflight, final two-cycle full-bust/native captures, complete sampled destination trajectories after handoffs/retriggers, interrupted release origins, repeated release and auto-blink/manual/reset/disable cases. Distinguish fresh samples from reused capability parity evidence. Frame labels alone are not proof: harness assertions and recorded actual state must agree.

## Limits and approval

No normal-speed playback observation or real-socket test is claimed. Finite 30 Hz performance and focused lifecycle sampling cannot prove every possible artistic combination. Inherited blunt right inner-brow termination and darker terminal pigment remain. The optional generic release can briefly flatten warmth and enamel while returning to neutral; it is not source-afterglow-identical. Original low-resolution source illustration and high-resolution canonical rig remain distinct artworks.

This is local, unapproved work. Final outcomes belong to the accompanying audit, not a claim inferred from this checklist. No Git publication, user preview, Library replacement or primary archive change is authorized by passing tests.
