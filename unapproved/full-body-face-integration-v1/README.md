# Full-body expression integration, review in progress

The user requested that all 47 already-approved expressions work on the assembled VTuber. This candidate exposes and operates those existing performances on the approved full-body rig. It adds no new expression, artwork or body animation.

The normal project launch now opens the full-body viewer. It includes the 47-expression picker, Play/Stop, all 27 original manual face channels, auto-blink controls, body/bounce controls and the unchanged opt-in local bridge bound to the same full-body controller. Reset and manual takeover cover the whole model. The old bust-only viewer remains available explicitly.

A Godot 4.6.3 compiler error in the existing eye-opening shader is repaired by binding the identical owner texture to an explicit sampler, rather than passing the built-in TEXTURE as a helper argument. No profile timing, geometry formula or artwork is changed.

- [Focused viewer/runtime checks](../../ryoko_object_rig/full_body/face_review/viewer_controls.json): 511 PASS across all 47 profiles, head attachment, playback/release/reset, retained controls, ownership and bounded bridge responses. No network port was bound by these tests.
- [Sampler compatibility record](../../ryoko_object_rig/full_body/face_review/shader_compatibility.json)
- [First visible integrated preview](../../ryoko_object_rig/full_body/face_review/live_affection_full_body.mp4): existing Affectionate Warmth on the full body, with a close-up of the same scene and frame. Other profiles are still being rendered and visually checked.

The preview uses actual Godot scene transforms, geometry, shader uniforms and original textures in an offscreen shader reconstruction. It is **not a native Godot screen capture**. Native renderer parity and live pacing remain unverified. The complete 47-expression visual pass is in progress; this checkpoint is not a claim that every profile has already passed visual review.

Main remains the accepted neutral/bounce checkpoint. Its approval records and source guard are frozen historical contracts for that checkpoint; this review intentionally changes the listed integration files and has not updated those approved inventories. Do not present their unchanged hashes as a current candidate pass. The complete integration will remain on this review branch until reviewed.
