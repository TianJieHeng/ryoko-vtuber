# EXP-114 normal-playback routing successor

Unbound offline proposal only. No normal-stage launch or lease has been granted.

The existing normal-playback GDScript is unchanged in source and runtime. It runs two 3.80-second cycles at the actual .49 bust camera and two at the actual native camera, advancing the public API with measured wall-clock frame deltas. All existing readiness, fixed-transform, exact canonical-neutral and final restoration assertions remain unchanged. Production source, profile, pose values, cache and current native-stream package are untouched.

The copied external runner is restricted to the normal stage. Its stage body and assertions are unchanged. Only its binding/guard/review/lease routes select this new successor. The final receipt additionally sets status and returncode after post-identity verification, preserving the existing failure rather than allowing an inconsistent numeric returncode. It also fails closed if a Godot process remains instead of accepting an unreleased lease. The obsolete guard requirement for a successful headless trajectory is replaced by exact binding to the successful combined native-stream run, its complete manifest, 701 record files, 1,402 actual camera images, final verifier and all attempt artifacts. Failed headless job21 remains NOT_PASS.

The final freeze is intentionally unavailable until the current native-stream run has exited successfully and produced its own final verification. A separate independent readiness review, fresh coordinator engine/display lease, separate guard PASS, and ONE supported Thunar custom /bin/sh launch with Use as default OFF are required. The old wrappers, guards and runner remain preserved and inactive.

This stage provides actual real-time execution and frame-pacing evidence. It does not by itself establish continuous normal-speed visual observation. Supported CUA observations, if obtained, must be recorded accurately and separately; no continuous observation claim is inferred from elapsed time, process success or the frame sequence.
