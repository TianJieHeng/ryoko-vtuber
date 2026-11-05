#!/usr/bin/env python3
"""Separate ONLY the four already-complete EXP-064/EXP-189 irises.

This is an existing-art rigging derivative, not an expression generator. Run:
    python tools/build_expression_gaze_layers.py

Requires the existing Python assembly dependencies: Pillow and NumPy. The
hand-audited scanline masks below are tied to the recorded source hashes. They
retain the complete authored iris, including its antialias/sharpening fringe.
No neutral iris, hidden iris synthesis, redraw, resize or warp is used.

Only the vacated cutout is underpainted, by harmonic extension of immediately
neighboring source sclera. That hidden sclera is an estimate, not recovered art.
The fixed aperture is the cutout's 7 x 2 source-pixel sweep plus a one-texel
filter guard. All unrelated source pixels are retained. Center reconstruction
is byte-exact at source pixel centers; Godot's filtered runtime is reviewed
separately. This builder neither edits runtime code nor publishes anything.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "rig_assets/expression_gaze"
SIZE = (1136, 1384)
TRAVEL = (7, 2)
SIDE_MAP = {"screen_left": "R", "screen_right": "L"}

# Explicit, inspected contour runs: start_y followed by inclusive x intervals.
# A small original sclera fringe is retained so source antialias pixels remain
# untouched. These are four individual masks, not mirrored neutral geometry.
CONFIGS = {
    "EXP-064": {
        "screen_left": {
            "source_center_px": [491.0, 502.0], "start_y": 487,
            "runs": [
                [490,492],[487,495],[485,497],[484,498],[483,499],
                [482,500],[481,501],[480,502],[479,502],[478,503],
                [478,503],[478,504],[478,504],[477,504],[477,504],
                [477,504],[478,504],[478,504],[478,504],[478,503],
                [479,503],[479,503],[480,502],[481,501],[482,500],
                [483,499],[484,498],[485,497],[487,495],[491,492],
            ],
        },
        "screen_right": {
            "source_center_px": [646.0, 502.0], "start_y": 487,
            "runs": [
                [644,646],[641,649],[639,651],[638,652],[637,653],
                [636,654],[635,655],[634,656],[634,657],[633,657],
                [633,658],[633,658],[632,658],[632,659],[632,659],
                [632,659],[632,659],[632,658],[633,658],[633,658],
                [633,657],[634,657],[635,656],[635,655],[636,654],
                [637,653],[638,652],[640,651],[641,649],[645,646],
            ],
        },
    },
    "EXP-189": {
        "screen_left": {
            "source_center_px": [490.0, 503.0], "start_y": 487,
            "runs": [
                [490,490],[486,494],[484,496],[483,497],[482,498],
                [481,499],[480,500],[479,501],[479,501],[478,502],
                [477,502],[477,503],[477,503],[476,503],[476,504],
                [476,504],[476,504],[476,504],[477,504],[477,503],
                [477,503],[478,503],[478,502],[478,502],[479,501],
                [480,500],[481,499],[482,498],[483,497],[485,496],
                [487,494],
            ],
        },
        "screen_right": {
            "source_center_px": [647.0, 503.0], "start_y": 487,
            "runs": [
                [646,648],[643,651],[641,653],[640,654],[639,655],
                [638,656],[637,657],[636,658],[636,658],[635,659],
                [634,660],[634,660],[634,660],[633,661],[633,661],
                [633,661],[633,661],[633,661],[633,661],[634,660],
                [634,660],[634,660],[635,659],[635,659],[636,658],
                [637,657],[638,656],[639,655],[640,654],[641,652],
                [643,650],
            ],
        },
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_hashes() -> dict[str, str]:
    return {
        str(p.relative_to(ROOT)): sha256(p)
        for p in sorted(ROOT.rglob("*.png"))
        if OUT not in p.parents and ".godot" not in p.parts
    }


def bounds(mask: np.ndarray) -> list[int]:
    yy, xx = np.nonzero(mask)
    return [int(xx.min()), int(yy.min()), int(xx.max() + 1), int(yy.max() + 1)]


def shift(array: np.ndarray, dx: int, dy: int) -> np.ndarray:
    """Integer translation only; explicitly avoid wrapping and resampling."""
    result = np.zeros_like(array)
    h, w = array.shape[:2]
    sx0, sx1 = max(0, -dx), min(w, w - dx)
    sy0, sy1 = max(0, -dy), min(h, h - dy)
    result[sy0+dy:sy1+dy, sx0+dx:sx1+dx] = array[sy0:sy1, sx0:sx1]
    return result


def sweep(mask: np.ndarray, x: int, y: int) -> np.ndarray:
    result = np.zeros_like(mask)
    for dy in range(-y, y + 1):
        for dx in range(-x, x + 1):
            result |= shift(mask, dx, dy)
    return result


def make_mask(config: dict) -> np.ndarray:
    mask = np.zeros((SIZE[1], SIZE[0]), dtype=bool)
    for y, (x0, x1) in enumerate(config["runs"], config["start_y"]):
        mask[y, x0:x1+1] = True
    return mask


def underpaint(source: np.ndarray, mask: np.ndarray) -> tuple[np.ndarray, dict]:
    """Discrete harmonic extension, holding all existing sclera pixels fixed."""
    x0, y0, x1, y1 = bounds(mask)
    x0 -= 1; y0 -= 1; x1 += 1; y1 += 1
    local_mask = mask[y0:y1, x0:x1]
    patch = source[y0:y1, x0:x1, :3].astype(np.float64)
    fixed = patch.copy()
    # Only immediate known sclera neighbors supply the missing pixels.
    border = sweep(local_mask, 1, 1) & ~local_mask
    patch[local_mask] = np.mean(patch[border], axis=0)
    residual = float("inf")
    for iteration in range(10000):
        average = (patch[:-2,1:-1] + patch[2:,1:-1]
                   + patch[1:-1,:-2] + patch[1:-1,2:]) / 4.0
        update_mask = local_mask[1:-1,1:-1]
        current = patch[1:-1,1:-1]
        residual = float(np.max(np.abs(average[update_mask] - current[update_mask])))
        current[update_mask] = average[update_mask]
        if residual < 1e-7:
            break
    assert residual < 1e-7, "Underpaint did not converge."
    assert np.array_equal(patch[~local_mask], fixed[~local_mask])
    result = source.copy()
    result[y0:y1, x0:x1, :3] = np.rint(patch).clip(0, 255).astype(np.uint8)
    assert np.array_equal(result[~mask], source[~mask])
    return result, {
        "method": "harmonic extension of neighboring source sclera only",
        "iterations": iteration + 1,
        "last_rgb_update_max": residual,
        "estimated_pixels": int(mask.sum()),
        "limitation": "Occluded sclera is estimated; it is not recovered original art. A small source antialias/sclera fringe moves with the rigid iris.",
    }


def compose(registration: dict, expression: str, eyes_only: bool) -> np.ndarray:
    image = Image.open(ROOT / "artwork/bust_base.png").convert("RGBA")
    entry = registration["expressions"][expression]
    # Match the established facial assembly order: effects, eyes, rest mouth.
    patches = [] if eyes_only else list(entry.get("effects", []))
    patches += [entry["eyes"][side] for side in ("L", "R")]
    if not eyes_only:
        patches.append(entry["mouth"])
    for patch in patches:
        image.alpha_composite(Image.open(ROOT / "artwork" / patch["file"]).convert("RGBA"), tuple(patch["xy"]))
    assert image.size == SIZE
    return np.array(image)


def render(source: np.ndarray, layers: dict, dx: int, dy: int) -> np.ndarray:
    result = source.copy()
    for layer in layers.values():
        moved = shift(layer["mask"], dx, dy)
        moved_rgb = shift(source, dx, dy)
        ap = layer["aperture"]
        eye = layer["sclera"].copy()
        eye[moved, :3] = moved_rgb[moved, :3]
        result[ap, :3] = eye[ap, :3]
    return result


def font(size: int):
    path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()


def comparison_sheet(expression: str, source: np.ndarray, layers: dict, review: Path) -> None:
    # Both eyes, original lashes/brows/hair, and an unmodified source control.
    crop = (400, 440, 720, 548)
    width, row_height = 1280, 465
    sheet = Image.new("RGB", (width, row_height * 6), (28, 30, 34))
    draw = ImageDraw.Draw(sheet)
    cases = [("ORIGINAL AUTHORED SOURCE", None), ("CENTER  (0, 0)", (0, 0)),
             ("LEFT  (-7, 0)", (-7, 0)), ("RIGHT  (+7, 0)", (7, 0)),
             ("UP  (0, -2)", (0, -2)), ("DOWN  (0, +2)", (0, 2))]
    for row, (label, offset) in enumerate(cases):
        array = source if offset is None else render(source, layers, *offset)
        draw.text((12, row * row_height + 5), f"{expression}  {label}  |  4x source pixels", font=font(21), fill=(245, 245, 245))
        image = Image.fromarray(array).crop(crop).resize((1280, 432), Image.Resampling.NEAREST)
        sheet.paste(image.convert("RGB"), (0, row * row_height + 33))
        if offset is not None:
            Image.fromarray(array).save(review / f"{expression}_{label.split()[0].lower()}.png")
    sheet.save(review / f"{expression}_gaze_comparison.png")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-dir", type=Path, default=ROOT.parent / "review")
    args = parser.parse_args()
    review = args.review_dir.resolve()
    review.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    baseline_path = OUT / "source_png_sha256.json"
    baseline = json.loads(baseline_path.read_text())
    assert len(baseline) == 610, "Expected 594 original artwork plus 16 inherited rig PNGs."
    assert png_hashes() == baseline, "Inherited PNGs changed; stop and re-audit rather than adapt geometry."
    registration = json.loads((ROOT / "registration.json").read_text())
    assert registration["size"] == list(SIZE)
    assert len(registration["expressions"]) == 93
    manifest = {
        "schema_version": 1,
        "scope": "Existing-eye rigging feasibility proof; only EXP-064 and EXP-189",
        "canvas_size": list(SIZE),
        "maximum_translation_px": list(TRAVEL),
        "coordinate_convention": "screen_left is authored R; screen_right is authored L; positive y is down; bounds are [left, top, right_exclusive, bottom_exclusive]",
        "source_baseline": "rig_assets/expression_gaze/source_png_sha256.json",
        "registration_sha256": sha256(ROOT / "registration.json"),
        "rest_reconstruction": "Exact source RGBA at native pixel centers. Runtime filtering, scaling, and deformation need separate Godot review.",
        "iris_method": "Four individually inspected source cutouts, with original antialias/sclera fringe; no hidden iris synthesis, neutral substitution or distortion",
        "underpaint_limitation": "Only sclera beneath each original iris cutout is estimated from neighboring source sclera; it is not an exact recovery of hidden artwork.",
        "profiles": {},
    }
    validation = {"inherited_png_count": 610, "unchanged_inherited_pngs": True, "profiles": {}}
    for expression, configs in CONFIGS.items():
        source = compose(registration, expression, eyes_only=True)
        complete_source = compose(registration, expression, eyes_only=False)
        layers = {}
        profile = {}
        checks = {}
        total_aperture = np.zeros(source.shape[:2], dtype=bool)
        for side, config in configs.items():
            mask = make_mask(config)
            aperture = sweep(mask, TRAVEL[0]+1, TRAVEL[1]+1)
            sclera, underpaint_info = underpaint(source, mask)
            known_sclera = aperture & ~mask
            known_values = source[known_sclera, :3].astype(int)
            # Bounded rejection checks support (not replace) the visual audit:
            # all known travel-space texels must be near-white, not iris/hair,
            # lash, skin or shaded lid. No generated mask broadens this region.
            assert int(known_values.min()) >= 220, (expression, side, "unsafe dark pixel")
            assert int(np.ptp(known_values, axis=1).max()) <= 18, (expression, side, "unsafe chromatic pixel")
            assert np.array_equal(source[aperture], complete_source[aperture]), "Another expression overlay intersects the safe eye region."
            # Retain source RGB beneath a two-texel transparent color-bleed
            # guard. Bilinear samples never meet black at an alpha edge, but
            # unrelated full-bust RGB is not duplicated in these textures.
            iris = np.zeros_like(source)
            iris_bleed = sweep(mask, 2, 2)
            iris[iris_bleed, :3] = source[iris_bleed, :3]
            iris[:, :, 3] = mask.astype(np.uint8) * 255
            sclera_texture = np.zeros_like(source)
            sclera_bleed = sweep(aperture, 2, 2)
            sclera_texture[sclera_bleed, :3] = sclera[sclera_bleed, :3]
            sclera_texture[:, :, 3] = aperture.astype(np.uint8) * 255
            prefix = f"{expression}_{side}"
            paths = {kind: f"rig_assets/expression_gaze/{prefix}_{kind}.png" for kind in ("iris", "sclera", "aperture")}
            Image.fromarray(iris).save(ROOT / paths["iris"])
            Image.fromarray(sclera_texture).save(ROOT / paths["sclera"])
            Image.fromarray(aperture.astype(np.uint8) * 255).save(ROOT / paths["aperture"])
            source_patch = registration["expressions"][expression]["eyes"][SIDE_MAP[side]]
            profile[side] = dict(paths, **{
                "source_center_px": config["source_center_px"],
                "iris_bounds_px": bounds(mask),
                "aperture_bounds_px": bounds(aperture),
                "source_eye_patch": f"artwork/{source_patch['file']}",
                "source_patch_registration_xy": source_patch["xy"],
                "source_patch_sha256": sha256(ROOT / "artwork" / source_patch["file"]),
                "transparent_rgb_bleed_texels": 2,
                "underpaint": underpaint_info,
            })
            layers[side] = {"mask": mask, "aperture": aperture, "sclera": sclera}
            total_aperture |= aperture
            changed = np.any(sclera != source, axis=2)
            assert not np.any(changed & ~mask)
            assert np.array_equal(iris[mask, :3], source[mask, :3])
            yy, xx = np.nonzero(mask)
            offsets = 0
            for dy in range(-TRAVEL[1], TRAVEL[1]+1):
                for dx in range(-TRAVEL[0], TRAVEL[0]+1):
                    moved = shift(mask, dx, dy)
                    assert not np.any(moved & ~aperture)
                    assert int(moved.sum()) == int(mask.sum())
                    assert np.array_equal(shift(iris, dx, dy)[yy+dy, xx+dx], iris[yy, xx])
                    # Same displacement for every pixel, preserving all detail
                    # and pairwise distances (including both extreme diagonals).
                    shifted_points = np.column_stack((xx+dx, yy+dy))
                    points = np.column_stack((xx, yy))
                    assert np.all(shifted_points - points == [dx, dy])
                    offsets += 1
            checks[side] = {
                "restored_original_iris_texels": int(mask.sum()),
                "uniform_integer_offsets_checked": offsets,
                "iris_rgb_error_max": 0,
                "underpaint_changed_outside_cutout_pixels": 0,
                "travel_clipped_pixels": 0,
                "known_sclera_min_rgb_channel": int(known_values.min()),
                "known_sclera_max_chroma": int(np.ptp(known_values, axis=1).max()),
                "expression_fx_intersections": 0,
                "aperture_fraction_of_full_canvas": float(aperture.mean()),
            }
        reconstructed = render(source, layers, 0, 0)
        assert np.array_equal(reconstructed, source)
        for dy in range(-TRAVEL[1], TRAVEL[1]+1):
            for dx in range(-TRAVEL[0], TRAVEL[0]+1):
                moved = render(source, layers, dx, dy)
                assert np.array_equal(moved[~total_aperture], source[~total_aperture])
        checks["rest_rgba_error_max"] = 0
        checks["changed_pixels_outside_safe_eye_interiors"] = 0
        validation["profiles"][expression] = checks
        manifest["profiles"][expression] = profile
        comparison_sheet(expression, complete_source, layers, review)
        mask_view = complete_source.copy()
        for layer in layers.values():
            ap, mask = layer["aperture"], layer["mask"]
            mask_view[ap,:3] = mask_view[ap,:3] // 2 + [0,127,0]
            mask_view[mask,:3] = complete_source[mask,:3] // 2 + [127,0,0]
        Image.fromarray(mask_view).crop((400,440,720,548)).resize((1280,432), Image.Resampling.NEAREST).save(review / f"{expression}_safe_masks.png")
    assert png_hashes() == baseline, "Builder changed inherited artwork."
    validation["new_texture_count"] = 12
    validation["runtime_review"] = "Pending separate actual Godot MP4 review; CPU checks do not claim runtime visual approval."
    (OUT / "profiles.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (review / "expression_gaze_validation.json").write_text(json.dumps(validation, indent=2) + "\n")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
