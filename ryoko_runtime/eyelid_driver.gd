extends RefCounted
# Coordinates are viewer/screen side, not the character's anatomical side.
var hold_left=-1.0
var hold_right=-1.0
var wink_left=0.0
var wink_right=0.0
func reset():
    hold_left=-1.0;hold_right=-1.0;wink_left=0.0;wink_right=0.0
func set_hold(side:String,value:float):
    var closed=1.0 if is_finite(value) and value>=0.5 else 0.0
    if side=="screen_left":hold_left=closed
    elif side=="screen_right":hold_right=closed
func trigger(side:String,duration=0.28)->bool:
    if side not in ["screen_left","screen_right","both"]:return false
    var seconds=float(duration)
    seconds=clamp(seconds,0.08,0.8) if is_finite(seconds) else 0.28
    if side in ["screen_left","both"]:wink_left=seconds
    if side in ["screen_right","both"]:wink_right=seconds
    return true
func step(delta:float):
    wink_left=max(0.0,wink_left-max(0.0,delta))
    wink_right=max(0.0,wink_right-max(0.0,delta))
func busy()->bool:
    return hold_left>=0 or hold_right>=0 or wink_left>0 or wink_right>0
func resolve(shared:float)->Vector2:
    var left=hold_left if hold_left>=0 else shared
    var right=hold_right if hold_right>=0 else shared
    if wink_left>0:left=1.0
    if wink_right>0:right=1.0
    return Vector2(left,right)
