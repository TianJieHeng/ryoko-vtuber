# Bounded headless compatibility evidence

The package source remains the exact historical seven-profile candidate. This assessment used a clean scratch copy of sibling `EXP-116-confident-denial/source` (inventory 95fa422e615d63ec0226f6cf84097acc1d78837486478b0fb08dbb62f69c9783), added only the exact EXP-003 profile and its registry entry, and ran the included assessment harnesses. The current source is not shipped a second time.

`assessment_probe.gd` was run with Godot 4.6.3 headless against both copied projects. It writes one JSON record per line to the path supplied after `--`. The files were named `historical_samples.jsonl` and `current_samples.jsonl`. `compare_samples.py` compares those files beside itself. Raw samples are excluded; their hashes are in the comparison result. All 640 historical-field comparisons are exact, not tolerance-based. Current-only fields are separately listed. Texture resource paths and UV match, but four source PNG bytes differ; this is not pixel parity.

Only expected catalogue lists/counts are adapted in the contentment, blink and sealed-width assessment harnesses. The sealed-width harness requires the unchanged `sealed_observed_rig.gd` beside it from the current common source. No production source, profile value, artwork, geometry or shader is edited. These are local test instructions, not permission to change the approved project.

No current display replay is included. Use a separate bounded render plan before claiming current visual compatibility.
