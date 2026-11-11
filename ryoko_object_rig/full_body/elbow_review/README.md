# Neutral elbow and cuff source registration

This is an unapproved local fit candidate, built from six independent raw source owners. It is not new generated artwork, a combined fullbody texture, a gesture, or a native-render validation.

## Cause

The original registration displayed the upper sleeve's artificial dark open-tube end at the elbow. It placed the forearm's top construction cut, not its painted elbow fold, at the elbow. Consequently the upper sleeve lower fold was near canvas y498 while the forearm fold was around y598. The lower sleeve was narrower and rotated outward 14 degrees. Those misregistered bends and the exposed tube cap made the elbow look flared and detached.

## Candidate

- Upper source lower fold y780 maps to canvas y530. The last painted fold defines the cut, excluding the open tube. Original shoulder alignment remains fixed; documented rowwise fitting slopes the upper arm gently outward.
- Forearm source fold y400 maps to [354,532] / [670,532]. The original cuff-end landmark maps to wrist [325,725] / [699,725]. Independent source centerlines require rotations +8.8095 / -6.6954 degrees, horizontal scale .30 and vertical scale about .3717. The top is a rounded hidden overlap tab, drawn behind the upper sleeve.
- The gray closed cuff ellipse and lower construction rim are removed at the painted opening, using an explicit alpha cut. Each original raw hand has an absolute 10px upward underlap behind the white cuff. Its proportions, fingers and neutral angle are unchanged. The wrist bind point remains y725, inside the visible wrist.
- No jacket, head, neck, blouse, jewelry or lower-body artwork is changed. No source PNG is overwritten. Reference fullbody pixels are used only for visual landmark inspection, never as candidate art.

`registration_candidate.json` contains six replacement owners, source SHA256 values, exact cuts/warps/transforms and the two elbow joint replacements. Apply those records to the same IDs, and apply only the two supplied elbow bind changes. The candidate PNGs are individually baked registrations at scale 1, not a combined-body shortcut.

## Reproduce and inspect

Run `python ryoko_object_rig/full_body/elbow_review/build_candidate.py` from the repository root. All six candidates derive from the raw layer sources, never an installed previous candidate. The hand transform uses the original measured neutral bind with the 10px offset applied once. Before/after comparison reconstructs the original six registrations from the original upper fragment, so installing a candidate does not turn the baseline into the candidate.

Two successive builds produced identical candidate PNG hashes. Source hashes and forearm landmark transforms are checked in `validation.json`. Runtime import and the final neutral review clip are recorded separately in `../review/`. No native-render or articulation quality claim is made here.

Proof: `integrated_candidate.png`, `candidate_elbow_detail.png`, and `before_after_elbows.jpg`.
