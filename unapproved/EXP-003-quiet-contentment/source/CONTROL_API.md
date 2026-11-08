# Shared expression control API

Use `expression_rig.gd` through `expression_rig.tscn`, or call `expression_viewer.apply_controls(dictionary)` for the default app. Both use the same validated player. This remains the authoritative callable Godot API. The opt-in loopback socket adapter in `LOCAL_CONTROL_BRIDGE.md` delegates to this same controller; no AI-model or voice-service connection is claimed.

## Calls

- `list_expressions()` returns detached `{id,title,duration,aliases}` entries. Currently EXP-163 / Yawn, EXP-005 / Hearty laughter, EXP-001 / Bright welcome, EXP-006 / Suppressed giggle, EXP-107 / Confident reassurance, EXP-007 / Relieved smile and EXP-003 / Quiet contentment are authored. Approval and publication status is recorded separately in `RELEASE.json`. Other historical catalogue IDs are references, not playable placeholders.
- `apply_controls(dictionary) -> bool` validates the entire transaction before changing controls, clock or ownership. Failure returns false and sets `last_error`; no partial pose/state mutation occurs.
- `play_expression(id)`, `release()` and `reset()` wrap their corresponding control transactions.
- `advance(delta) -> bool` advances deterministically. Delta must be finite and nonnegative. The engine calls it from `_process`; an external deterministic driver must disable automatic processing to avoid advancing twice.
- `get_state()` returns detached `registry_ready`, `active_expression`, `time`, `phase`, `release_time`, normalized `controls`, actual `displayed_controls`, feature `owners`, actual `auto_blink`, deferred `auto_blink_pending_restore` and `last_error`.
- `sample_expression(id,time)` returns a pose without changing playback. Unknown IDs or nonfinite time return `{}` and set `last_error`. Time outside the duration returns neutral. A sample is not a command.

The same `apply_controls` contract is the external adapter entry point. Do not expose direct calls to historical `object_rig`, `object_face` internals, registry mutation or `_apply_performance_pose` as external controls.

## Transactions and ownership

    {"perform_expression":"EXP-163"}
    {"perform_expression":"yawn"}
    {"release_performance":true}
    {"mouth_open":0.3,"blink_R":0.7}
    {"reset":true}

Trigger and release must each be separate transactions. A trigger starts from the displayed pose and joins the new timeline over 0.30 seconds. A release captures the displayed pose and returns to neutral over 0.45 seconds. Both temporarily suspend auto blink, retaining its prior enabled intent across retriggers and repeated releases. These are coordinate transitions, never texture/opacity fades.

A valid manual transaction cancels performance/release ownership and any deferred auto-blink restoration, including an explicit `auto_blink:false` while the actual state is already temporarily false. Unspecified channels keep their current control values; the supplied channels change. There are no stale tweens or timers that resume later. All four feature groups report the active expression ID, `release`, or `manual` as their owner.

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
- `auto_blink`: boolean, immediate manual-mode closure floor. Like other manual fields, writing it takes ownership and cancels unfinished performance/release and deferred restoration. It is not a queue-only preference update.
- `mouth` / `viseme`: only REST, RELEASE or NEUTRAL, case-insensitive, restore continuous neutral. A/E/I/O/U are unsupported and rejected atomically.

All numeric values must be actual finite numbers, not booleans or numeric strings. Unknown control keys and unregistered expression IDs are rejected. Only the bounded generic controller is the supported public interface. The low-level historical base's legacy discrete visemes are diagnostic compatibility behavior and can bypass this app's cap if called directly.

## Data registry and timeline schema

`expressions/registry.json` contains `schema_version:1` and a nonempty `entries` array. Each entry has a unique nonempty `id`, a local `res://...json` `path`, optional nonempty unique string `aliases`, and optional nonempty `trigger_phase` (default `anticipation`). IDs/aliases are case-sensitive. No alias may collide with any ID or alias. Unknown keys reject the catalogue. No parent-directory or nonlocal paths are accepted.

