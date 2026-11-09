# Hidden canonical iris support and bounded downward gaze

Eight user-approved performances share one rig: EXP-163/005/001/006/107/007/002/152. EXP-002 is preserved from published commit 9b10e2f2c70f19fa003169502a73ee935af55480; EXP-152 includes the approved hidden-iris/down-gaze prerequisite. EXP-003/160/177 and new brow channels are excluded. See MERGED_PUBLICATION_VALIDATION.md for exact scope, source identities and focused merge checks. Earlier stage descriptions and frozen review receipts are historical.

## Artwork and provenance

The canonical flattened bust, original assembly layers, observed iris/pupil/highlight material, registration and stationary sclera remain unchanged. The assembly-pack iris drawings differ from the canonical likeness and were not substituted. The prior generic upper caps were not treated as completed merely because they had color.

A built-in imagegen edit produced a donor for the missing hidden upper pigment. Its exact prompt, original input/donor hashes, dimensions and crop registration are in source_references/hidden_iris_generation_prompt.txt and hidden_iris_cap_patch.json. Only 155 screen-left and 132 screen-right RGB texels are retained. Generated alpha and all generated lower/core pigment are discarded. New pixels are explicitly inferred art, not recovered original layers. The compact registered RGB patch is durable source; tools/complete_hidden_iris.py reproduces the exact runtime files after the original assembly builder.

Thirty left and 25 right newly reached perimeter texels keep the already inferred, canonical measured dark-ring RGB [55,29,17] and existing ellipse alpha. No ring shape changes. The completion additions total 185/157 nonzero texels. Farther unsupported cap material remains unverified and cannot justify a larger bound.

## Preservation and support boundary

The full old physical rectangle x[-4,4], y[-2,1] is enlarged by continuous bilinear tent support and intersected with the stationary aperture/lid profiles. Every channel in all 2655/2262 reachable texture texels is locked, including 1405/1094 alpha-zero texels. Their ordered RGBA hashes remain exact. The entire iris alpha planes, dimensions and import settings remain exact.

The new physical rectangle x[-4,4], y[-2,6] is covered by observed material, prior completed support, the explicit new strip and retained dark perimeter. The 12/11 newly reached transparent edge texels that can share a bilinear cell with positive alpha also remain unchanged RGB [55,29,17]. Other transparent texels cannot influence a positive-alpha bilinear sample. This explicitly covers straight-RGBA color filtering, not just alpha-positive texels. Imports use lossless texture data, no alpha-border RGB rewrite, no premultiplication and no mipmaps.

Open ordinary lids give maximal fixed-q support. Closing ordinary lids, smile masks and foreground hair only reduce it, so the proof does not assume their occlusion. Shaders, aperture/profiles, sclera, lashes, lower contours and hair are byte-identical to main. Dynamic UVs, feature scaling, mesh deformation, head pitch and anatomical opacity blending are absent.

## Controller contract

Old normalized gaze semantics remain exact. The optional default-zero gaze_down_extra [0,1] adds 5 source pixels to the old vertical offset. The one iris owner receives the sum; dx and all other bounds remain unchanged. Mixed up+extra inputs are additive and bounded. Validator, sampler, displayed state, reset/retrigger/release, viewer and preparation-only adapter share this field. Existing payloads gain an additive field in returned state/capabilities; whole serialized responses are not claimed byte-identical.

Existing mouth 0.55 physical factor, 30.8-pixel aperture cap and fixed white upper teeth are protected. Six existing profile JSONs remain byte-identical. No new performance is registered.

## Readability selection and evidence

Real Godot 4.6.3/OpenGL Compatibility rendered whole-bust comparisons at actual 0.49 scale. Down 2 was too subtle, down 4 borderline and down 5 transitional. Down 6 was the smallest tested integer extent independently judged a clear downward glance with matched 0.12/0.22 ordinary lids. Down 8 was unnecessary and was trimmed out of the final candidate. The selected maximum is 2.94 viewer pixels; a nonzero offset or magnified crop alone was not accepted as evidence.

Final capture and independent-review receipts are supplied separately with this local candidate. They distinguish continuous source proof, finite actual-render regressions and visual judgments. The 12-second synthetic capability movie shows gaze trajectories and mask combinations, not private-pride acting. Normal-speed playback observation is not claimed. Those historical receipts did not imply approval or publication. The user has since approved this prerequisite with EXP-152. No CI, paid resource, remote execution, hardware flashing, model/TTS or listening-socket work is included.

## Executed validation

The final source passed 20 actual Godot runtime suites, including the new 581,455-check downward-extension contract and the existing 1,757,314-check gaze contract. The originally mistyped closed-smile test name was not counted as a pass; the actual closed-smile contract was run successfully. Existing real-socket transport was not run.

Fresh parent/candidate captures produced 534 paired old-domain frames across native and 0.49 viewer scale, with identical RGBA, all old state fields and all old face snapshot fields. The new field was explicitly zero. At each scale, 195 new-domain states included 25 exact fractional reversal pairs and 12 identical iris-hidden backing samples. Neutral return was exact. The 360-frame capability trajectory repeats the same descent exactly and keeps tested gaze-only changes inside the eye region. Source coverage is continuous; these render tests are finite samples, not exhaustive continuous rendering.

The 12-second, 30 fps review MP4 fully decodes to 360 frames. Its whole-bust view is at actual 0.49 scale and its eye crop is labeled magnification. The original source panels are acting references, not a claim that an EXP-152 performance was built.
