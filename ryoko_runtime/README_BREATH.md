# Controlled inhale and exhale

User-approved on 2026-11-05 and integrated with rigid-iris gaze, neutral brows, look-at and hairpin ornament. This adds a small optional breath deformation, not another automatic idle loop.

## Controls

- I triggers one inhale/exhale, lasting approximately six seconds.
- API/live UDP: `breath_trigger: true`, with optional `breath_strength` from 0 to 1. Trigger once; do not repeat the trigger in every heartbeat.
- `breath_level` from 0 to 1 holds a controlled inhalation level for animation or tracking input.
- `breath_cancel: true` eases back to rest. R/reset clears it immediately.
- UDP timeout releases breathing with the other live controls.

The shoulder line and chest share a four-source-pixel upward lift at full strength. Shallow rib expansion adds up to 1.2 percent lateral displacement below the shoulders and blends to zero at the anchored lower edge. The neck transition is smooth, while the face and upper head receive zero additional displacement. Both sides expand symmetrically. The displacement follows the torso's rotation.

The new breath is off by default. Existing approved motion, subtle legacy idle movement, torso/chest follow-through, crown lag, gaze, mouth and eyelids are preserved. The new breath does not drive the chest spring or create recurring chest bounce. Pausing a timed clip freezes the entire rig, including breathing, under the existing pause behavior.

## Validation

`test_breath.gd` covers default rest, bounded inhale/exhale, manual level, cancellation, anchored head/base, symmetric expansion, shoulder/chest coupling, strength/reset, live runtime/shader wiring, real UDP delivery and timeout release. It passes 15,974 checks. All 14 previous suites are rerun.

`--breath-proof` records two actual Godot breaths: one neutral and one layered over a held head/torso pose. The character returns to rest after each. A runtime crop supplements the full-frame MP4 for the small movement. Video inspection uses chronological decoded frames; normal-speed playback is unavailable here.

No new artwork is produced. Original PNGs and the approved rigid-iris textures are unchanged. The user reviewed and approved the runtime proof before publication.
