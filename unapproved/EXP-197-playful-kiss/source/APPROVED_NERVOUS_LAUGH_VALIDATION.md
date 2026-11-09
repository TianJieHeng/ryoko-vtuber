# EXP-148 approved integration

Twenty user-approved performances share one rig. EXP-148 Nervous laugh adds the approved 3.6-second performance, with nervous-laugh and nervous_laugh aliases. All nineteen predecessor profiles, production runtime, scenes, shaders, 182 PNGs and both inherited iris import sidecars remain byte-exact. Only EXP-148 approval metadata changes from the reviewed acting profile; its duration, keyframes, controls and curves are unchanged.

EXP-148 live engine pacing and continuous normal-speed playback remain UNVERIFIED. Review covered 109 decoded chronological frames at 30 fps and selected full/detail/reference views, not continuous normal-speed observation. Source KP5–6 opposing dental clench is unsupported and excluded; source nose blush and painted brow curvature are approximations. The inherited EXP-114 smooth real-time pacing HOLD and other documented rig limits remain unchanged.

Current source checks: python -B tools/verify_approved_integration.py and sha256sum -c APPROVED_SOURCE_FILES.sha256. APPROVED_SOURCE_MANIFEST.json, APPROVED_INTEGRATION_STATUS.json and RELEASE.json describe this twenty-profile source. Prior manifests, test reports and expression-local candidate notes are historical evidence with their original scope. See APPROVED_NERVOUS_LAUGH_VALIDATION.md for the current approval and verification limits.

## Exact source and qualification

- Prior approved source: cc0b76ccf3a7e3e1475b9adc08cdfa298d079517, 661 source files, 19 profiles.
- Frozen preview source: c3fab643b2d8048ade34c703b4110c7ca4955c4b, 663 source files. [Preserved candidate backup](https://github.com/TianJieHeng/ryoko-vtuber/tree/5bef3fb6e4a5ab7ecf8d587312cf02f7107197c8/unapproved/EXP-148-nervous-laugh). Its unapproved label is historical.
- Reviewed profile SHA256: 74709a0deafa02c3a36f0c0960bbe25a47a81ec68ca5ae2cbb3541d5904aff87. Published profile SHA256: d803a850c3eda78f4f27586c0798432367fd66c9093c5cd7364bed0020ba47dd. The only changed profile field is status; all acting data and the registry are exact.
- One 3.6-second cycle: 109 sampled frames at 30 fps; 262 independent anatomical objects; all actual controls and owners checked; pixel-exact neutral return and restart/release restoration passed on this exact acting source.
- Both preview videos decoded to 109 chronological frames, each timestamp equal to index/30 within one microsecond. Duration 3.633333 seconds includes the sampled neutral endpoint.
- Final preview was preview_02. The earlier missing-import-sidecar failure stopped before any frame and was resolved before final capture; it was not an expression defect.
- No new runtime, transition, recovery archive or timing run is claimed. This approval-only overlay reuses the completed source-matched checks and adds a portable source/registry guard.

## Review limits

Inspected all 109 decoded detail frames chronologically in three sheets, all seven full-size selected stills and the reference comparison. Both small laugh accents are distinct, modest unequal lids keep both amber eyes visible, cheek blush rises once and fades, mouth reseals continuously. No new transient clipping, doubled blush or stray under-eye marks observed. Existing thin cheek hair strokes and subtle neck boundary are unchanged baseline anatomy. The brow worry remains milder and smile narrower than the painted reference; interpretation is restrained, slightly coy nervous amusement.

## Publication scope

Only the existing ryoko_object_rig root is updated. The prior publication receipt requires no second current source mirror. All other repository roots and the complete unapproved tree remain unchanged. Generated caches and import sidecars are excluded except the two already-tracked iris sidecars, which remain exact. No source paths are deleted.

EXP-097 remains rejected and excluded. EXP-187 remains parked and excluded. All other existing exclusions, source originals and unapproved backups are preserved. No new Godot run, CI, workflow changes, binary/media upload, archive, hardware flashing or remote-machine execution is part of this approval integration.
