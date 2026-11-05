extends RefCounted
var cues=[]
var duration=0.0
var elapsed=0.0
var index=0
var active=false
var paused=false
var error_message=""
# Invalidates already-collected cues after reset, cancel or clip replacement.
var dispatch_id=0
const ALLOWED=["loose_hair_secondary","earring_secondary","gaze_x","gaze_y","breath_level","breath_strength","breath_trigger","breath_cancel","brow_raise","brow_screen_left","brow_screen_right","look_x","look_y","look_release","ornament_secondary","head_tilt","head_x","head_y","body_tilt","body_x","body_y","body_follow","gesture","gesture_strength","gesture_cancel","wink","wink_duration","eye_screen_left","eye_screen_right","release_eye_controls","blink","auto_blink","audio_level","audio_stop","mouth","speech_active","bounce","chest_secondary","reset"]
func load_data(data)->bool:
    error_message=""
    if not data is Dictionary or data.get("version")!=1 or not data.get("cues") is Array:
        error_message="Invalid clip format.";return false
    if not (data.get("duration") is float or data.get("duration") is int) or not is_finite(float(data.duration)) or data.duration<=0 or data.duration>120:
        error_message="Duration must be between 0 and 120 seconds.";return false
    if data.cues.size()>512:error_message="Too many cues.";return false
    var last=-1.0
    for cue in data.cues:
        if not cue is Dictionary or not (cue.get("time") is float or cue.get("time") is int) or not cue.get("controls") is Dictionary:
            error_message="Invalid cue.";return false
        if not is_finite(float(cue.time)) or cue.time<last or cue.time<0 or cue.time>data.duration:
            error_message="Cues must be in time order and within duration.";return false
        for key in cue.controls:
            var value=cue.controls[key]
            if key not in ALLOWED or not (value is String or value is bool or value is float or value is int):
                error_message="Unsupported control: "+str(key);return false
            var string_keys=["gesture","wink","mouth"]
            var bool_keys=["loose_hair_secondary","earring_secondary","breath_trigger","breath_cancel","look_release","ornament_secondary","body_follow","gesture_cancel","release_eye_controls","auto_blink","audio_stop","speech_active","bounce","chest_secondary","reset"]
            if key in string_keys and not value is String:
                error_message="Expected text control.";return false
            if key in bool_keys and not value is bool:
                error_message="Expected boolean control.";return false
            if key not in string_keys and key not in bool_keys and not (value is float or value is int):
                error_message="Expected numeric control.";return false
            if (value is float or value is int) and not is_finite(float(value)):
                error_message="Non-finite value.";return false
            # Keep legacy clamping behavior unchanged; new cue fields use the
            # same documented ranges as the live adapter.
            if key in ["gaze_x","gaze_y","brow_raise","brow_screen_left","brow_screen_right","look_x","look_y"] and (value< -1.0 or value>1.0):
                error_message="Control must be between -1 and 1: "+key;return false
            if key in ["breath_level","breath_strength"] and (value<0.0 or value>1.0):
                error_message="Control must be between 0 and 1: "+key;return false
        last=cue.time
    stop();cues=data.cues.duplicate(true);duration=float(data.duration)
    return true
func load_file(path:String)->bool:
    var json=JSON.new()
    if json.parse(FileAccess.get_file_as_string(path))!=OK:error_message="Invalid clip JSON.";return false
    return load_data(json.data)
func play()->bool:
    if duration<=0:return false
    elapsed=0.0;index=0;active=true;paused=false;return true
func stop():
    dispatch_id+=1
    active=false;paused=false;elapsed=0.0;index=0
func step(delta:float)->Array:
    var due=[]
    if not active or paused:return due
    elapsed=min(duration,elapsed+max(0.0,delta))
    while index<cues.size() and float(cues[index].time)<=elapsed+0.000001:
        due.append(cues[index].controls.duplicate(true));index+=1
    if elapsed>=duration:active=false
    return due
