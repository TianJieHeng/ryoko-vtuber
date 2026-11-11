# Jacket source-part registration candidate

Unapproved jacket correction integrated through the full-body manifest builder. The source builder writes only these derived parts and proof files; the assembly builder applies the seven owner records. No new action sequence or approved/main update is included.

## Inspect

- `integrated_candidate.png`: complete neutral assembly on light background.
- `integrated_candidate_dark.png`: same assembly on dark background.
- `jacket_detail.png`: crop of that exact integrated frame.
- `registration_candidate.json`: seven explicit replacement/additional owners, including source hashes, positions, scale, ordering and cut metadata.
- `validation.json`: narrow ownership/provenance checks. This is not native-render or motion certification.

Run `python ryoko_object_rig/full_body/jacket_review/build_candidate.py` from the repository root. The script derives jacket, blouse, belt and pelvis masks directly from retained raw source PNGs. Current registration and neutral transform samples are used only to render unaffected background owners. Already-installed overrides are excluded before the candidate owners are drawn, so integration does not cause duplicate collar/button rendering or repeated cutting.

## Defect and correction

The earlier registration displayed the detached fronts' broad inner-facing strips as outer lapels. Their straight inner edges created the high black collar and narrow opening; the blouse collar tabs were behind those strips. The panels also ended near y650, making the hem read as a short flare.

Each front is now isolated along its painted lapel-fold seam, including the continuous lower front edge. The excluded inner-facing/underlap pixels are retained in `blazer_*_facing_not_instantiated.png` for audit and are not put into the visible rig. The exterior cutouts are registered using named silhouette/fold and vertical garment landmarks. The target opening is rounded through the bust and closes at the waist; the fitted hem reaches y689. This is a documented source-pixel deformation, not copied reference artwork. L and R use their own painted sources; only target silhouette coordinates are symmetric.

Two collar tabs are cut from the original blouse, removed from the rear blouse, kept at their original registered coordinates, and baked as integer-position scale-1 front owners. The full original button is an independent chest-mounted fastener, with the same source pixels removed from the visible jacket front. The blouse's untucked lower side excess is masked inside the fitted jacket outline. Only belt strap outside the raw-derived pelvis silhouette is masked, with the original gold buckle alpha and centered position preserved.

The canonical full-body reference supplies alignment/silhouette observations only. No reference/full-body/bust pixels are instantiated. The existing head stays at scale .32 and [329,4]; neck, sleeves, hands and lower-body owners are unchanged by these records.

## Integration contract

Replace existing ids `blazer_R`, `blazer_L`, `blouse`, `belt`. Add `blouse_collar_R`, `blouse_collar_L`, `blazer_button`. `file` paths are relative to `ryoko_object_rig`; add `res://` when writing the runtime manifest. Position is final canvas bind top-left, scale and rotation are explicit; do not recompute a legacy pivot offset. All are chest children except the pelvis-mounted belt. Preserve the recorded z values. Source extraction/affine metadata is provenance, not a request for runtime shear.

The neutral proof is a CPU layer composite with the retained neutral head source, not native facial-shader output. These corrections do not certify large motions or imply user approval.
