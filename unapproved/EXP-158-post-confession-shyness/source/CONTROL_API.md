# Current EXP-158 local review candidate

This package has **13 registered/authored expressions and 12 approved/published predecessors**. EXP-158 Post-confession shyness remains pending user approval. An unapproved-folder Git backup preserves work and does not approve or integrate it into the approved rig. All runtime, art and predecessor profiles are exact to main d5a4539c.

Run `python tools/verify_post_confession_shyness_package.py`. The authoritative current package files are `POST_CONFESSION_SHYNESS_SOURCE_MANIFEST.json` and `POST_CONFESSION_SHYNESS_FILES.sha256`. Generic `CURRENT_SOURCE_MANIFEST.json`, `PUBLICATION_SOURCE_MANIFEST.json`, `SOURCE_FILES.sha256`, and predecessor guards are retained historical evidence and are not this successor's verifier. The seven changed documentary files from the captured implementation are preserved under `post_confession_shyness_capture_metadata/`. No registry, runtime, artwork, test or capture-harness byte differs from the captured freeze. EXP-158 profile interpolation prose only adds a missing space; every timing and control value is exact.

Original source proof uses pinned commit/path/hash and portable `../original_reference/` paths, relative to this rig directory. A complete recovery/backup bundle should include the original sheet and 9 panels there. They are comparison evidence, not runtime face/parts substitutions.

## Preserved prior documentation

# Shared expression control API

Twelve user-approved performances share one rig: EXP-163/005/001/006/107/007/002/152/160/177/164/021. EXP-021 Quiet sadness is the approved 3.65-second, five-key data-only performance, available through the existing API and quiet-sadness / quiet_sadness aliases. All eleven predecessor profiles, shared runtime, scenes, shaders and 182 PNGs remain byte-identical to main 2d46f72704ddf2a329b44a87cd24c66d5fe92568. Only EXP-021 profile status changes from its reviewed source; all other fields, times and control values are exact. EXP-003/139/170/153/161 and every other unregistered draft remain excluded.

Current publication checks: python tools/verify_quiet_sadness_publication.py and sha256sum -c SOURCE_FILES.sha256. PUBLICATION_SOURCE_MANIFEST.json is the current manifest. CURRENT_SOURCE_MANIFEST.json, tools/verify_quiet_sadness_package.py, QUIET_SADNESS_CAPTURE_FREEZE.json, historical_capture_metadata/ and inherited exact-scope receipts remain byte-exact historical contracts for their original source trees; do not run them as current publication guards. The historical backbone fixture also remains unchanged and is not a twelve-profile smoke test. Use tests/test_quiet_sadness_runtime.gd for the actual twelve-profile registry. See QUIET_SADNESS_PUBLICATION_VALIDATION.md for scope, evidence and limits.

## Historical published baseline

Eleven user-approved performances share one rig: EXP-163/005/001/006/107/007/002/152/160/177/164. Fighting sleep adds the approved 3.47-second data-only performance. All ten predecessor profiles, shared runtime, shaders, scenes and 182 PNGs remain byte-identical to main 958eb944a37ce836fec5acf369f12b89f47b6656. Only the EXP-164 profile status text changes from its approved review; all other fields, times, phases and values remain exact. EXP-003/170/139, inner-cover experiments and all other unregistered drafts remain excluded. RELEASE.json and FIGHTING_SLEEP_PUBLICATION_VALIDATION.md record current status. Earlier explicitly marked checkpoints and frozen review receipts are historical provenance. No normal-speed playback observation, AI/TTS or real-socket validation is claimed.

Historical EXP-177 publication checkpoint:

Ten user-approved performances share one rig: EXP-163/005/001/006/107/007/002/152/160/177. Revised EXP-177 Meditative calm adds a single continuous 1.2-second closing arc, with unchanged hold/opening keys from 1.2 seconds onward. All nine prior profiles, gaze_down_extra, rigid outer-anchor brow controls, automatic-blink restoration, runtime and all 182 PNGs remain exact. EXP-003/164 and all other unregistered drafts remain excluded. See MEDITATIVE_PUBLICATION_VALIDATION.md for approval, source identities and verification. Earlier explicitly marked checkpoint descriptions below are historical provenance. The EXP-177 publication profile changes only its status text; every other reviewed field and motion value is exact.

Historical EXP-160 checkpoint: nine user-approved performances shared one rig: EXP-163/005/001/006/107/007/002/152/160. The published002/152 profiles, hidden-iris support and gaze_down_extra semantics are preserved. EXP-160 adds the approved default-zero rigid outer-anchor brow capability without new artwork. EXP-003/177/161/153 remain excluded. See SHY_MERGED_PUBLICATION_VALIDATION.md for merged scope and evidence; preceding frozen review stages are historical.

