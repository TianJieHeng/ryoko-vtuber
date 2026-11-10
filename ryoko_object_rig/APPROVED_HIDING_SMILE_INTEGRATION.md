# Approved Hiding a Smile integration

EXP-153 Hiding a Smile is the 27th user-approved performance. The user approved the exact reviewed candidate. Its 4.0-second profile bytes, timing, controls and historical preapproval metadata are preserved unchanged. RELEASE.json and APPROVED_INTEGRATION_STATUS.json record current approval. The registered alias is `hiding_a_smile`; its trigger phase is neutral.

Base main: 2663835145ca90bb1125803a05363f257034de9f. Review backup: review/exp153-hiding-a-smile-v1 at 8892bc6e7a7734e3f4d12592b09bf44765058234. Profile SHA-256: 8a6b61f41a7d6e619f7bcbee188008d5c454cb2295e2c22460829c40f1b87b76. Reviewed MP4 SHA-256: 9642f1afbef44680cc81b2a32a8c49d00a7b6c87f6ba266f39a4f44bf0addfbd.

All 26 prior profiles, production runtime, shaders, scenes and 184 PNGs remain byte-exact, including the shared mouth/scoped-handoff ordering repair. No runtime changes or new artwork were necessary. Previous current manifests, status, release, modified test harnesses, source guard and publication receipt are archived under historical_capture_metadata/approved26_before_hiding_smile.

## Fresh evidence

- Production EXP-153 checks: 4716, covering all 121 chronological 30fps samples, the alias, fixed 1.4–2.05-second hold, five restart/release/reset points, exact neutral reset and bidirectional handoffs with all 27 profiles.
- Prior-profile regressions: approved pair 5834, Recovering Composure 2308, Sudden Insight 1918, Stunned Silence 2078, Queasy 4717. All passed without failures.
- Dense actual-runtime control regression: 15419433 assertions, 3457 exact standalone samples, 14823 source/target cases and 251991 transition samples. Every source key and segment midpoint is paired with every target. Sampling includes both sides of 0, 0.15 and 0.30 seconds, bounded controls, scope, sealed-mouth validity, exact old/current control equality and release to neutral. The comparison uses the unchanged approved26 runtime with the 27-profile catalogue. Rendering setters are stubbed; this is control evidence, not visual parity.
- Focused native production parity: 53 checks comparing ten approved review checkpoints in bust/detail views, twenty exact RGBA pairs. This verifies that the approved neutral-cycle appearance is unchanged in the production registry.
- Original candidate evidence: 3,536 native capture checks and 3,293 headless checks, all passing. The original review report and receipts retain their historical preapproval scope under validation/approved_hiding_smile.

## Scope and limits

Source fidelity is partial. Ordinary upper-lid narrowing approximates the source's open-eye lower-lid crinkle; the peak can read as a relaxed or knowing half-lidded smile. Rigid brow controls and existing lip pressure do not reproduce the exact painted brow curvature or compressed lip contour. The shared controls provide a small sealed smile without new artwork or anatomy. Existing outer eyelid/hair edge fragments remain a local polish limitation. The four-second timeline and 0.65-second hold are authored from nine static panels, not recovered source animation. No new head/body acting, gaze, blush, automatic blink or mouth opening was added.

Whole-rig full-trajectory native parity NOT RUN. Continuous normal-speed observation and live pacing UNVERIFIED. The inherited EXP-114 pacing HOLD and EXP-148 limits remain unchanged. Inherited dummy-renderer custom_samplers diagnostics and the runtime-image import/export warning remain in raw logs. No export package was tested.

No CI, paid resources, purchases, remote-machine execution or hardware flashing. Current source checks: `python tools/verify_approved_integration.py` and `sha256sum -c APPROVED_SOURCE_FILES.sha256`. The source guard verifies inventory completeness, file hashes, predecessor preservation, exact review identity and passing validation receipts; corruption, missing-source and unexpected-source rejection are separately checked.
