# Shared expression control API

Use `expression_rig.gd` through `expression_rig.tscn`, or call `expression_viewer.apply_controls(dictionary)` for the default app. Both use the same validated player. This remains the authoritative callable Godot API. The opt-in loopback socket adapter in `LOCAL_CONTROL_BRIDGE.md` delegates to this same controller; no AI-model or voice-service connection is claimed.

## Calls

- `list_expressions()` returns detached `{id,title,duration,aliases}` entries. Currently EXP-163 / Yawn, EXP-005 / Hearty laughter and EXP-001 / Bright welcome are authored. Other historical catalogue IDs are references, not playable placeholders.
- `apply_controls(dictionary) -> bool` validates the entire transaction before changing controls, clock or ownership. Failure returns false and sets `last_error`; no partial pose/state mutation occurs.
- `play_expression(id)`, `release()` and `reset()` wrap their corresponding control transactions.
- `advance(delta) -> bool` advances deterministically. Delta must be finite and nonnegative. The engine calls it from `_process`; an external deterministic driver must disable automatic processing to avoid advancing twice.
- `get_state()` returns detached `registry_ready`, `active_expression`, `time`, `phase`, `release_time`, normalized `controls`, actual `displayed_controls`, feature `owners`, `auto_blink` and `last_error`.
- `sample_expression(id,time)` returns a pose without changing playback. Unknown IDs or nonfinite time return `{}` and set `last_error`. Time outside the duration returns neutral. A sample is not a command.

The same `apply_controls` contract is the external adapter entry point. Do not expose direct calls to historical `object_rig`, `object_face` internals, registry mutation or `_apply_performance_pose` as external controls.

## Transactions and ownership

    {"perform_expression":"EXP-163"}
    {"perform_expression":"yawn"}
    {"release_performance":true}
    {"mouth_open":0.3,"blink_R":0.7}
    {"reset":true}

Trigger and release must each be separate transactions. A trigger starts from the displayed pose and joins the new timeline over 0.30 seconds. A release captures the displayed pose and returns to neutral over 0.45 seconds. Both disable auto blink. These are coordinate transitions, never texture/opacity fades.

A valid manual transaction cancels performance/release ownership. Unspecified channels keep their current control values; the supplied channels change. There are no stale tweens or timers that resume later. All four feature groups report the active expression ID, `release`, or `manual` as their owner.

`reset:true` immediately cancels playback/release, clears timeline restart/release state, restores neutral and disables auto blink. It may be combined with valid manual fields, which apply after resetting. `reset:false` by itself, `release_performance:false`, and an empty transaction are no-ops. Successful commands clear `last_error`.

Three explicit lifecycle fixes relative to the old yawn controller:
1. Release ownership changes immediately on the command rather than one engine tick later.
2. Trigger/release capture the visible auto-blink lid position before disabling auto blink, preventing a handover jump; release cannot retain an auto-blink floor.
3. `reset:false` alone no longer cancels a performance.

These fixes do not change the approved ordinary yawn timeline or rendered two-cycle sequence.

## Supported manual fields

- `mouth_open`: normalized [0,1], mapped to physical aperture [0,0.55]. Maximum opening in any vertical source-pixel column is 30.8; maximum central lower-lip translation 29.7. Raised smile corners can make the whole aperture bounding box taller than 30.8; that box is not the physical opening metric. Cannot be combined with `mouth` or `viseme` in one transaction.
- `mouth_spread`: [0,1], lateral rigid-mouth support; effective amount is `mouth_spread * mouth_smile`. See the lateral-mouth section below.
- `mouth_smile`: [0,1], rigid upper/lower lip and corner articulation. Distinct inferred joint owners supply missing contour material; this is not a painted-mouth swap.
- `eye_smile_R`, `eye_smile_L`: [0,1], anatomical R is screen-left. The first half closes the ordinary lids; the second half articulates a fully closed contour into the real historical smiling crescent owners. Independent `blink` supplies a closure floor, so combinations do not reveal an iris through the closed-contour handover.
- `blink`, `blink_L`, `blink_R`: [0,1]. L is anatomical left / screen right. `blink` sets both, then supplied individual fields override their respective eye.
- `brow_raise`, `brow_screen_left`, `brow_screen_right`: [-1,1], rigid translation up to 10 source pixels. `brow_raise` sets both before individual fields.
- `brow_tilt_screen_left`, `brow_tilt_screen_right`: [-1,1], rigid rotation up to 8 degrees.
- `hair_sway`: [-0.07,+0.07]. Out-of-range values reject the complete transaction.
- `gaze_x`, `gaze_y`: shared `control_limits.gd` contract. Normalized [-1,1] maps to bounded source-pixel travel: left/right 4 px, up 2 px, down 1 px. Positive x is screen-right; positive y is down. Both eyes use the same rigid displacement. Unsupported and nonfinite values are rejected before any control/ownership mutation. These are normalized inputs, not pixel coordinates. This scoped release preserves the approved predecessor gaze runtime and artwork exactly.
- `auto_blink`: boolean, manual-mode closure floor.
- `mouth` / `viseme`: only REST, RELEASE or NEUTRAL, case-insensitive, restore continuous neutral. A/E/I/O/U are unsupported and rejected atomically.

