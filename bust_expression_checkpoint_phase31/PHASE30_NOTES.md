# Phase 30: local visual review candidate

- EXP-003 quiet contentment: relaxed brows, softly closed eyes and tiny serene smile, matching the catalog peak. Rest and blink intentionally share closed-eye art.
- EXP-043 silent fury: deeply inward brows, intense narrowed amber eyes and compressed lips. Dedicated closed blink.
- EXP-064 shocked gasp: raised worried brows, wide small-pupil eyes and upright open gasp. Dedicated closed blink.

Exact peak references were retrieved from TianJieHeng/ryoko-vtuber reference_library. Lewd expressions remain deferred. Source art was generated with the built-in image tool. The user authorized the existing Python crop/assembly pipeline for this batch.

All 87 previous registrations and 552 artwork PNGs are byte-for-byte preserved. Only generated facial tiles are registered on the unchanged fixed bust. Quiet-contentment source framing was corrected during extraction; its mouth mask excludes the nose. The gasp mouth was fitted inside existing mouth bounds without modifying the jaw. Final comparison boards were visually inspected for alignment, speech replacement and fully closed blinks. Static composites are not live graphical runtime captures.

Validation: Godot 4.6.3 headless import passed; 89 facial-control checks passed; 56,614 full 90-profile expression checks passed; 12 jaw/chin/neck/body pixel checks passed; prior-asset preservation passed. Initial test execution hit an unwritable default Godot data directory, resolved with per-run writable XDG directories under /tmp. An open-eye-only assertion was adapted for EXP-003's intentionally closed rest state and the suite passed again.

No upload, publication, CI, audio, continuous deformation, physics or transitions added. Awaiting user visual approval.


## User-requested correction, 2026-11-05

The user identified EXP-003 eyes sitting too far off the face and EXP-064 underlying eyes showing through the blink. Inspected both supplied screenshots. EXP-003 source was regenerated directly from the fixed approved neutral, eliminating the prior shifted/misaligned source. Removed the manual eye-strip translation. Both corrected profiles now use eye tiles extending to y555 rather than y531, covering the old lower-lash area completely. EXP-064 blink now cleanly occludes the underlying open-eye layer.

Reinspected rest, speaking A, blink, combined states for both corrected profiles. Verified full alpha=255 coverage over both old lower-lash core regions in rest and blink tiles. Reran headless import, 89 controls, 56,614 expression checks, all 12 jaw/body pixel checks and phase29 preservation checks: all pass. EXP-043 remains unchanged. No publication. Updated boards still await user approval.
