# Approved EXP-197 and EXP-144 shared-rig integration

The user approved both completed review animations with “looks good on both”. This new note supersedes the approval-state wording in the frozen KISS_CANDIDATE.md and historical unapproved review archives; those archives are retained unchanged as evidence of their original review stage.

## Current state

- One shared registry/player contains 22 approved expression IDs: EXP-163, EXP-005, EXP-001, EXP-006, EXP-107, EXP-007, EXP-002, EXP-152, EXP-160, EXP-177, EXP-164, EXP-021, EXP-158, EXP-181, EXP-102, EXP-116, EXP-050, EXP-186, EXP-114, EXP-148, EXP-197 and EXP-144.
- Published with the containing commit at the user’s explicit request to publish now despite the unavailable visual test environment. Native visual parity is **NOT RUN**. The CUA runtime was unavailable and Xvfb was not installed. No native renderer/driver result can be claimed.
- Release metadata, source inventory and verification guard describe the current 22-profile release. The preceding twenty-profile metadata and guard are retained in historical_capture_metadata/approved20_before_pair/.

## Exact source and animation preservation

Fresh main was 13d067ccd3d226ce3cace148a074669bb905e479. Its approved tree was 8a11e99effa6e59fa7e92d76babf5d45a9e2ab67. Both archived reviews reference the verified 671-file EXP-197 dependency tree 9df08a62056614080a395c6c8442ee673fefec09. All twenty prior profiles and 182 prior PNGs remain byte-exact. All source files and historical backups remain present.

EXP-197 retains the reviewed 7.2-second keys and fixed 44x42 kiss artwork, native opacity shaders, restored oral visibility and raw repaired iris loading. Only its profile approval status changes. EXP-144 uses its exact reviewed 5.2-second keyframes in the same data-only registry/player. Its corrected shallow-mouth part, fixed [537,628] placement, upper-opening transport and positive horizontal aversion are preserved. The kiss stays invisible throughout EXP-144.

## Runtime ownership and technical handoffs

The three component channels are authored timeline channels, not unrestricted manual controls. Opening stays 0–4 pixels with centered gaze and no closure/eye-smile. Aversion stays 0–12 positive horizontal pixels, with both closures at least .18 and no ordinary gaze/down-extra/eye-smile. The shallow mouth cannot overlap open-mouth or kiss weights. Validation checks entire interpolated segments.

The public player restores temporary eye materials before committing each native pose, then applies the scoped component parts. Native mouth opacity is restored by the existing kiss mechanism before the shallow part takes ownership. Release/retrigger from a scoped pose first fades the scoped parts while retaining their valid ordinary pose; only then does it blend ordinary controls. This technically required interruption behavior is new and is not a claim of visual equivalence to an interrupted external review controller. Standalone authored timing is unchanged. Transient mesh diagnostics are cleared on restoration to avoid accumulating across repeated cycles. Aversion is applied outside assertions so it also runs in release builds.

## Checks and limits

Focused state tests cover both complete 30fps cycles, interruption/retrigger/reset, bidirectional handoffs with all 22 profiles, neutral state and manual ownership. Source/profile hashes and whole-segment rejection checks pass. The dummy renderer emits its inherited custom_samplers diagnostic; it is retained in the receipt, not treated as evidence of native GL failure or success.

The user explicitly waived waiting for native parity before publication. Native parity remains unverified. The prepared check compares 40 selected full/detail frame hashes against the exact reviewed captures, including neutral, onset, mouth transitions, hold, recovery and reset. It saves only a few stills, not a full-frame dump. This is focused qualification, not a full legacy regression suite or real-time playback measurement. EXP-142/033 and all other held proposals remain excluded. No CI, paid resources, installation, hardware flashing or remote-machine execution occurred.
