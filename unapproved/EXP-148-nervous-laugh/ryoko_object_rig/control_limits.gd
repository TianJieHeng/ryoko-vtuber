extends RefCounted
## Shared bounded movement contracts.
# Unapproved outer-anchor revision; 26-degree bound fixed for full local QA. Nonzero unpublished v0 inputs are NOT compatible.
const BROW_INNER_LIFT_DEGREES=26.0
const BROW_OUTER_ANCHORS={"screen_left":Vector2(466.550,452.350),"screen_right":Vector2(646.227,453.773)}
static func brow_capabilities()->Dictionary:
    return {"controls":["brow_inner_lift_screen_left","brow_inner_lift_screen_right"],
        "range":[0.0,1.0],"default":0.0,"additional_rotation_degrees":BROW_INNER_LIFT_DEGREES,
        "screen_left_sign":-1.0,"screen_right_sign":1.0,"composition":"angle = legacy_tilt + side_sign * bound * inner_lift; pivot = C + vertical + R(legacy_tilt) * (a - R(additive_angle) * a), a = outer_anchor - C",
        "outer_anchor_canonical":{"screen_left":[466.550,452.350],"screen_right":[646.227,453.773]},
        "anchor_reference":"tail after legacy center tilt and vertical translation",
        "zero_lift_legacy_transform_exact":true,
        "nonzero_v0_compatible":false,
        "supersedes_unapproved_mapping":"v0 used a 14 degree additive center-pivot rotation; v1 changes nonzero lift mapping",
        "legacy_tilt_degrees":[-8.0,8.0],"combined_screen_left_degrees":[-34.0,8.0],"combined_screen_right_degrees":[-8.0,34.0],
        "owner":"existing rigid brow pivot with rigid outer-anchor translation", "mapping_revision":"outer_anchor_v1_local_candidate","unit_scale":true,"foreground_hair_occludes":true,
        "state_semantics":"additive controls; omitted manual fields retain their value, omitted timeline fields default to zero"}

## One contract for normalized gaze and calibrated source-pixel travel.
## Enable ONLY after both eyes, all corners, and closure combinations pass visual QA.
const GAZE_ENABLED=true
const GAZE_MIN=-1.0 if GAZE_ENABLED else 0.0
const GAZE_MAX=1.0 if GAZE_ENABLED else 0.0
const GAZE_LEFT_PIXELS=4.0
const GAZE_RIGHT_PIXELS=4.0
const GAZE_UP_PIXELS=2.0
const GAZE_DOWN_PIXELS=1.0
# Explicit additive extension; old normalized gaze mapping remains unchanged.
const GAZE_DOWN_EXTRA_PIXELS=5.0
static func valid_gaze_down_extra(value)->bool:
    return (value is int or value is float) and is_finite(float(value)) and value>=0.0 and value<=1.0
static func valid_gaze(value)->bool:
    return (value is int or value is float) and is_finite(float(value)) and value>=GAZE_MIN and value<=GAZE_MAX
static func gaze_pixels(value:Vector2,down_extra:float=0.0)->Vector2:
    if not GAZE_ENABLED:return Vector2.ZERO
    var bounded=value.clamp(Vector2(GAZE_MIN,GAZE_MIN),Vector2(GAZE_MAX,GAZE_MAX))
    return Vector2(bounded.x*(GAZE_LEFT_PIXELS if bounded.x<0 else GAZE_RIGHT_PIXELS),bounded.y*(GAZE_UP_PIXELS if bounded.y<0 else GAZE_DOWN_PIXELS)+clampf(down_extra,0.0,1.0)*GAZE_DOWN_EXTRA_PIXELS)
static func gaze_capabilities()->Dictionary:
    # Flat directional fields describe active support; calibration is not activation.
    return {"enabled":GAZE_ENABLED,"input_units":"normalized",
        "down_extension":{"control":"gaze_down_extra","bounds":[0.0,1.0],"default":0.0,"additional_down_source_pixels":GAZE_DOWN_EXTRA_PIXELS,"combined_y_range":[-GAZE_UP_PIXELS,GAZE_DOWN_PIXELS+GAZE_DOWN_EXTRA_PIXELS],"combination":"old gaze_y source-pixel offset + gaze_down_extra * additional_down_source_pixels","status":"local candidate; user approval pending"},"physical_units":"source_pixels",
        "left":GAZE_LEFT_PIXELS if GAZE_ENABLED else 0.0,"right":GAZE_RIGHT_PIXELS if GAZE_ENABLED else 0.0,
        "up":GAZE_UP_PIXELS if GAZE_ENABLED else 0.0,"down":GAZE_DOWN_PIXELS if GAZE_ENABLED else 0.0,
        "calibration":{"status":"verified_enabled" if GAZE_ENABLED else "coverage_bounded_pending_visual_qa",
            "left":GAZE_LEFT_PIXELS,"right":GAZE_RIGHT_PIXELS,"up":GAZE_UP_PIXELS,"down":GAZE_DOWN_PIXELS}}
