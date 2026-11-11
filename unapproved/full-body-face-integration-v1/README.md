# All 47 expressions on the full-body model

The user requested that all 47 already-approved expressions work on the assembled VTuber. This candidate exposes and operates those existing performances on the approved full-body rig. It adds no new expression, artwork or body animation.

The normal project launch now opens the full-body viewer. It includes the 47-expression picker, Play/Stop, all 27 original manual face channels, auto-blink controls, body/bounce controls and the unchanged opt-in local bridge bound to the same full-body controller. Reset and manual takeover cover the whole model. The old bust-only viewer remains available explicitly.

A Godot 4.6.3 compiler error in the existing eye-opening shader is repaired by binding the identical owner texture to an explicit sampler, rather than passing the built-in TEXTURE as a helper argument. No profile timing, geometry formula or artwork is changed.

- [Focused viewer/runtime checks](../../ryoko_object_rig/full_body/face_review/viewer_controls.json): 511 PASS across all 47 profiles, head attachment, playback/release/reset, retained controls, ownership and bounded bridge responses. No network port was bound by these tests.
- [Sampler compatibility record](../../ryoko_object_rig/full_body/face_review/shader_compatibility.json)
- [First visible integrated preview](../../ryoko_object_rig/full_body/face_review/live_affection_full_body.mp4): existing Affectionate Warmth on the full body, with a close-up of the same scene and frame. The user accepted this first integrated preview. The complete run below now covers all 47 profiles.

The preview uses actual Godot scene transforms, geometry, shader uniforms and original textures in an offscreen shader reconstruction. It is **not a native Godot screen capture**. Native renderer parity and live pacing remain unverified. The complete 47-expression reconstruction visibly changes the face for every profile and returns to byte-identical neutral face and full canvas for all 47. The contact sheet and representative full-size/native-reference comparisons were visually inspected. This is not a claim of native engine pixel parity or real-time pacing.

Main remains the accepted neutral/bounce checkpoint. Its approval records and source guard are frozen historical contracts for that checkpoint; this review intentionally changes the listed integration files and has not updated those approved inventories. Do not present their unchanged hashes as a current candidate pass. The complete integration will remain on this review branch until reviewed.

## Complete run

- [All 47 expressions on the same full-body rig, MP4](../../ryoko_object_rig/full_body/face_review/all47_full_body_live_faces_15fps.mp4): 190.27 seconds, 15fps, original authored durations plus sampled neutral endpoints. The full-body and close-up views use the same model state.
- [47-face contact sheet](../../ryoko_object_rig/full_body/face_review/all47_face_contact_sheet.jpg)
- [Per-expression pixel and neutral-return evidence](../../ryoko_object_rig/full_body/face_review/all47_face_pixel_evidence.csv)
- [Summary](../../ryoko_object_rig/full_body/face_review/all47_summary.json)
- [Reproduction and limits](../../ryoko_object_rig/full_body/face_review/README.md)

Launch the integrated model with `godot --path ryoko_object_rig`. The existing bust-only scene can still be opened explicitly. No listener is enabled unless a control port is supplied.

Run `python -B ryoko_object_rig/full_body/face_review/verify_integration.py` for this candidate's source-preservation check. It allows only the intended viewer/controller-interface, default-scene and sampler-compatibility edits against the accepted main checkpoint. The original 47 profiles, artwork, body registration and physics remain unchanged.
