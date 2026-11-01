# Visual reference QA boundaries

- Accepted images have been reviewed as character design/performance references, not as implemented Blender geometry, UVs, blendshapes, animation curves, or a working VTuber rig.
- Source sheets are counted as primary assets. Cropped key poses, peak copies, prompts and JSON are separate supporting files and do not inflate primary counts.
- The user approved splitting finished sheets into individual PNG frames. Originals remain byte-identical. `frame_extraction.json` records exact integer crop bounds, dimensions, hashes and pixel equality. No resampling, painting or registration is performed.
- The generated poses are not pixel-registered animation frames. Framing, scale, perspective and illustrative anatomy can vary. A modeler/animator must resolve continuity on the actual mesh rather than directly playing cropped images as a calibrated animation.
- Most motion sheets contain nine poses; jawRight is explicitly a three-panel comparative guide, and vowelChart is a mouth-shape comparison rather than a temporal speech performance. Eye/mouth modeling details are six-panel comparisons, not nine-frame motion sheets.
- The 24 planned controls yielded 22 accepted references. `CTL-jawLeft` and `CTL-lowerLipDepress` are unavailable: attempts did not isolate the intended motion reliably. The actual mesh still requires these controls to be designed and tested where needed. No ARKit52 or runtime certification is claimed.
- Teeth, tongue, hidden surfaces and hair construction details are illustrative proposals, not verified unseen geometry. The neutral face plus front/back full-body masters govern identity and costume when a secondary detail conflicts.
- Graphic sweat, tears, blush, motion strokes and similar accents are visual performance suggestions, not implemented effects or physical geometry.
- Expression-to-body pairings are reusable separate references, not bespoke combined animations. Timing values are suggested performance timing, not measured animation playback.
- A rejected or pending image must not be published as accepted. Review decisions are bound to source SHA-256; changed bytes require renewed review. Frozen batch manifests preserve the exact approved source and support-file set.
