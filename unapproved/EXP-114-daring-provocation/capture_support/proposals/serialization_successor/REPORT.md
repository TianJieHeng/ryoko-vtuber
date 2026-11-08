# EXP-114 bounded-record combined native proposal

## Scope and status

Prepared offline only. The next proposed operation is ONE new full native run that can earn its own trajectory and pixel gate. The coordinator explicitly selected this route instead of repeating headless job21. Independent reviews accepted the twenty completed runtime jobs at 5,380,806 checks, plus exact prior18 parity across3,230 records including324 ordered pairs.

Failed headless job21 remains NOT_PASS. Its log reached701 checkpoints and its process exited by signal9 with an empty evidence file. This locates the interruption in final evidence production; the exact cause and OOM attribution are unproved. All original scripts, bindings, failed attempts and verifier files remain unchanged. No prior failed trajectory is copied, relabeled or used as a successful reference.

## Minimal bounded writer

The new external `trajectory_record_files.gd` preserves the complete existing checkpoint row construction, all pose/control/owner/material/texture fields, all original assertions and every frame. After each checkpoint it serializes that one full row to `records/0000.json` through `records/0700.json`, flushes and verifies the file, then retains only a small descriptor. Complete rows and their large JSON strings are released after each capture rather than accumulated for a final giant encode.

After all original final reset/neutral/count assertions, the writer rechecks all701 ordered labels, chapters, checkpoint indices, elapsed times, byte lengths and hashes, parses each complete record individually, and rejects missing or extra files. Only then can `evidence.json` declare PASS, `serialization_complete:true` and exactly701 records. A missing, truncated or failed completion manifest cannot pass the offline reader.

Actual output is proposed at `daring_provocation_performance_work/native_stream_01/`:

- `evidence.json`: original metadata plus `serialization_schema: EXP114_RECORD_FILES_V1`, completion/count fields and the ordered `record_files` descriptors.
- `records/0000.json` … `records/0700.json`: complete original checkpoint content. The fourteen held anchors retain full actual/direct owner records, not just hashes.
- `native/{label}.png`: actual1136×1384 native camera view.
- `bust/{label}.png`: actual568×800 .49 bust camera view.
- `imported_data/`: all71 actual loaded texture buffers, checked against the accepted static buffers.

## Explicit rendering-invariance replacement

The unavailable headless/native cross-run comparison is NOT claimed. Instead, every actual view retains the original exact before/after-render raw owner snapshot and public-control equality assertion. Additional per-view proof records exact-equality flags, stable scene hashes, full instance-ID scene hashes, public before/after controls and476-node counts. The verifier requires both stable hashes to equal the checkpoint's scene hash, both full instance hashes to match, and all controls to match exactly. No field is normalized to hide a difference.

All existing exact static checks remain: fourteen accepted held anchors over two natural cycles, exact public values, all direct geometry/material state, explicit six ownership strings, actual native/bust pixels, texture-buffer identity, canonical neutral pixels, camera-only presentation and fixed head/body/root transforms. All701 checkpoints and1,402 PNGs are required. This is a new actual trajectory gate, separate from the twenty accepted runtime tests. Normal-speed live observation remains a separate later check.

## Reader and tests

`record_files.py` validates the final manifest and each complete file before offering a bounded, repeatable iterator. It preserves every row/header field and rejects malformed JSON, duplicate JSON keys, nonfinite values, incorrect counts, missing/extra files, wrong order/identity, path escapes, size/hash mismatches and incomplete status. The active verifier is `verify_native_record_files.py`; the preserved original verifiers and earlier unexecuted reader draft are not called by this run.

Twenty-four offline schema tests passed, including exact round trips of all seven complete real native static records and a clearly synthetic701-record ordering fixture. Six corrupt render-proof negatives and the positive proof fixture passed. One initial negative-test fixture shared an in-memory dictionary, causing its mutation to alter both expected and actual values. That fixture-only failure is preserved; cloning through JSON now models real decoded records. No validator assertion was changed.

## Execution boundaries

`verify_native_stream_inputs.py` rechecks the original source/cache bindings, both failed attempts and independent completed-job reviews. `guard_native_stream.py` requires a fresh independent prepared approval, the coordinator's exclusive engine+display lease, no Godot process and no existing native output, and must succeed in a separate awaited call. `run_native_stream.py` runs only this new native capture, stops on first unexpected failure, and requires its own process exit0, complete manifest, every record/frame and final exact identity before writing a successful verification receipt.

Use only the frozen minimal `EXP114_NATIVE_STREAM_ONCE.sh` through supported Sky/CUA Thunar Open With Other Application, custom `/bin/sh`, Use as default OFF, one Open click. No terminal typing, alternate GUI library, default-association change or accepted/uncertain retry. No import, extra suite, production change, Git operation, display or engine action has occurred during proposal preparation.

The ordinary existing native/headless wrappers are not reused. This package does not authorize launch. Independent ready review and a separate coordinator lease remain required.