All numeric values must be actual finite numbers, not booleans or numeric strings. Unknown control keys and unregistered expression IDs are rejected. Only the bounded generic controller is the supported public interface. The low-level historical base's legacy discrete visemes are diagnostic compatibility behavior and can bypass this app's cap if called directly.

## Data registry and timeline schema

`expressions/registry.json` contains `schema_version:1` and a nonempty `entries` array. Each entry has a unique nonempty `id`, a local `res://...json` `path`, optional nonempty unique string `aliases`, and optional nonempty `trigger_phase` (default `anticipation`). IDs/aliases are case-sensitive. No alias may collide with any ID or alias. Unknown keys reject the catalogue. No parent-directory or nonlocal paths are accepted.

Each definition contains matching `id`, nonempty `title`, positive finite `duration`, and at least two `keyframes`. A keyframe contains only finite `time`, nonempty `phase` and `values`. Times strictly increase from exactly 0 through exactly duration; first/last poses must be neutral. Missing channels mean zero. Adjacent poses use cubic smoothstep interpolation, preserving the approved sampler.

Allowed timeline channels are `blink_R`, `blink_L`, `brow_screen_left`, `brow_screen_right`, `brow_tilt_screen_left`, `brow_tilt_screen_right`, `gaze_x`, `gaze_y`, `hair_sway`, `mouth_open`, `mouth_smile`, `mouth_spread`, `eye_smile_R`, `eye_smile_L`, `mouth_corner_lift`, `mouth_lip_press` and `blush_intensity`, with the same bounds above. The only optional definition metadata keys are `status`, `intent`, `source_catalogue_sha256`, `timing_origin`, `scope` and `interpolation`, all strings. The historical `interpolation` field is descriptive metadata, not executable logic or a mode selector.

Catalogue loads validate all entries before replacement. Failure preserves the previous catalogue. Returned definitions and listings are deep copies. Only actual authored performances belong in the runtime registry. The three predecessor performances are user-approved; EXP-006 is a review candidate; test-only fixtures and the other historical IDs do not constitute authored expressions.

## Compatibility and review

`yawn_rig.gd` delegates all logic to the generic controller and retains only `sample_yawn(time)`, the historical `DURATION` constant, labels and the Y shortcut for existing tools. `yawn_stage` remains a separate synchronized review scene. The default `expression_viewer` contains one rig and uses the same API. All legacy static expression commands remain unsupported; there are not 93 implemented registry entries.

## Lateral mouth support

`mouth_spread` is a finite number in [0,1], default 0. Effective spread is `mouth_spread * mouth_smile`. It drives fixed-texture, fixed-UV, unit-scale rigid lip owners and spatially reveals source-derived oral surfaces. Maximum half-width increment is 20 source pixels; additional corner lift is 5 and central lift is 4. It does not change the physical mouth-open limit (0.55; 30.8 source pixels per column). Lifecycle, atomic validation and manual ownership use the same shared player. EXP-001 (`bright_welcome`) is 3.0 seconds. EXP-163, EXP-005, EXP-001 and EXP-006 are registered. Wide-eye and oral-lift controls are not included.

## Closed smile and independent blush FX

- `mouth_corner_lift`: finite [0,1], default 0. Adds up to 12 source pixels of cubic radial corner lift through rigid upper/lower lip segments. Endpoint secants avoid hooked corners. The original zero-control geometry is preserved.
- `mouth_lip_press`: finite [0,1], default 0. Reveals up to 4 source pixels of inferred hidden inner-upper-lip tissue using fourteen fixed-UV children of the existing upper-lip pivots. It does not lower the outer mouth or move/tint teeth.
- `blush_intensity`: finite [0,1], default 0. Controls only the alpha intensity of two independent, fixed registered original cheek FX sprites. These are `face.effect_objects`, distinct from opaque anatomy owners in `face.objects`. They retain fixed texture/UV, position, rotation and unit scale, at z=29 below eyes and foreground hair. Their cheek masks exclude eyes, nose, mouth and neck. This is not a face texture swap or facial opacity crossfade.

All three controls participate in generic atomic validation, manual takeover, continuous retrigger/release and exact reset. FX ownership follows the same active expression, release or manual writer. Missing required FX textures fail readiness. All prior profiles omit these controls and therefore default to zero.
