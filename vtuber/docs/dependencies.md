# Ryoko VTuber — Dependencies and Environment

**Phase:** 0  
**Prepared:** 2026-11-01

## Verified authoring environment

| Component | Verified state |
|---|---|
| Blender Python launcher | `/usr/local/bin/3dpy` available |
| Blender | 5.2.1 LTS, verified through `bpy.app.version_string` |
| Character-model generation SDK | `agent-gw` 0.3.0 available |
| Source references | Existing repository reference pack; no source images modified |

Blender modeling, measurement, rendering, and export scripts will run through `/usr/local/bin/3dpy`. Headless visual checks will use Cycles with neutral lighting. Saved `.blend` files will be reopened and inspected rather than judged only by script exit status.

## Required later toolchain

- VRM 0.x export toolchain compatible with the finished Blender asset
- Unity/UniVRM or another verified VRM0X configuration route where required
- Current patched VSeeFace release on the user's 64-bit Windows system
- User-selected iPhone perfect-sync sender supported by VSeeFace
- Compatible webcam-body tracker capable of sending VMC data when full-body webcam tracking is enabled
- OBS or the user's chosen capture/projection tool

Exact versions will be recorded when those stages are implemented. No add-on or runtime compatibility is claimed solely from installation or successful file export.

## Checkpoint and evidence requirements

Each phase must produce:

1. The phase deliverables or a clear statement of why no visual artifact applies.
2. A build-journal entry describing actual work, evidence, limitations, and the commit.
3. GitHub publication of the phase files.
4. User approval before dependent work begins.

For modeling and expression phases, checkpoints must include matched Blender-versus-reference comparisons. Facial work must show neutral and deformed states from consistent camera angles, including relevant side or close-up views when a front view can conceal eyelid, lip, teeth, tongue, or intersection defects.
