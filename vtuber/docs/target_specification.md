# Ryoko VTuber — Target Specification

**Phase:** 0 — Target and environment specification  
**Status:** Complete; awaiting user checkpoint approval before Phase 1  
**Prepared:** 2026-11-01

## Confirmed targets

| Area | Decision |
|---|---|
| Character | Full-body human anime-style Ryoko; preserve the established repository design |
| Presentation | Full-character wall projection with readable facial acting and body gestures |
| Primary runtime | VSeeFace on 64-bit Windows, subject to AI-control integration validation |
| Avatar format | VRM 0.x / VRM0X, not VRM 1.0 |
| Primary animation source | Blender-authored actions, poses, shape-key curves, transitions, and reusable performances |
| Performance controller | An AI selects, parameterizes, interrupts, and blends authored animation states |
| Facial tracking | iPhone ARKit perfect-sync input supported as a live input/override, not the sole animation source |
| Body tracking | Webcam-based body input through a compatible VMC tracking route when live body tracking is enabled |
| Performance goal | High-detail avatar targeting 2560×1440 at 60 fps on the user's final Windows hardware |
| Authoring | Editable Blender source with milestone saves and rendered comparison checkpoints |

## AI-directed animation architecture

Blender is the authoring source of truth for the avatar's reusable performance library. The AI controller communicates high-level intent or state; it does not need to author deformation geometry or animation curves during a live session.

Initial state families include:

- Neutral idle, breathing, subtle posture shifts, blink, and gaze
- Talking, listening, thinking, reacting, and conversational turn-taking
- Reusable emotional facial presets and head accents
- Full-body gestures, including crossed arms, finger-wag reprimands, stern stances, and scolding
- Enter/exit transitions, interrupted-action recovery, loop handling, and return to neutral

Authoring requirements:

- Keep facial, head, body, and secondary-motion channels separable so the controller can compose them deliberately.
- Define stable action/state IDs, loop boundaries, transition durations, interrupt rules, and procedural override policies.
- Preserve a safe neutral state and prevent additive blinks, mouth openings, or body channels from accumulating incorrectly.
- Bake/export Blender actions or translate them into runtime control data as required. A `.blend` action is not itself a runtime controller.
- Determine during integration whether VSeeFace plus a control bridge is sufficient or whether a Unity/VRM runtime layer is needed for the AI state machine.
- Test actual AI-triggered state changes, interruption, blending, and recovery before declaring the control route complete.

## Runtime and tracking requirements

- Export **VRM 0.x**. VSeeFace's official documentation explicitly states that VRM 1.0 models are unsupported.
- Include all **52 ARKit blendshape clips** required by the selected iPhone perfect-sync route. Empty placeholder clips are not evidence of a working facial rig; every required deformation must be tested on the real mesh.
- Include VSeeFace's standard mouth, blink, expression, and eyebrow mappings in addition to the ARKit set.
- Treat webcam full-body tracking as a separate VMC input route. VSeeFace's ordinary webcam tracking must not be described as built-in full-body tracking.
- Use a compatible iPhone sender supported by VSeeFace, such as iFacialMocap, FaceMotion3D, or VTube Studio. Select the exact sender during runtime integration.
- Define precedence when AI-authored motion and live tracking are both active: full override, additive composition, or per-channel suppression.
- Validate hybrid lip-sync behavior so AI speech, audio visemes, and ARKit mouth controls do not add incompatible openings.

## Initial high-detail budgets

These are starting budgets, not a guarantee of 1440p60. Final budgets depend on measured performance on the user's hardware.

- Prioritize face, eyes, hands, hair silhouette, and costume deformation over invisible geometry.
- Keep the avatar modular during authoring, but control final mesh and material counts to avoid runtime overhead.
- Use model-fitted UVs and efficient texture atlases; 4K maps are allowed only where they visibly improve the final result.
- Avoid unnecessary subdivision, transparent overdraw, duplicated hidden geometry, and expensive simulation.
- Provide a lower-cost fallback if the high-detail configuration cannot sustain the target frame rate.

## Validation boundary

The Linux build environment can author and test Blender geometry, rigs, shape keys, animation curves, renders, and exports. It cannot certify VSeeFace tracking, the final AI-control bridge, or Windows performance without the user's Windows runtime and devices. Final VSeeFace, AI-state, iPhone, webcam-body, audio, OBS, hardware-performance, and physical wall-projection tests require user-side validation.

## Open but non-blocking decisions

- Exact AI host, control protocol, and whether a Unity/VRM runtime layer is required
- Exact iPhone sender application and version
- Exact webcam-body/VMC sender and final live body-tracking coverage
- Final Windows GPU/CPU and webcam/iPhone models
- Which illustrated effects to implement: blush, tears, sweat, sparkle eyes, graphic marks, or chibi cutaways
- Final OBS capture and projection configuration

These items remain recorded for later phases. They do not justify claiming compatibility before testing.

## Official references

- [VSeeFace official site and manual](https://www.vseeface.icu/)
- [VTube Studio: sending iPhone tracking data to VSeeFace](https://github.com/DenchiSoft/VTubeStudio/wiki/Sending-data-to-VSeeFace)
