# EXP-091 Overly Sweet Taste: technical preview QA

Status: MP4 ready for review; UNAPPROVED. Technical capture/encoding validation passes using supplemental validator v2. Source fit does not pass on this evidence.

## Deliverable
- Path: /workspace/scratch/42f2baf55663/ryoko_native_editor_attempts_20261111/EXP-091-editor-attempt-02/Overly_sweet_taste_reconstruction_20261111_r1_review.mp4
- SHA-256: 035ed33369ba957d2e2c1275cee377b0f9a21d3b6b2c529ea88592dbddfb4d19
- Size: 225487 bytes.
- H.264 High, yuv420p, 968 × 800 displayed pixels, 30/1 fps, 121 frames, 4.033333 seconds; silent video.

## Validation and preserved lineage
The original unchanged preflight exited 2 because Python exact floating-point equality rejected 80 Godot JSON timestamp representations. Largest error was 3.552713678800501e-15 seconds. Its failure and original validator are preserved. Supplemental EXP091_validator_v2.py changes timestamp comparison to finite numeric values with absolute tolerance 1e-12 seconds and requires an actual integer frame index. It imports the original frozen numeric_model through an explicit path; all other capture, metadata, pose, lifecycle, hash, PNG CRC, dimensions, chronology, neutral-pixel and no-overwrite checks remain unchanged. The tolerance is far below a frame interval and is not a timing correction to the raw evidence. Original/derived SHA and exact diff are recorded in EXP091_validator_v2_lineage.json and EXP091_validator_v2.diff.

All 13 mutation tests passed, including malformed/nonfinite timestamps, reordered/duplicated/missing frame records, time changes beyond tolerance, stale freeze/profile/frame hashes, native pose corruption and failed runtime status. Full supplemental preflight passed all 260 PNG checks and emitted the same ffmpeg command. That exact command then encoded successfully, without a renderer launch. Post-encode freeze verification passed for 1175 pinned files. No frozen file or raw receipt was modified.

ffprobe counted 121 readable frames and verified dimensions, frame rate and duration. A separate ffmpeg full decode with -xerror completed exit 0 with no errors. Eight decoded frame samples were extracted (0, 17, 38, 50, 67, 82, 100, 120) and visually inspected. Sample composition is correct: full bust on the left, 400 × 360 face crop on the right, dark padding. No obvious codec corruption was seen in the inspected samples.

## Visual scope and findings
Inspected the original nine-panel source, nine-anchor native detail contact sheet, all 121 native detail frames in chronological contact sheets, eight decoded full/detail samples, and a full-resolution encoded peak sample. Framewise progression shows small intake opening, gradual blush and eye closure, closed-eye hold, reopening and neutral settling. No obvious pose-order reversal or large one-frame discontinuity was visible at contact-sheet resolution. This is not real-time playback and does not establish perceived pacing or absence of subtle jitter.

Source-specific raised-inner-brow strain and pinched mouth are substantially weaker than the source. Peak reads pleased/bashful rather than unmistakably overloaded by sweetness. The mouth barely changes at bust scale. Closed curved eyes and blush are present, but those ingredients alone do not establish expression identity. Dark jagged lash/hair intersection edges are visible at neutral and during closure/reopening; the sequence changes lash shape from downward closure to smile curvature, which needs normal-speed scrutiny. Framing remains stable in the inspected samples.

## Explicit missing checks
- No real-time playback or pacing/flicker assessment was performed (not performed in this validation pass).
- No native comparator review against EXP-197 Kiss, EXP-160 Shy Laughter, EXP-090 Queasy or EXP-096 Headache.
- Not all decoded frames were visually inspected; all decoded successfully, and eight were visually sampled. All 121 native detail frames were viewed as scaled contact sheets, not each at full resolution.
- No perceptual source-fit/distinctness pass and no user approval.
- No renderer rerun, CI, publication, upload or main-branch edit.

The earlier EXP-091-preview-blocker.md remains historical. Its encoding block is resolved only by the separately documented supplemental validator, not by silently changing the original gate.

Public report derived from the original technical QA: only the wording of the missing-playback note was neutralized. Technical evidence, findings and approval status are unchanged.
