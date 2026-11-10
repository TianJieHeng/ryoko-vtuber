# Approved Queasy integration

EXP-090 Queasy is the 26th user-approved performance. The user approved the exact reviewed candidate. Its 4.0-second profile bytes, timing, controls and historical preapproval metadata are preserved unchanged. RELEASE.json and APPROVED_INTEGRATION_STATUS.json record current approval. The registered alias is `queasy`; its trigger phase is neutral.

Base main: b8697a7be03f789d7e881e472acf05bb8e6fbc19. Review backup: review/exp090-queasy-v1 at 3fca7bd9f82e5d421b7173af9dff3ac8e4adc652. Profile SHA-256: 08813729222c8231500233ec6952459b6549e5fd534e87516fb1f99efa17676c. Reviewed MP4 SHA-256: 6597d8405fec550a0a9dec4b206e97608cc14a6686fd023a7a0ed928a8198e81.

All 25 prior profiles, production runtime, shaders, scenes and 184 PNGs remain byte-exact, including the approved25 shared mouth/scoped-handoff ordering repair. No runtime changes or new artwork were necessary. Previous current manifests, status, release, modified test harnesses, source guard and publication receipt are archived under historical_capture_metadata/approved25_before_queasy.

## Fresh evidence

- Production EXP-090 checks: 4665, covering all 121 chronological 30fps samples, the alias, fixed 1.3–2.0-second hold, five restart/release/reset points, exact neutral reset and bidirectional handoffs with all26 profiles.
- Prior-profile regressions: approved pair 5698, Recovering composure 2258, Sudden insight 1868, Stunned silence 2026. All passed without failures.
- Dense actual-runtime control regression: 14388661 assertions, 3327 exact standalone samples, 13832 source/target cases and 235144 transition samples. Every source key and segment midpoint is paired with every target. Sampling includes both sides of 0, 0.15 and 0.30 seconds, bounded controls, scope, sealed-mouth validity, exact old/current control equality and release to neutral. The comparison uses the unchanged approved25 runtime with the26-profile catalogue. Rendering setters are stubbed; this is control evidence, not visual parity.
- Focused native production parity: 53 checks comparing ten approved review checkpoints in bust/detail views, twenty exact RGBA pairs. The candidate review used the pre-repair runtime; this check verifies that the approved neutral-cycle appearance is unchanged with the fixed current runtime.
- Original candidate evidence: 3,536 native capture checks and 3,293 headless checks, all passing. Its review report and receipts are retained unchanged under validation/approved_queasy.

## Scope and limits

Source fidelity is partial. Existing rigid inner-brow controls do not reproduce the source's strongly curved worried brows. Cheek tension and newly painted forward lip contour are unsupported. The peak can also read as tired or pouty. Narrowed lids and the sealed pressed/pursed mouth are represented using existing controls. The four-second timeline and 0.7-second hold are authored from nine static panels, not recovered source animation. No new anatomy, head/body acting, gaze, blush, smile, auto-blink or cheek deformation was added.

Whole-rig full-trajectory native parity NOT RUN. Continuous normal-speed observation and live pacing UNVERIFIED. The inherited EXP-114 pacing HOLD and EXP-148 limits remain unchanged. The original review's cross-profile warning described the pre-repair baseline; approved25 fixed it, and this integration repeats dense all-pairs regression without changing that runtime. Inherited dummy-renderer custom_samplers diagnostics and the runtime-image import/export warning remain in raw logs. No export package was tested.

No CI, paid resources, purchases, remote-machine execution or hardware flashing. Current source checks: `python tools/verify_approved_integration.py` and `sha256sum -c APPROVED_SOURCE_FILES.sha256`. The source guard verifies inventory completeness, file hashes, predecessor preservation, exact review identity and passing validation receipts; corruption, missing-source and unexpected-source rejection are separately checked.
