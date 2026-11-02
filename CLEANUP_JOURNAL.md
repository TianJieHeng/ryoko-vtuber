# 2D-only repository cleanup

2026-11-02: User explicitly requested a full-body 2D cut-and-assemble VTuber and removal of everything unrelated to that assembly. Starting commit: addadee7a3310bfdf15fae3b2d14bcf2980e5c18.

Removed from the current branch: the `vtuber/` 3D implementation, 3D build plans/handoffs/material targets, duplicate root/reference-library collections, obsolete publication journals and batch snapshots, generation prompts/sidecars not needed for assembly, and rejected audit artwork. Retained one assembly collection with the 69 transparent parts, useful source sheets, all expression/body references and extracted panels, original character references and useful catalogues. Replaced active instructions with the 2D workflow. No image bytes were modified by cleanup.

This is a normal child commit, not a history rewrite or permanent purge. It does not build or validate a new rig. The missing separate neck part and registration/assembly work remain explicit.
