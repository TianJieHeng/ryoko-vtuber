# EXP-050 independent performance pre-capture review

## Decision

**PASS for the exact proposed actual-render capture.** This is not actual-performance acceptance, user approval, publication approval or approval of any predecessor profile. No display was used by the reviewer.

- Performance source freeze: `c2f4d0ff703f9caf418bf2a72ff117a294730a75f0be2ae3de4ba9c24577fd8a`.
- Capture plan: `9b3bfb0991d6bfe87438eb4da006e1832ed3e2161a3a35bfc902b8473dfb1e6e`.
- Capture input binding: `a0d25e0b909a19f2a21c8714726858a8b431c001b7c0e2940cc37ec6efc0a031`.
- EXP-050 profile: `e1b775d34244bf1a1f05fac351170062657b0b12d11acf2edf08bf8f3ec9e630`.

The proposed run has 18 chapters and 541 checkpoints, each captured in full 568×800 presentation and native 1136×1384 presentation: 1,082 real viewport images. The existing shared player drives every state. Reference pictures are not runtime face art. The runner requires a separate parent display lease and refuses an already-attempted run.

## Authored acting and accepted anchors

The nine authored keys are literal accepted combined static vectors or duplicate holds, not refinements:

- 0.00: KP1 neutral.
- 0.73: KP3 gathering.
- 1.57 and 1.99: exact KP5 peak, held for 0.42 seconds.
- 2.34 and 2.65: exact KP6 sustained pose, held for 0.31 seconds.
- 3.22: KP7 broader non-smiling release.
- 3.91 and 4.13: exact KP9 neutral, held for 0.22 seconds.

This distinct 4.13-second timing is clearly identified as newly authored interpretation of still panels. The source's proposed 1.9-second timing is not recovered animation. KP2/4/8 are represented by the unchanged smoothstep progression between accepted anchors, not additional fitted poses. Purse gathers monotonically through the peak and then holds/eases; no smiling release or oral opening is authored.

The old 0.30-second trigger bridge attenuates initial gathering from neutral, and its behavior is included in expected states. For example, purse is approximately 0.0273285 at 0.15 seconds and 0.1839251 at 0.30 seconds. The bridge has finished before the first nonzero accepted anchor at 0.73 seconds. All nonzero anchor vectors remain exact. Exact neutral **pose** begins at 3.91 seconds, while the player remains active until 4.13 seconds; pending auto-blink restores only after completion. The inherited 0.45-second release is unchanged.

The static acceptance's canonical interpretation limits remain: smoother/rounder mouth contour rather than the source's flatter-center/pinched ends, weaker localized brow knit and a less sharply intense peak. The prior component-only whole-face HOLD was superseded by actual combined-pose evidence, without changing values. Nothing in this performance preparation silently upgrades the static conclusion to a temporal one.

## Scope and preservation

The exact 605-file input source remains unchanged. The delivery has 616 frozen payload files plus its freeze receipt, 617 files total, with the same 182 PNGs and 17 registered profiles.

The only inherited change is appending EXP-050 to `expressions/registry.json`. All first sixteen entries are structurally exact, and all sixteen old profile files and their status strings, runtime, shaders, scenes and art remain byte-identical. The new status sidecar preserves the previous approved/unapproved ID lists and adds only unapproved EXP-050. No runtime field, control bound, artwork, opacity, UV, owner scale or shape was changed.

The eleven new payload files are the local profile/status/documentation, accepted-source/anchor/prior-registry evidence, new tests and capture helper with their two UIDs, and a portable scope verifier. Generated inherited UID/import files are excluded from the clean delivery. Earlier unreviewed packaging and unfrozen-preflight history was not counted as final evidence.

## Independent checks

- `audit_pre_capture.py` compared every key to the pinned accepted union and independently recomputed sampler, trigger, release and mouth-bridge arithmetic for all 541 planned receipt states. Maximum control discrepancy was about 2.94×10⁻⁸, consistent with recorded float32 channels. Every natural unused channel is zero; positive width/open overlap is absent.
- All 140 common natural-cycle states match exactly, including ownership, phase and bridge metadata. Natural neutral holds, completion, manual ownership, release/retrigger/reset and blink suspension/restoration expectations were checked.
- The actual baseline and candidate parity JSON files are byte-identical, not merely reported similar. They contain 2,661 records covering all sixteen old profiles, fixed head/body transforms, controller/face/material state and 1,792 checkpoints over all 256 ordered old-profile pairs. This is state/material parity, not a claim that all old-profile pixels were newly rendered.
- A fresh independent copy of the import-free 617-file delivery passed headless import, all **1,151,389 runtime checks**, and the exact **359,370-check capture preflight**. The fresh preflight receipt is byte-identical to the builder's final receipt. All 617 protected payload files remained unchanged.
- All 31 files and external evidence references in the final capture binding were independently hashed. The static review remains pinned and unchanged. No capture-attempt marker existed at readiness review.

These checks cover bounds/default zeros, dense near-zero purse activation/recovery, held anchors, repeated 30/60 Hz cycles, lifecycle at multiple phases and both blink intents, incoming/outgoing prior profiles, dense strong open/width handovers and reversals, large steps, invalid-input atomicity, registry rejection atomicity, fixed anatomy/UV/modulation and exact reset. Tests do not establish image quality merely by having a large assertion count.

## Actual-render review still required

The frozen actual plan specifically covers natural progression and epsilon purse activation/recovery, two repeated cycles, release/repeated release, retrigger/interrupted release, EXP-005 open-mouth handovers, EXP-116 sealed-width handovers and active-width reversals, manual takeover, reset and visible blink suspension/restoration. Incoming legacy open-mouth mixing can temporarily combine purse with opening, and width-involved transitions use the unchanged bounded-direct bridge. Those integration pixels must be inspected, not inferred safe from headless arithmetic. Using unapproved EXP-116 for a test does not approve it.

Actual review must verify every image/hash/state receipt, native equality to all accepted static anchors and duplicate holds, exact neutral endpoints and repeated-cycle equality, confinement of natural changes to the intended components, and visible continuity/seam behavior. Timing/pacing and acting must be judged from the resulting trajectory. No normal-speed live playback, socket test, AI/TTS connection or final media readiness has been observed or claimed.

## Evidence

- `evidence/BASELINE_AND_STATIC_PIN.json`: immutable baseline and previous static acceptance.
- `evidence/INPUT_AND_TRAJECTORY_AUDIT.json`: independent anchor, arithmetic, cycle and parity checks.
- `evidence/COLD_CHECKS.json`, `evidence/COLD_RUNTIME.json`, `cold_preflight/evidence.json`: independent cold execution.
- `evidence/FINAL_BINDING_AUDIT.json`: exact final input binding.
- `audit_pre_capture.py` and `run_cold_checks.py`: reproducible independent checks.

No graphical display, capability change, publication, Library write, CI, paid resource, hardware action or remote execution occurred in this review.
