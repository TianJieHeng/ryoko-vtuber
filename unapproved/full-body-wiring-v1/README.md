# Individual-part full-body wiring, unapproved

The earlier combined-body/bust-overlay approach on this branch was rejected. This revision replaces it with independently cut and registered raw parts from `avatar_build_assets`, attached to the skeletal hierarchy. The original bust node is removed entirely. Main and the approved facial app remain unchanged.

- [Implementation, source ownership and limits](../../ryoko_object_rig/full_body/README.md)
- [Every layer, bind transform, pivot and parent](../../ryoko_object_rig/full_body/registration.json)
- [Actual Godot headless checks](../../ryoko_object_rig/full_body/review/headless_checks.json)
- [Labeled CPU assembly MP4](../../ryoko_object_rig/full_body/review/ryoko_full_body_wiring_v1.mp4)

The clip is not a native Godot render and does not show animated facial shader output. The current clip holds neutral for sleeve/arm inspection without a gesture. The missing clean neck skin is new unapproved compatible artwork with provenance. Native visual review and user approval remain outstanding. Do not merge this branch into main without approval.

The latest jacket correction removes construction-facing strips from the visible lapels, separates the two front shirt-collar tabs and gold fastener, and restores the longer fitted hem. See [source cuts and fitting records](../../ryoko_object_rig/full_body/jacket_review/README.md). This correction is still awaiting user review.

The neutral sleeve correction aligns both painted folds at each elbow, removes the visible construction tube ends, and restores the hand/cuff connection. See [sleeve cuts and bind points](../../ryoko_object_rig/full_body/elbow_review/registration_candidate.json).