Each definition contains matching `id`, nonempty `title`, positive finite `duration`, and at least two `keyframes`. A keyframe contains only finite `time`, nonempty `phase` and `values`. Times strictly increase from exactly 0 through exactly duration; first/last poses must be neutral. Missing channels mean zero. Adjacent poses use cubic smoothstep interpolation, preserving the approved sampler.

Allowed timeline channels are `blink_R`, `blink_L`, `brow_screen_left`, `brow_screen_right`, `brow_tilt_screen_left`, `brow_tilt_screen_right`, `gaze_x`, `gaze_y`, `hair_sway`, `mouth_open`, `mouth_smile`, `mouth_spread`, `eye_smile_R`, `eye_smile_L`, `mouth_corner_lift`, `mouth_lip_press`, `mouth_oral_lift`, `mouth_purse` and `blush_intensity`, with the bounds documented in this file. The only optional definition metadata keys are `status`, `intent`, `source_catalogue_sha256`, `timing_origin`, `scope` and `interpolation`, all strings. The historical `interpolation` field is descriptive metadata, not executable logic or a mode selector.

Catalogue loads validate all entries before replacement. Failure preserves the previous catalogue. Returned definitions and listings are deep copies. Only actual authored performances belong in the runtime registry. Approval and publication history is recorded in `RELEASE.json` and predecessor receipts. Test-only fixtures and the other historical IDs do not constitute authored expressions.

## Compatibility and review

`yawn_rig.gd` delegates all logic to the generic controller and retains only `sample_yawn(time)`, the historical `DURATION` constant, labels and the Y shortcut for existing tools. `yawn_stage` remains a separate synchronized review scene. The default `expression_viewer` contains one rig and uses the same API. All legacy static expression commands remain unsupported; there are not 93 implemented registry entries.

## Lateral mouth support

`mouth_spread` is a finite number in [0,1], default 0. Effective spread is `mouth_spread * mouth_smile`. It drives fixed-texture, fixed-UV, unit-scale rigid lip owners and spatially reveals source-derived oral surfaces. Maximum half-width increment is 20 source pixels; additional corner lift is 5 and central lift is 4. It does not change the physical mouth-open limit (0.55; 30.8 source pixels per column). Lifecycle, atomic validation and manual ownership use the same shared player. EXP-001 (`bright_welcome`) is 3.0 seconds. All seven authored IDs listed above are registered. Oral-lift and purse controls are documented below. Wide-eye support is not included.

## Closed smile and independent blush FX

- `mouth_corner_lift`: finite [0,1], default 0. Adds up to 12 source pixels of cubic radial corner lift through rigid upper/lower lip segments. Endpoint secants avoid hooked corners. The original zero-control geometry is preserved.
- `mouth_lip_press`: finite [0,1], default 0. Reveals up to 4 source pixels of inferred hidden inner-upper-lip tissue using fourteen fixed-UV children of the existing upper-lip pivots. It does not lower the outer mouth or move/tint teeth.
- `blush_intensity`: finite [0,1], default 0. Controls only the alpha intensity of two independent, fixed registered original cheek FX sprites. These are `face.effect_objects`, distinct from opaque anatomy owners in `face.objects`. They retain fixed texture/UV, position, rotation and unit scale, at z=29 below eyes and foreground hair. Their cheek masks exclude eyes, nose, mouth and neck. This is not a face texture swap or facial opacity crossfade.

All three controls participate in generic atomic validation, manual takeover, continuous retrigger/release and exact reset. FX ownership follows the same active expression, release or manual writer. Missing required FX textures fail readiness. Profiles that omit these controls default to zero. EXP-006, EXP-107 and EXP-007 use their individually authored values; omitted controls do not acquire another profile's values.

## Rigid lower oral-surface lift

`mouth_oral_lift` is finite [0,1], default 0. It participates in the same atomic validator, registry, sampler, current/displayed pose, manual takeover, release, retrigger, interrupted handover, reset, viewer slider and preparation-only local bridge. Missing profile values are zero. The four profiles predating EXP-107 omit this channel; EXP-107 and EXP-007 use their authored oral-lift values.

