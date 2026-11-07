extends RefCounted
## One contract for normalized gaze and calibrated source-pixel travel.
## Enable ONLY after both eyes, all corners, and closure combinations pass visual QA.
const GAZE_ENABLED=true
const GAZE_MIN=-1.0 if GAZE_ENABLED else 0.0
const GAZE_MAX=1.0 if GAZE_ENABLED else 0.0
const GAZE_LEFT_PIXELS=4.0
const GAZE_RIGHT_PIXELS=4.0
const GAZE_UP_PIXELS=2.0
const GAZE_DOWN_PIXELS=1.0
static func valid_gaze(value)->bool:
    return (value is int or value is float) and is_finite(float(value)) and value>=GAZE_MIN and value<=GAZE_MAX
static func gaze_pixels(value:Vector2)->Vector2:
    if not GAZE_ENABLED:return Vector2.ZERO
    var bounded=value.clamp(Vector2(GAZE_MIN,GAZE_MIN),Vector2(GAZE_MAX,GAZE_MAX))
    return Vector2(bounded.x*(GAZE_LEFT_PIXELS if bounded.x<0 else GAZE_RIGHT_PIXELS),bounded.y*(GAZE_UP_PIXELS if bounded.y<0 else GAZE_DOWN_PIXELS))
static func gaze_capabilities()->Dictionary:
    # Flat directional fields describe active support; calibration is not activation.
    return {"enabled":GAZE_ENABLED,"input_units":"normalized","physical_units":"source_pixels",
        "left":GAZE_LEFT_PIXELS if GAZE_ENABLED else 0.0,"right":GAZE_RIGHT_PIXELS if GAZE_ENABLED else 0.0,
        "up":GAZE_UP_PIXELS if GAZE_ENABLED else 0.0,"down":GAZE_DOWN_PIXELS if GAZE_ENABLED else 0.0,
        "calibration":{"status":"verified_enabled" if GAZE_ENABLED else "coverage_bounded_pending_visual_qa",
            "left":GAZE_LEFT_PIXELS,"right":GAZE_RIGHT_PIXELS,"up":GAZE_UP_PIXELS,"down":GAZE_DOWN_PIXELS}}
