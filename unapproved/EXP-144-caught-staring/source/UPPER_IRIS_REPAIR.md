# Approved upper-iris part repair

The user approved the two-part comparison before this integration. The exact reviewed textures now replace only the two active gaze iris PNGs. This is newly authored hidden upper-iris/pupil continuation, not recovered original detail. It adds no expression or eye-opening control.

## Scope and preservation

The predecessor is main f3848b3f9ebf365b144f3aadae1cd321665a10fc, whose shared rig is tree e01bda668f821c1bd57210f4eabfa5975859daa7. All twenty expression profiles and the registry, runtime code, scenes, shaders, controls, original source art, and both iris import sidecars remain byte-identical. Of 182 existing PNGs, exactly two change. No files are removed and all other repository roots, including historical backups, remain intact.

The exact reviewed pixels are reused without regeneration or additional painting. Left and right guarded masks cover 1,097 and 886 texels; 1,096 and 880 texels actually change. All alpha and every RGBA value outside those masks remain identical. The one-pixel neutral-aperture guard is untouched. The existing native review captures on this exact base prove pixel-identical centered-neutral eye and bust views. Integration rechecks those saved images and exact source identities; it does not claim a new renderer run or full twenty-expression visual regression.

## Provenance

The original generation, registered mask assembly and review are documented in the [frozen proposal backup](https://github.com/TianJieHeng/ryoko-vtuber/tree/f3848b3f9ebf365b144f3aadae1cd321665a10fc/unapproved/upper-iris-repair-proposal). That folder's unapproved label records its historical backup state and is not modified. Its two proposals are identical to the integrated active textures. Its guarded masks preserve the precise newly authored boundary. UPPER_IRIS_REPAIR.json records exact source, output and mask hashes.

## Verification and limits

Run `python -B tools/verify_approved_integration.py` and `sha256sum -c APPROVED_SOURCE_FILES.sha256` from a clean source copy. The current guard recognizes only these two approved artwork exceptions and continues enforcing unchanged profiles, registry, runtime and other artwork. Earlier validation files retain their original scope and source identities; current manifests supersede their source inventories.

The reviewed fixed 4px fixture remains a private diagnostic, not an accepted production capability. A thin protected-pixel transition and some inherited right highlight streak remain visible when enlarged. Larger openings, general gaze/blink behavior and smooth real-time pacing are not newly qualified. Previous expression holds and exclusions remain unchanged. No new engine/display run, CI, workflow, geometry, control, shader, profile, remote-machine execution, paid resource or hardware operation is part of this integration.
