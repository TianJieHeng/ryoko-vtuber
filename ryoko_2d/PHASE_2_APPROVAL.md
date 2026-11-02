# Phase 2 approval

- Neutral artwork approved by the user after PNG review.
- Both arm-to-torso background wedges are transparent.
- Alpha verification at reference coordinates `(397,500)`, `(615,500)`, `(390,540)`, and `(620,540)`: `0` at every point.
- Light preview RGB at every verification point: `(242,239,232)`, exactly the preview background.
- Dark preview RGB at every verification point: `(24,29,34)`, exactly the preview background.
- The white blouse and cuffs were not removed.
- Rebuild with `python3 ryoko_2d/tools/assemble_neutral.py` from the repository parent directory.
