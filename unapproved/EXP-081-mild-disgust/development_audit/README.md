# Development audit

The first separate Python geometry audit used a 0.00001-source-pixel threshold for Godot Vector2 translations. Nine comparisons failed because the engine stores these transform positions in single precision (for example, requested 0.3 source pixels is recorded as 0.29998779296875).

Only the translation-comparison tolerance was corrected to 0.0001 source pixels, matching the established Godot geometry checks. Rotation, control interpolation and mouth-formula tolerances were not widened. The profile, runtime and artwork were unchanged. The initial audit script and failed receipt are preserved here. The final separate audit and eleven mutation/unit tests pass.

construct_probe_scaffold.py is the historical transformation used to construct the initial probes from the established Open Sobbing pipeline. It is retained as provenance, not a supported rerun entry point. Use the final pinned scripts in the parent directory.
