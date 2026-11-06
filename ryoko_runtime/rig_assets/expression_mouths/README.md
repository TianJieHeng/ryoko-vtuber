# EXP-005 isolated oral features

Only hearty laughter (EXP-005) is included and enabled for performance playback. The user approved its actual runtime video; no other performance is approved by this release. Original artwork is unchanged.

## Composition

Read `manifest.json`. The cleared patch preserves every source byte outside the oral mask, and preserves original alpha everywhere. Only 9,406 RGB pixels inside the reviewed mask are estimated by harmonic extension from neighboring skin. `EXP-005_estimated_mask.png` identifies every estimated pixel. Jaw and nose are outside this mask.

The oral feature contains original RGB with hard alpha inside the mask and nearest oral RGB bleed outside it. Compose:

    result.rgb = mix(cleared.rgb, moved_feature.rgb, moved_feature.a)
    result.a = original_mouth.a

The optional coverage PNG is grayscale; sample its red channel. It is identical to original mouth alpha. Do not use ordinary alpha-over between the two already-feathered patch assets. That would double alpha at feathered oral pixels.

Pivot is local (90.5, 62), registered origin is (477, 576), patch size is 178 by 130. The production controller clamps vertical scale to [0.10, 1.0] and horizontal scale to [0.82, 1.16]. The image-space generator diagnostics sample Y 0.235/0.6/1.0 and X 0.82/1.0/1.18; the separate actual-Godot pixel gate covers all authored timeline values and extreme controls. Full original scale is already the authored maximum laugh. Centered vertical stretching beyond 1 moves upper lip into the protected nose region. Do not trim the real upper lip to work around that constraint.

At exact rest, RGB/alpha recomposition is byte-exact to original source, including 482 feathered oral-mask pixels. A direct original-texture render is also appropriate at exact rest.

## Evidence

- `contact_sheet.png`: original, cleared, isolated feature, closed, half, rest. Composites use the actual bust base and the formula above.
- `geometry_guard_contact.png`: nine requested image-space combinations of Y 0.235/0.6/1.0 and X 0.82/1.0/1.18.
- `geometry_guard_checks.json`: all nine combinations preserve nose [530,540,606,586], jaw y>=700, and every pixel outside oral ROI [492,578,644,700]. Bilinear filtering; zero changed guard pixels.
- `validation.json`: exact outside-mask preservation, exact rest RGBA, exact rest composite over base, exact feature RGB, immutable source.
- `source_baseline_verification.json`: original mouth and bust base hashes match the approved performance-preset baseline.

Regenerate with `python tools/build_performance_mouth_layers.py`. Python compilation passes. These generator checks are image-space tests. Actual Godot render validation, accepted-video provenance, and remaining playback limits are recorded in ../../VALIDATION_EXP005_RELEASE.md.

A transparent oral hole was rejected: the underlying bust base exposes a hidden nose tip and different skin shading through the original mouth patch. Harmonic underpaint avoids that visible seam.
