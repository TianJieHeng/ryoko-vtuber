# EXP-063 Stunned silence: independent review

**Disposition: ready for USER review as a bounded, unapproved candidate.** This is not expression approval, production integration approval, or source-perfect certification.

## Visual findings

- Inspected the original nine-panel source sheet, all five static full/detail poses, native motion detail frames 12, 18, 24, 30, 45, 60, 72, 78, 90, 105, 113 and 120, and the decoded MP4 peak frame. The small parted mouth, fixed stare, frozen hold and neutral recovery form a coherent restrained reaction.
- The main fidelity limitation is substantial: the source peak has rounder, much wider eyes and a more rounded mouth opening. The candidate retains the runtime's angular eye silhouette and flatter mouth. It reads as mild silent surprise rather than the source's stronger stunned expression, especially at full-bust scale. Opening is already at the existing 4-pixel limit; this is deliberately an approximation, not an unexercised control.
- No new conspicuous detached facial layer, body displacement, or neutral-return residue was seen in the inspected frames. Tiny lash/hair edge fragments near the screen-left eye are already present in the neutral render and persist through the candidate. They should not be mistaken for a new EXP-063 regression, but remain visible at detail scale.
- The four-second timing is a new interpretation of static panels, with a 1.0–2.4-second frozen hold. It is not recovered source animation or the catalogue's 1.9-second proposed schedule.

## Validation checked

- Reviewed the capture/test scripts and result files: isolated state and native static gates each report **34 checks, PASS**. Native motion reports **872 checks, PASS**, covering 121 samples, scope, excluded controls, fixed transforms, neutral restoration, and sampled restart/release/reset behavior. These are reported execution results, not an independent rerun of Godot.
- Independently compared every native PNG: 121 full and 121 detail frames; initial frames 0–9 match; hold frames 30–72 are identical; frames 113–120 match frame 0 exactly in both views. Static neutral and neutral-return images also match exactly.
- Across all full-frame images, every changed pixel lies inside inclusive rectangle **x=215–344, y=285–393**. Every pixel outside this facial region is unchanged, including head silhouette, hair, earrings, neck, clothing and body. There are 62 distinct raster frames in each view; duplicates include the intentional holds.
- All recorded nonzero controls are the seven intended eye-opening, eyebrow and mouth channels. No unintended gaze, smile, spread, blush, blink, hair or body action appears. The on-disk registry has 24 entries and does not contain EXP-063; the capture injects the candidate into memory only.
- Independently probed and fully decoded `Stunned_Silence_review_v1.mp4` without errors: **H.264, 968×800, yuv420p, 30 fps, 121 frames, 165,588 bytes**. Duration is **4.033333 seconds**, including the final endpoint sample for the 4.0-second profile. The inspected encoded peak preserves the full/detail layout and review-candidate label.

## Limits

Native evidence is Godot 4.6.3 on X11/Mesa llvmpipe. This review did not observe normal-speed playback or measure interactive real-time pacing, test another renderer, run full production regression, or validate an exported build. The native log retains a runtime-image-loading export warning for existing `uneasy_clear_parting.png`; successful local capture does not resolve that export limitation. Lossless neutral/body equality applies to the PNG captures, not to compressed MP4 pixels.

No blocker was found to showing this explicitly limited candidate to the user. Whether its restrained expression is sufficiently “stunned” remains the user's visual judgment.
