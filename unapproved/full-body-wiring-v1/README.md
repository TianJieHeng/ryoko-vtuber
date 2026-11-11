# Individual-part full-body wiring, unapproved

The earlier combined-body/bust-overlay approach on this branch was rejected. This revision replaces it with independently cut and registered raw parts from `avatar_build_assets`, attached to the skeletal hierarchy. The original bust node is removed entirely. Main and the approved facial app remain unchanged.

- [Implementation, source ownership and limits](../../ryoko_object_rig/full_body/README.md)
- [Every layer, bind transform, pivot and parent](../../ryoko_object_rig/full_body/registration.json)
- [Actual Godot headless checks](../../ryoko_object_rig/full_body/review/headless_checks.json)
- [Labeled CPU assembly MP4](../../ryoko_object_rig/full_body/review/ryoko_full_body_wiring_v1.mp4)

The clip is not a native Godot render and does not show animated facial shader output. It checks only neutral assembly and isolated head/elbow attachments. The missing clean neck skin is new unapproved compatible artwork with provenance. Native visual review and user approval remain outstanding. Do not merge this branch into main without approval.