Use `expression_rig.gd` through `expression_rig.tscn`, or call `expression_viewer.apply_controls(dictionary)` for the default app. Both use the same validated player. This remains the authoritative callable Godot API. The opt-in loopback socket adapter in `LOCAL_CONTROL_BRIDGE.md` delegates to this same controller; no AI-model or voice-service connection is claimed.

## Calls

- `list_expressions()` returns detached `{id,title,duration,aliases}` entries for the twelve IDs in `expressions/registry.json`. EXP-021 / Quiet sadness is a local review candidate. The eleven predecessors in `RELEASE.json` remain approved/published. This package does not mark EXP-021 approved.
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

`mouth_spread` is a finite number in [0,1], default 0. Effective spread is `mouth_spread * mouth_smile`. It drives fixed-texture, fixed-UV, unit-scale rigid lip owners and spatially reveals source-derived oral surfaces. Maximum half-width increment is 20 source pixels; additional corner lift is 5 and central lift is 4. It does not change the physical mouth-open limit (0.55; 30.8 source pixels per column). Lifecycle, atomic validation and manual ownership use the same shared player. EXP-001 (`bright_welcome`) is 3.0 seconds. All eleven authored IDs listed above are registered. Oral-lift and purse controls are documented below. Wide-eye support is not included.

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

## Approved downward-gaze extension

`gaze_down_extra` is a finite normalized number in [0,1], default zero. The old `gaze_x` and `gaze_y` contracts are unchanged: x maps to ±4 source pixels; negative y maps to up 2 and positive y to down 1. The one eye owner's final vertical rigid translation is:

    old_gaze_y_source_pixels + 5 * gaze_down_extra

Thus the combined domain is x [-4,4], y [-2,6]. Mixed upward input plus extra is deliberately additive: gaze_y=-1 with extra=1 gives down 3; gaze_y=0 with extra=1 gives down 5; gaze_y=1 with extra=1 gives down 6. There is no change to old normalized values and no saturation or second eye owner. The optional field is part of the same atomic control transaction, shared timeline schema, neutral/reset state, retrigger/release interpolation, viewer and preparation-only adapter. Omitted timeline values default to zero.

State controls/displayed_controls and face snapshots gain the new field; capabilities gain an explicit down_extension description. This is an additive schema change, not byte-identical serialized responses. All previously existing field values and rendered behavior at extra=0 remain protected. The prerequisite itself did not author a performance. EXP-152 adds data only; both it and the capability are approved. See DOWN_GAZE_VALIDATION.md for the dependency stage and PRIVATE_PRIDE_SCOPE_VALIDATION.md for the current profile.

## Current EXP-152 local data

All eleven authored IDs use the same player. EXP-152 aliases are private-pride and pride, duration 1.9 seconds. Its gaze leads and outlasts its sealed smile. The optional gaze_down_extra field and old gaze_y combine on the same rigid iris owners. No new control/controller is introduced by EXP-152. Both this profile and its capability dependency are user-approved.


## Preserved EXP-002 affectionate warmth

The approved EXP-002 profile, aliases, reference provenance and capture harnesses are retained. Its default gaze_down_extra is zero. The merged runtime uses the reviewed generic gaze capability and all eleven profiles use the same player. See AFFECTION_SCOPE_VALIDATION.md and MERGED_PUBLICATION_VALIDATION.md.


## Approved rigid inner-brow controls

Independent brow_inner_lift_screen_left and brow_inner_lift_screen_right accept finite [0,1], default 0, and add at most 26 degrees after the legacy tilt about fixed outer-tail anchors. Omitted manual fields retain state; omitted timeline fields and reset default to 0. All eleven profiles use the generic player. The gaze_down_extra control remains independent and zero by default. See BROW_INNER_LIFT_VALIDATION.md for exact geometry and historical evidence.

## Approved EXP-177 meditative calm publication

The user-approved revised EXP-177 (meditative-calm / meditate) is the tenth published performance, based on main 70655752bc82ba01b3fe8f64923360da60c578c9. Its single 1.2-second closing arc and all hold/opening motion match the approved review exactly. All nine prior profiles, runtime, artwork, iris/gaze, brow and automatic-blink behavior remain unchanged. RELEASE.json and MEDITATIVE_STATUS.json record current approval/publication. See MEDITATIVE_PUBLICATION_VALIDATION.md. The primary cumulative archive stays at version 19. No normal-speed playback observation, real-socket test or live AI/TTS connection is claimed.

## Approved EXP-164 Fighting sleep publication

The reviewed 3.47-second fifteen-key performance is the eleventh approved entry, using only existing ordinary lids, rigid brows and a restrained sealed purse. The six holds, source-pose relationships and disclosed timing tradeoffs are unchanged. See FIGHTING_SLEEP_PUBLICATION_VALIDATION.md. The current strict successor guard is tools/verify_fighting_sleep_scope.py; inherited exact-scope guards describe historical parent packages and are run only against their exact reconstructed parent. Primary cumulative archive version 19 and original review media/recovery remain untouched.
