#!/usr/bin/env python3
"""Compare real Godot readbacks, not transformation matrices or mock renders."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("captures", type=Path)
parser.add_argument("--reference", type=Path, help="Optional original-source Godot legacy_rest.png from the frozen checkpoint")
args = parser.parse_args()
root = args.captures.resolve()
metadata = json.loads((root / "captures.json").read_text())
assert metadata["expression"] == "EXP-005", "This independent ROI audit is scoped to EXP-005 only"

def image(path):
    out = np.asarray(Image.open(path).convert("RGBA"))
    assert out.shape == (1384, 1136, 4), "Only unscaled native source-resolution Godot captures are accepted"
    return out

legacy = image(root / "legacy_rest.png")
rest = image(root / "articulated_rest.png")
# Fixed, independently inspected source coordinates. These do not derive from
# a candidate's mask, so a wrongly broad cutout cannot expand its own test ROI.
oral_roi = [492, 578, 644, 700]
nose_roi = [530, 540, 606, 586]
jaw_roi = [430, 700, 710, 755]
outside = np.ones(legacy.shape[:2], dtype=bool)
x0, y0, x1, y1 = oral_roi
outside[y0:y1, x0:x1] = False
guards = {"nose": nose_roi, "jaw_chin": jaw_roi}
records = []
failures = []
extreme_failures = []
unique_timeline = set()
rest_exact = bool(np.array_equal(legacy, rest))
if not rest_exact:
    failures.append("Undeformed articulated composite differs from original-source legacy render")
reference_exact = None
if args.reference:
    reference_exact = bool(np.array_equal(legacy, image(args.reference)))
    if not reference_exact:
        failures.append("Candidate legacy render differs from frozen original-source Godot reference")

for entry in metadata["frames"]:
    pixels = image(root / entry["file"])
    delta = np.max(np.abs(pixels.astype(np.int16) - legacy.astype(np.int16)), axis=2)
    changed = delta > 0
    outside_count = int(np.count_nonzero(changed & outside))
    guard_counts = {}
    for name, (gx0, gy0, gx1, gy1) in guards.items():
        guard_counts[name] = int(np.count_nonzero(changed[gy0:gy1, gx0:gx1]))
    authored = entry["time"] >= 0 or (-0.850001 <= entry["opening"] <= 0.240001 and -0.100001 <= entry["width"] <= 0.180001 and 0 <= entry.get("curve", 0) <= 0.180001 and not any(entry.get("shift", [0, 0])))
    if outside_count or any(guard_counts.values()):
        error = f"{entry['file']}: outside oral ROI={outside_count}, protected pixels={guard_counts}"
        (failures if authored else extreme_failures).append(error)
    count = int(np.count_nonzero(changed[y0:y1, x0:x1]))
    if entry["time"] >= 0:
        unique_timeline.add(hashlib.sha256(pixels[y0:y1, x0:x1].tobytes()).hexdigest())
    # The original laughter artwork is already maximally open. Positive-only
    # opening may legitimately clamp at the source peak; closure or width
    # changes must still produce actual pixels, never silently pass as static.
    if authored and not entry["legacy"] and (entry["opening"] < -0.05 or abs(entry["width"]) > 0.05 or abs(entry.get("curve", 0)) > 0.05) and count < 25:
        failures.append(f"{entry['file']}: no meaningful rendered oral movement ({count} changed mouth pixels)")
    ys, xs = np.nonzero(changed)
    bbox = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1] if len(xs) else None
    records.append({**entry, "authored_envelope": authored, "changed_mouth_pixels": count, "changed_outside_mouth_pixels": outside_count, "protected_pixel_changes": guard_counts, "all_changed_bbox": bbox, "max_channel_delta": int(delta.max())})

if metadata.get("full_timeline", True) and len(unique_timeline) < 20:
    failures.append(f"Full mouth timeline has only {len(unique_timeline)} distinct rendered oral frames; static faces are not completion")
result = {
    "passed_authored_envelope": not failures,
    "authored_failures": failures,
    "extreme_api_failures": extreme_failures,
    "rest_composite_exact": rest_exact,
    "original_source_reference_exact": reference_exact,
    "oral_roi": oral_roi,
    "protected_regions": guards,
    "frame_count": len(records),
    "unique_rendered_mouth_timeline_frames": len(unique_timeline),
    "source": metadata["kind"],
    "scope": metadata["scope"],
    "limits": "Pixel stability and real oral movement do not by themselves establish good closure anatomy, preserved teeth/tongue shape, or expression readability; inspect captures/video too.",
    "frames": records,
}
(root / "pixel_qa.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "frames"}, indent=2))
raise SystemExit(0 if not failures else 1)
