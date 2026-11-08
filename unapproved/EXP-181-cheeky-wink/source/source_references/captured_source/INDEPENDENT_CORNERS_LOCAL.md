# Independent mouth corners: local, unapproved capability

This candidate starts from approved EXP-021 source at d5a4539cd7395783fcbf5756b03bb993be6692b8. All twelve existing profiles and all182 PNGs are unchanged. No EXP-181 profile is registered or authored.

Two controls, `mouth_corner_lift_screen_left` and `mouth_corner_lift_screen_right`, each accept finite [0,1], default0. Screen coordinates identify the visible left/right half. They extend the existing rigid upper/lower lip segments, corner owners and joins on the one shared rig.

At source coordinate x, radius is clamp(abs((x-39.5)/35.5),0,1). Existing bilateral curvature remains exactly -12 * bilateral * radius^3. The applicable new side adds -12 * (1 - bilateral) * side * radius^3. Thus each side spends only the unspent original12px budget. Bilateral1 makes both new inputs geometrically inert. The cubic side term and its first two derivatives vanish at the center; no mouth/face rotation is used. Existing smile, spread and purse retain their independent meanings and bounds.

The GDScript zero path keeps its previous evaluation order. Each of five existing mouth shaders retains the old seam expressions and conditionally adds the side delta only when new inputs are nonzero, with screen coordinates mapped back through rigid spread/purse width. Pigment UV, textures, owner scale, opacity, head/body transforms, central enamel attachment and existing art are unchanged. All registered oral, enamel, tongue, lip, join and inner-lip materials receive the same side vector in the existing material update pass. The extension does not claim to repair inherited bilateral+purse clipping discrepancies.

The shared public controller, timeline validator, sampling, reset/release/retrigger/handover lifecycle, viewer sliders, state and preparation-only local bridge all carry the new channels. Missing internal profile values become exact zero. Omitted manual values retain their previous value. Input rejection stays atomic. The lower-level positional set_smile_controls API takes a final optional Vector2, preserving callers' old positional semantics.

Current checks and limits are recorded in the external work directory's evidence and report. Headless tests establish numeric contracts only. Actual-render parity and source-fit static review are separate gates. No final performance, updated approval status, artwork, Git/Library publication, remote execution, network listener, CI or AI/TTS connection is included.
