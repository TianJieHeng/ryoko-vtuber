# Approved full-body rig and small bounce

The user accepted the corrected neutral pose and then approved the delivered small-bounce/jiggle preview with “nice”, under the explicit rule “if i say its good its approved”. Exact evidence, preview hashes and reviewed-source identities are recorded in [APPROVAL.json](APPROVAL.json). Approval takes effect in the containing main commit.

## Promoted scope

The separately assembled 23 body/accessory owners, 17-joint skeleton, existing live head/face integration, small manual controls and 120Hz chest/garment/pendant spring motion are promoted together. The runtime code, registration, textures, sampled geometry and both delivered MP4s remain byte-identical to review commit `a2dccc9e9179306a14d52c4df5bd3b32239089ae`. Historical review labels inside files and videos remain unchanged; this approval record supersedes their pending-review wording only for the final accepted version. Source-cut alternatives and before-images are provenance, not alternative runtime owners or approvals of rejected versions.

All 47 existing facial profiles, original face runtime, shaders, artwork, control bridge and default project entry point are unchanged. No unrelated unapproved expression or draft is imported. The full-body viewer remains an explicit scene:

```sh
godot --path ryoko_object_rig full_body/full_body_viewer.tscn
```

Use Small bounce to replay the accepted motion. It does not start automatically.

## Validation and retained limits

The accepted candidate passed 104 focused spring/runtime checks and headless viewer startup. Its existing neutral wiring baseline passed 951 focused checks. Both MP4s fully decoded; resting and motion-extreme CPU frames were visually inspected. Promotion checks source hashes and scope only, without rerunning or changing accepted motion.

The videos are CPU composites using actual Godot transforms and deformed mesh vertices, with a neutral source face. They are **not native screen captures**. Native renderer parity, continuous live pacing, tracking and export remain unverified. Approval does not erase these limitations or qualify large rotations, head yaw/pitch, or additional actions.

The existing integrity command now also checks this additive module and its exact reviewed source identity:

```sh
python -B ryoko_object_rig/tools/verify_approved_integration.py
```

Publication-only changes are current documentation/approval status, aggregate inventories and the integrity guard's additive-module scope. The prior versions of changed predecessor metadata are archived under `approval/predecessor_metadata`.
