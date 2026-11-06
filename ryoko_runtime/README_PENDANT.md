# Approved necklace-pendant motion

Based on approved main `bd4888a`. The user approved this accessory addition's actual Godot runtime review on 2026-11-06. It moves only the small original green pendant below its lower bail. The necklace chain and upper bail remain fixed to their existing body artwork. No new expression, replacement necklace, full-body rig, shader sampler or viewport is added. Native-speed playback and live performance remain unverified.

## Controls and lifecycle

- Direct API, opt-in loopback UDP and version-1 clips accept `pendant_secondary: true` or `false`. It defaults on. No keyboard shortcut is added.
- Disabled and zero-angle states render the exact original `artwork/bust_base.png` and hide the derivative cutout. Turning off updates the texture and visibility immediately, including during a paused clip.
- Turning on begins from cleared dynamics. While paused it stays quiet until playback resumes. Reapplying an unchanged setting does not disturb the current state.
- Reset, live-input timeout and cancellation of an active or paused clip clear pendant dynamics but preserve the enabled preference. A repeated stop while already inactive does not erase later live dynamics.
- Clip pause holds the angle, spring velocity, anchor history, source pivot, texture choice and cue clock. Natural completion retains the final toggle. A clip that disables the pendant must explicitly re-enable it if that is the intended final setting.
- Direct malformed `pendant_secondary` values reject the entire patch before any mutation, including reset, facial effects and clip ownership. UDP and clip loading require a real JSON boolean; numeric/text lookalikes are rejected. An invalid replacement leaves an active or paused clip untouched.
- Valid loopback input takes over from a recorded clip. The existing opt-in, loopback-only binding, sequence checks and two-second timeout remain unchanged.

Example after starting with the existing `--live-input` opt-in:

    python send_live.py --seq 1 '{"pendant_secondary":true,"body_tilt":0.7,"body_x":0.4}'

A body-controlled demonstration is supplied separately in `demo_pendant_clip.json`. Existing demo files and their cues are unchanged.

## Source registration and rendering

The `1136 × 1384` canvas is unchanged. The local pivot is `(563.5, 933)`, with region `(547, 933, 34, 33)`. Chain and upper-bail pixels through y932 stay in place. `rig_assets/pendant_layers.json` records the source, source hash, pivot, rectangle and derivative filenames.

The facial controller exposes its existing base as `base_sprite`. The rig retains that original texture resource. A `Node2D` pivot and region-clipped `Sprite2D` compose the small cutout immediately after the base inside the original facial viewport, before facial overlays. At nonzero relative angle the base switches to `pendant_cleared_base.png`; the sprite uses `pendant_cutout.png`. Both are full-canvas derivatives of the original pixels. Zero and disabled states bypass both derivatives.

The original mesh then deforms the completed viewport exactly as before. The source pivot stays fixed, so the pendant and chain continue through the same body, chest, bounce and breathing deformation. This is **not a perfectly rigid screen-space transform**: the existing chest and breathing fields vary across this region. No deformation shader, shared vertex include, shader sampler or mesh topology changes are needed.

The deterministic short-pendant driver uses the existing 32 × 40 mesh's actual triangle interpolation to calculate the moving attachment and its local downward direction. It includes torso movement, chest follow-through, bounce and controlled breath. Independent head input, crown/hair motion and periodic baseline breathing do not drive it. With the inherited `body_follow` setting on, head input also commands the body; use `body_follow: false` for a genuinely head-only comparison.

Transient sway is capped at 6 degrees. Total relative angle is capped at 10 degrees, with modest 80% compensation toward vertical at held body tilt. The spring uses 240 Hz substeps, caps time steps and impulses, bounds extreme finite inputs before arithmetic, rejects nonfinite/nonpositive time steps and snaps quiet transient state to exact zero. It contains no periodic idle oscillator.

## Artwork limits and review status

`tools/build_pendant_layers.py` reproduces the derivatives from existing source pixels. The 730-pixel moving mask retains the original green stone, border and small shadow. All original source pixels remain unchanged. Local harmonic skin interpolation supplies the area exposed behind the moving pendant; it is estimated hidden skin, not recovered artwork. The source shadow moves with the pendant and is not relit. The small retained skin fringe can become visible at enlargement. No collision, 3D chain or jewelry-lighting model is implemented.

Actual Godot on/off neutral captures and three disabled comparisons against approved main are pixel-identical. Chronological runtime frames and enlarged limit/combined-control captures have been inspected; the user approved the supplied runtime review. The runtime's original-base bypass avoids a stationary composite seam. Native-speed playback and low-limit hardware compatibility are not verified. See `VALIDATION_PENDANT.md` for automated checks, actual capture evidence and remaining limits.

## Local checks

    godot --headless --path . --script res://test_pendant.gd

Use writable local `HOME`, `XDG_DATA_HOME` and `XDG_CONFIG_HOME` directories when the execution environment cannot write Godot's default user-data directories. These environment variables relocate test fixtures and logs without changing project behavior. No network service is opened unless explicitly requested; the focused suite opens only temporary localhost sockets for its acceptance/rejection tests.
