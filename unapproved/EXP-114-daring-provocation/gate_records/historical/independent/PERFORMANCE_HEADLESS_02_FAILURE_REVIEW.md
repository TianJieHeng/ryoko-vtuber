# EXP-114 headless attempt 02: independent result

**Original jobs 8–20 PASS. Original job 21 remains NOT_PASS.** No engine, display, import or retry was performed by this review.

## Verified completed work

I independently verified each job's original number, exact command/tree/script, binding and guard hashes, zero process exit, zero-failure console summary and JSON receipt where emitted. Jobs 8–18 total 3,295,570 checks, including 1,313,935 focused EXP-114 checks. Jobs 19 and 20 are the true paired prior-18 compatibility probes, not duplicate candidate runs.

The paired files are byte-identical and decode identically across all 3,230 records. Coverage includes all 324 ordered prior-profile pairs with seven recorded bridge times each, 81 manual samples and nine sealed-width combinations, plus profile/interval/lifecycle records. Every record's state, face and material digests matches; head/body transforms remain the canonical .49 presentation. Their common SHA256 is `a4abc6496e5cafa5207156ab396342243ff9f5fabaa7a8b855098fb363e91ff9`.

These thirteen successful jobs can be reused, together with accepted jobs 1–7, while the exact scripts, source and cache remain unchanged. Across jobs 1–18 this is 5,380,806 checks, plus the two 3,230-sample parity probes. This does not include the incomplete trajectory as a success.

## Exact termination facts

The trajectory ran for 118.4915 seconds, below its 900-second timeout, and exited with -9 (SIGKILL). Its runner did not set the error/timeout termination flag. The log contains the expected 26 chapter progress messages with exact cumulative counts ending at `final_reset records=701`. No SCRIPT ERROR, ERROR or final PASS/check-count summary is present. The final `trajectory/evidence.json` exists but is zero bytes. No `HEADLESS_02_VERIFICATION.json` success receipt exists.

The source retains each full row in the `records` array. `finish()` builds the header, opens/truncates the evidence file, then calls `store_string(JSON.stringify(result,"  "))` for the entire retained graph. The zero-byte file and reached chapter logs locate the interruption in final evidence production, between file creation and a completed write. They do not instrument the exact point inside JSON conversion or prove which process sent SIGKILL. Final checks and row values cannot be accepted from the progress messages alone.

All 71 emitted imported buffers survived and exactly match their accepted static loaded hashes. They do not replace the missing 701 trajectory records. All 95 failed-attempt files, original attempt history, source/profile/runtime/cache identities and final FAIL/1 receipt have been independently checked. No Godot remained; the lease was released.

## Memory evidence and limits

Current `/proc/self/cgroup` identifies `0::/`; no cgroup mount entry is exposed. The attempted memory event/limit/current/peak and pressure paths are absent. `/proc/meminfo` and `/proc/vmstat` are readable, but are post-failure system snapshots only. The current cumulative `oom_kill` value is 7 with no before/after baseline or process-specific attribution. It does not prove this process was OOM-killed.

A serialization memory peak is plausible: the code keeps all 701 row dictionaries, including fourteen full anchor owner graphs, then allocates one aggregate JSON string. The prior static record has roughly 544 KB of actual-node data, 609 KB of direct-owner data and 39 KB of face-state JSON; those are approximate serialized data sizes, not measured peak memory for this process. The supported classification remains **signal 9 during final evidence production; exact cause unproved**.

## Narrow proposed evidence remedy

An external successor may avoid retaining the complete array and final aggregate string by serializing each unchanged checkpoint row to a separate bounded file. This is an evidence-output change only. Preserve every row field, all 701 ordered checkpoints, full anchor snapshots, public controls, face state, source-owner/material digests, imported-buffer metadata, neutral snapshots, checks, failures and all original assertions. Do not replace raw row content with hashes alone or omit difficult chapters.

Each row file must be closed, hashed and indexed with a unique path, label/chapter/checkpoint/time and byte count. The final completion manifest must be written only after final restoration/completeness assertions; it must bind all 701 records and the complete non-record metadata. A missing, duplicate, reordered, truncated, altered or extra record must fail verification. A partial output must remain clearly incomplete, never a PASS inferred from file count or progress logs. Preserve both failed attempts and their original scripts/verifiers unchanged.

## Efficiency option: one fresh native trajectory and capture run

I support a single newly reviewed native streaming run serving as both the successful trajectory gate and the actual pixel gate, rather than repeating a separate headless trajectory first. The twenty completed jobs already establish the reviewed runtime/domain/lifecycle/paired-compatibility evidence, and the existing trajectory script parsed and reached every planned checkpoint. There is no remaining safety reason requiring a second no-display pass before rendering. A native run can validate the full trajectory afresh while obtaining the requested pixels.

Conditions remain strict: preserve every original in-run assertion and full row; process all 701 checkpoints; obtain both actual camera scales; match all fourteen accepted static geometry/pixel anchors; verify exact neutral and the 71 imported buffers; and retain exact before/after-render owner-state equality for every capture. A new offline verifier must independently require the complete record set, expected control arithmetic/ownership and all existing material/geometry/pixel checks. Offline corruption/completeness tests must prove fail-closed behavior before launch.

This changes one validation comparison: there would be no claim of exact all-checkpoint equality against a successfully serialized headless run, because none exists. Its renderer-invariance purpose is instead covered by the existing exact snapshot/pose equality checks before and after each actual capture. All other original trajectory and visual gates remain. The new native run must earn its own successful exit, complete manifest and independent review; the failed job 21 never becomes a pass retroactively.

This is a proposed validation route, not execution authorization. The exact streaming successor, verifier, native wrapper/guard and binding must first be frozen and reviewed; a fresh coordinator engine/display lease is then required. No broad runtime change, extra pose, silent rerun or weakened material criterion is supported.

Detailed receipts and hashes: `PERFORMANCE_HEADLESS_02_FAILURE_REVIEW.json`. Current memory evidence: `HEADLESS_02_CURRENT_MEMORY_EVIDENCE.json`.
