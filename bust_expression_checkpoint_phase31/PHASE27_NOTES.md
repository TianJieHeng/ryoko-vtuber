# Phase 27: approved visual checkpoint

- EXP-063 stunned silence: raised worried brows, wide fixed amber eyes and a small parted mouth.
- EXP-090 queasy: raised inner brows, heavy amber eye slits and small pursed downturned lips.
- EXP-153 hiding a smile: relaxed brows, crinkled open amber eyes and a restrained closed-lip smile.

All three use dedicated fully closed blink artwork. Speech mouths independently override and restore expression rest. Fixed jaw, chin, neck and body are unchanged across twelve review states outside the existing shared speech-mouth bounds. All 78 earlier profiles and 489 existing artwork PNGs are preserved byte-for-byte.

Built-in image generation supplied facial artwork. The existing crop/mask registration pipeline assembles only eyes, brows, mouth and cheek tiles onto the approved base. Source framing is normalized to the registration canvas; full generated busts are not runtime replacements.

Comparison boards are static registered sprite composites, not live graphical runtime captures. No audio wiring, continuous deformation, physics, transitions or CI added. User approved the comparison boards before publication.

Validation: facial controls 89 passed; expression controls 50,944 passed (Godot 4.6.3 headless); jaw registration 12/12 passed; prior-asset preservation passed. Initial test invocation could not write Godot user data to its default home location; rerun with workspace-local XDG data/cache/config passed with exit codes 0. Visual review covers static boards, not live graphical runtime.
