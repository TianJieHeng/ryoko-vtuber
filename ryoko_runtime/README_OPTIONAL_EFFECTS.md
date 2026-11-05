# Independent optional effect overlays

The user approved the actual Godot runtime review on 2026-11-05. Based on approved main `4328debdae08f993c90f151a29c0ee8ec7d03f95`, this revision uses the original transparent effect PNGs without generating new expressions or changing the 93 registered expression selections, their artwork, or registration. No full-body changes. Native-speed playback and live performance remain unverified.

## Controls

`MotionRig.apply_controls({"effects": {"blush_L": true, "tear_R": true}})` enables the specified optional overlays. The seven exact keys are `blush_L`, `blush_R`, `tear_L`, `tear_R`, `sweat`, `anger`, and `sparkle`. L is character-left / viewer-right; R is character-right / viewer-left.

Each value must be a boolean. Omitted keys retain their current values; an empty dictionary is a no-op. Unknown keys, arrays, null, numeric lookalikes, strings and other malformed values are rejected before any same-command reset, motion, ownership or overlay changes. This validation is shared by the direct API, version-1 clip loader and loopback UDP decoder. Invalid clip replacements leave running or paused clips untouched.

The existing opt-in UDP adapter accepts, for example:

```json
{"seq": 1, "controls": {"effects": {"blush_L": true, "blush_R": true, "sweat": false}}}
```

There are no added keyboard shortcuts, automatic effects, listener startup changes or expression remappings. Existing live sequence/size/loopback checks remain in force.

## Additive artwork limitation

These controls add optional overlays. They do not remove, hide, replace or recolor blush, tears or other effects already painted into an authored expression. `false` removes only that optional overlay. An expression can therefore still show its own blush or tears with every optional effect off. Switching expression, including selecting `neutral`, preserves explicit optional state. Blinks, mouth shapes, gaze and speech do not change it. Neutral **reset** clears every optional effect, as does the existing live-input timeout reset. All seven overlays are hidden at startup.

## Clip lifecycle

Put `effects` in a version-1 cue's `controls` object. Cues use the same dictionary patch semantics as the live API. The clip owns each optional effect key it actually dispatches, not the entire effects dictionary. Cancellation, active/paused replacement and valid UDP takeover clear only those owned optional keys; unrelated optional states remain intact. Invalid UDP packets do not stop a clip or consume their sequence number. A valid packet stops and releases clip-owned effects first, then applies its own patch.

Pause holds the cue clock and deformation state; direct optional patches can still refresh visibility while paused. Resume continues without repeating cues. Natural completion retains the final values, consistent with existing clip channels; include explicit false cues for an off ending. Replaying starts at cue zero. Repeated stop after completion/inactive cancellation does not erase subsequently set effects. Reset clears all effects and invalidates already-collected remaining cues.

## Rendering and source registration

`rig_assets/effects/manifest.json` maps the original PNG crops into the existing 1136 × 1384 face coordinate space. Each sprite is non-centered, uses the declared source region and scales to the declared target size. The original source checksums and provenance are recorded in the manifest.

The facial controller creates the hidden optional sprites after the authored face layers. In the motion rig, they are moved into a transparent sibling facial effects SubViewport and rendered by a second mesh after the authored face. This deliberate post-gaze composition prevents the iris/brow fragment replacements from overwriting tears or other overlays near the eyes. The second mesh shares the exact grid, transform and unchanged vertex deformation source (`motion_vertex.gdshaderinc`) with the face. All vertex uniforms are discovered and copied from the face material, including during pause. No sampler was added to the existing face shader. The overlay shader uses premultiplied-alpha blending for the transparent viewport. When all effects are off, the second mesh is hidden and its viewport updates are disabled.

## Validation

Run `godot --headless --path . -s test_optional_effects.gd` after importing the project. The focused suite covers all 128 boolean combinations, all 93 existing expressions plus neutral, blink/mouth/gaze independence, untouched authored effect visibility, typed and atomic rejection, invalid replacement, pause/cancel/completion/replay/reset, actual loopback UDP active/paused takeover and timeout, source registration, shared mesh/deformation parameters and disabled-default rendering. Existing `test_*.gd` suites remain applicable. Actual Godot rendering and user video review are separate acceptance steps; passing headless tests is not a visual approval.