Effective spread is `mouth_spread * mouth_smile`. Additional upward travel is `40 * (1 - effective_spread) * mouth_oral_lift` source pixels. Only the existing `spread_lower_oral_surface` owner changes position, with X 510 and Y `667 - 40 * effective_spread + 2.75 * mouth_open - additional_travel`. Total upward movement never exceeds its already supported 40-pixel spread envelope. Zero retains the exact predecessor operation order; full effective spread provides no further rise. No width, aperture, lip, central white enamel, texture, UV, region, tint, alpha, rotation or local scale changes. The original yawn tongue is unchanged.

## Rigid purse control and manual blinking

`mouth_purse` is finite [0,1], default 0, and is transported through the same atomic public control validator, timeline sampler, displayed/current state, manual takeover, reset, retrigger, release, viewer slider and preparation-only bridge. Missing profile values default to zero, preserving all five prior definitions. Public discrete visemes remain rejected; the old composite O/U images are not used by this channel.

Purse translates existing upper/lower lip strips and independent corners inward by at most 14 source pixels per side, rotates them to a rounded contour, and uses spatial clipping for only the extra geometric overlap. Fixed native pigment/UV, atlas regions, unit local scales and opaque anatomical owner modulation remain unchanged. The original O/U assembly images are contour references only. Existing cavity, fixed white enamel at (533,626), and independently translated oral surface stay separate. The upper contour has a bounded vertical offset of 4–12 source pixels at full purse. Relative lower separation is clamped nonnegative and never exceeds the existing 30.8-source-pixel aperture bound. Zero uses the predecessor coordinate/coverage path. Nonzero overlap clipping compares oriented normal distances against the zero-purse baseline, retaining a finite denominator even when neighboring edges become horizontal or reverse.

Auto-blink defaults to off. If it is enabled before a performance or idle release, the shared controller captures the displayed lid pose, temporarily suspends automatic blinking and retains `auto_blink_pending_restore:true`. Retrigger, cross-profile handoff and repeated release preserve that intent instead of reading temporary `auto_blink:false` as a new preference. Completion or interrupted release restores it only after playback/release ownership has ended and every control is exactly neutral. An empty `active_expression` alone is insufficient during release.

Restoration clears pending intent once and restarts the unchanged base 4.2-second cycle at its open phase (`elapsed=0`), with the same final .34-second sinusoidal closure. It does not resume a stale mid-blink clock or add a new blink style. Any delta overshoot is handled as before: the completion call ends at the neutral boundary; the next idle advance begins the blink clock. `advance(0)` cannot complete a positive-duration performance/release; it may refresh the inherited phase label at the current keyframe. Zero-duration profile definitions remain invalid.

Successful manual takeover, explicit disabling and reset cancel pending intent. Initially disabled blinking stays disabled. Reset plus explicit `auto_blink:true` still enables it after the reset, as before. Empty transactions, `reset:false` alone, `release_performance:false`, invalid transactions and read-only calls cannot erase intent. Paused processing cannot complete recovery or restore blinking by a timer. The public API retains immediate manual ownership: an explicit auto-blink write during recovery cancels recovery rather than silently queuing a setting.

`get_state().auto_blink` reports actual activity; `auto_blink_pending_restore` reports intended resumption after neutral recovery. `auto_blink_policy()` returns a detached description of this policy, also included in bridge capabilities. The viewer checkbox is labeled as a preference, stays checked while the saved intent is suspended, and separately says active, paused until neutral recovery, or off. Changing it is visibly labeled manual takeover. The local bridge remains preparation only, with no actual AI/TTS or socket integration validation claimed.

## EXP-003 data-only addition

The registry exposes EXP-003 / Quiet contentment through aliases `quiet-contentment` and `contentment`. Its nine keys span 1.9 seconds. Six predecessor performances are approved; EXP-003 is a local review candidate. This extension adds no control or player behavior. It inherits the separately published neutral-boundary blink preference restoration from parent 8c349e29. All expression controls recover to exact zero and ordinary idle eyes before saved automatic blinking resumes.
