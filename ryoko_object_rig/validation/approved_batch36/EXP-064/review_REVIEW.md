# Shocked Gasp EXP-064 independent review

Status: PASS for unapproved review delivery. No integration or approval is implied.

The actual source sheet, seven native static bust/detail pairs, selected encoded phases and all native/decoded frame evidence were inspected. The rapid opening into a taller held gasp and smaller residual mouth is clearly different from neutral at bust size. Raised inner brows support surprise/apprehension. The source has much rounder eyes and taller painted oral anatomy; the current rig's bounded upper-eye opening and split-lip mouth only approximate those shapes. There is no jaw motion or breathing simulation. The enlarged detail crop retains inherited lash/hair edge seams. No clear new mouth break or eye-render failure was found.

## Verification

- All 1,124 frozen baseline files and 184 PNGs match both the isolated rig and original approved27 snapshot. Production registry stays at 27 and excludes EXP-064. Only recorded import UID metadata is additional.
- Source sheet, catalogue and all nine referenced panel hashes match.
- Native static 496 checks and native motion 7,541 checks pass. Native logs have the known V-Sync/raw-image export warnings, but no ERROR or custom-sampler diagnostic. The broader headless shader diagnostic is not a native rendering pass and is not concealed.
- All 242 native RGBA hashes match capture records; all 121 captured poses equal the headless timeline records.
- Exact neutral bookends and static/held-peak parity pass. All changes are inside the bust face region [215,283,345,402]; body/background pixels are unchanged.
- MP4 has 121 frames at 30 fps, 968×800 H.264 yuv420p, 4.033333 seconds, 173,655 bytes. Full decode has no errors. Each decoded panel was compared to its same-index native frame, with monotonic 30 fps timestamps and nearest-frame checks. Maximum expected-versus-best face error difference is 0.001822, consistent with near-identical frames and lossy encoding rather than reordered acting.

MP4 SHA-256: dc12527791221935a345f3a94ddd6575b6929e2b44e293f9f37ff17eb6d4f80a

## Scope

This review independently checks static and encoded pixels, source preservation, frame hashes and chronology. Parent-controlled sampled 1× playback is recorded separately when supplied. It does not claim continuous human observation, live Godot frame pacing, complete runtime coverage, export readiness, lip-sync, user approval or integration.

Evidence: review_evidence/review_checks.json, native_frame_hashes.json, decoded_frame_order.json, static_faces.png, encoded_keyframes.png and bust_progression.png. The review script requires the original local baseline/source paths; it is not a portable standalone source archive.

## Parent playback observation

The parent sampled default 1× ffplay at 1180×812 bust/detail viewing size, observing the large open gasp/inner-brow rise and returned closed-mouth neutral. Mouth action read clearly; eyes remained less round than the source. Player closure was verified. This is sampled-phase evidence, not continuous observation or live engine pacing. See PLAYBACK_REVIEW.json.
