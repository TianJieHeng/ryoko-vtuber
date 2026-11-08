# White teeth and reference-limited mouth

## Requested change

The user requested white teeth and a maximum opening no wider than their attached screenshot. The actual screenshot was materialized and viewed before implementation. Its SHA256 is 27251922a6834aaf65a7d1da787bba89621ea63643f8eea68627a64570cf9a77.

Fixed nose/jaw/face landmarks align the screenshot to the native source at approximately 0.792 scale. Independent measurement agrees. The screenshot dark aperture occupies roughly x330–379, y428–452. Comparing actual baseline Godot sweep frames at that facial scale selects a conservative effective aperture cap of 0.55. Whole-mouth RGB similarity alone is not used as a hard constraint because it is affected by screenshot compression and the fuller canonical lip artwork.

## Exact implementation

The public continuous control remains normalized 0–1. Every call to the face's continuous opening function maps it to effective opening 0–0.55. Existing rigid translation and alpha-only aperture formulas are evaluated at this effective value. Maximum central aperture height is 56 × 0.55 = 30.8 source pixels; maximum lower-lip translation is 54 × 0.55 = 29.7 pixels. At the screenshot scale this is about 24.4 pixels of aperture. Upper lip and upper teeth stay fixed, with teeth at (533,626).

This is a bound on articulation, not compressed geometry. The existing neutral mouth, all seven independent oral objects, source proportions, spatial masks and identity UV stay intact. Timeline beat times, cycle duration, eyes, brows and hair are unchanged. Continuous manual takeover, normal playback, release and retrigger share the same final mapping. Legacy A/E/I/O/U and viseme aliases are explicitly rejected by yawn_rig, including M's A request, because those unapproved independent drawings could exceed the requested maximum. REST and the continuous neutral path remain available.

Only upper_teeth.png and lower_teeth.png in rig_assets/yawn_mouth change their RGB pixels. Source assembly originals remain immutable. Static tooth derivative color is computed as neutral R=G=B=round(clamp(135+0.5×Rec.709 source luminance,0,255)); alpha, size, placement and tooth boundaries remain unchanged. Opaque crown medians are 250 and 246, with soft neutral shading and visible divisions retained. No new tooth shapes are drawn and no animation-dependent whitening occurs.

## Preserved identity and scope

All 268 other existing PNGs are byte-identical to the preceding teeth-registration release. Original fuller lips, visible head, eyes, brows, nose, jaw, connected neck, hair and torso are unchanged. This does not make the earlier flattened source magically complete: the prior bounded hidden-skin/crossing/hair estimates remain documented. Earrings stay static. Hair remains limited to ±0.07 and gaze centered. Other 92 expression performances are unsupported. No repository push or CI was performed, and user approval remains pending.

See VALIDATION.md for source, actual-engine, visual and packaging evidence. Frame-by-frame inspection is not a claim of normal-speed native playback.
