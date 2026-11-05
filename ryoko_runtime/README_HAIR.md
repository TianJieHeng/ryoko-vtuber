# Crown/bun secondary motion

The later approved lower side-lock revision is documented in [README_LOOSE_HAIR.md](README_LOOSE_HAIR.md). It is separate from this approved crown/bun control and was approved after visual review.

User-approved revision based on approved clip-player rig 80a5395. Adds actual weighted mesh movement to the crown and bun while preserving the approved face, torso and chest behavior.

The upper hair lags slightly behind changes in head/torso motion and settles when movement stops. It is not driven by an idle sine wave. A damped spring follows an upper-head anchor, with an eight-source-pixel limit (under four pixels at the normal review scale). The focused head-motion test peaks at 6.67 source pixels.

The deformation weight is full above source y120, feathers down to zero at y330, and remains zero below that. All registered eyes start at or below y350; facial features, neck, clothing and chest receive zero additional hair displacement. Hairpin pixels in this crown region move with the hair. This is a small continuous crown/bun deformation, not independent strands, loose side-lock physics or 3D hair simulation.

- F toggles crown motion.
- API: `hair_secondary: false` restores the exact prior rigid-head rendering in this region. Re-enable with true.
- R clears spring displacement; the enabled setting is retained.

Existing gestures, pose recall, clips and torso bounce naturally drive the hair through their head motion. Paused clips also freeze this motion, consistent with the rest of the rig.

`--hair-proof` records a 17-second runtime sequence: rest, left/right head movement with hair enabled, a held pose settling to rest, then rigid/off comparison. No artwork files are modified.

`test_hair_secondary.gd` adds 289 checks for zero weight at face/neck/body landmarks, feathering, idle stability, bounds, settling, opt-out, variable-frame stability, runtime wiring, shader opt-out and reset. All prior suites also pass.

Visually reviewed and approved by the user before publication.
