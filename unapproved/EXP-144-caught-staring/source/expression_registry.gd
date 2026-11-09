extends RefCounted
## Data-only catalogue. Validation is transactional; callers receive deep copies.
const Limits=preload("res://control_limits.gd")
const CHANNEL_BOUNDS={"blink_R":[0.0,1.0],"blink_L":[0.0,1.0],"brow_screen_left":[-1.0,1.0],"brow_screen_right":[-1.0,1.0],"brow_tilt_screen_left":[-1.0,1.0],"brow_tilt_screen_right":[-1.0,1.0],"brow_inner_lift_screen_left":[0.0,1.0],"brow_inner_lift_screen_right":[0.0,1.0],"gaze_x":[Limits.GAZE_MIN,Limits.GAZE_MAX],"gaze_y":[Limits.GAZE_MIN,Limits.GAZE_MAX],"gaze_down_extra":[0.0,1.0],"hair_sway":[-0.07,0.07],"mouth_open":[0.0,1.0],"eye_smile_R":[0.0,1.0],"eye_smile_L":[0.0,1.0],"mouth_smile":[0.0,1.0],"mouth_spread":[0.0,1.0],"mouth_width_screen_left":[0.0,1.0],"mouth_width_screen_right":[0.0,1.0],"mouth_corner_lift":[0.0,1.0],"mouth_corner_lift_screen_left":[0.0,1.0],"mouth_corner_lift_screen_right":[0.0,1.0],"mouth_lip_press":[0.0,1.0],"mouth_oral_lift":[0.0,1.0],"mouth_purse":[0.0,1.0],"mouth_kiss":[0.0,1.0],"blush_intensity":[0.0,1.0]}
const DEFINITION_KEYS=["id","title","duration","keyframes","status","intent","source_catalogue_sha256","timing_origin","scope","interpolation"]
var last_error=""
var _entries:Dictionary={}
var _aliases:Dictionary={}
static func number(value)->bool:
    return (value is int or value is float) and is_finite(float(value))
# Public width is sealed-mouth only. Call after finite/bounds validation.
static func sealed_mouth_valid(values:Dictionary)->bool:
    return not (float(values.get("mouth_open",0.0))>0.0 and (float(values.get("mouth_width_screen_left",0.0))>0.0 or float(values.get("mouth_width_screen_right",0.0))>0.0 or float(values.get("mouth_kiss",0.0))>0.0))
static func width_present(values:Dictionary)->bool:
    return float(values.get("mouth_width_screen_left",0.0))>0.0 or float(values.get("mouth_width_screen_right",0.0))>0.0 or float(values.get("mouth_kiss",0.0))>0.0
func fail(message:String)->bool:
    last_error=message;return false
func load_file(path:String="res://expressions/registry.json")->bool:
    var parsed=JSON.parse_string(FileAccess.get_file_as_string(path))
    if not parsed is Dictionary:return fail("Registry must be a JSON object")
    var definitions={}
    if parsed.get("entries") is Array:
        for entry in parsed.entries:
            if entry is Dictionary and entry.get("path") is String:
                var file=entry.path
                if not file.begins_with("res://") or not file.ends_with(".json") or ".." in file:
                    return fail("Definition path must be a local res:// JSON file")
                definitions[file]=JSON.parse_string(FileAccess.get_file_as_string(file))
    return load_catalogue(parsed,definitions)
func load_catalogue(catalogue,definitions:Dictionary)->bool:
    if not catalogue is Dictionary:return fail("Registry must be an object")
    for key in catalogue:
        if key not in ["schema_version","entries"]:return fail("Unknown registry key: "+str(key))
    if not number(catalogue.get("schema_version")) or catalogue.schema_version!=1:return fail("Unsupported schema_version")
    if not catalogue.get("entries") is Array or catalogue.entries.is_empty():return fail("Registry entries must be a nonempty array")
    var staged={};var names={}
    for entry in catalogue.entries:
        if not entry is Dictionary:return fail("Registry entry must be an object")
        for key in entry:
            if key not in ["id","path","aliases","trigger_phase"]:return fail("Unknown entry key: "+str(key))
        if not entry.get("id") is String or entry.id.strip_edges().is_empty():return fail("Entry id must be nonempty")
        if not entry.get("path") is String or not entry.path.begins_with("res://") or not entry.path.ends_with(".json") or ".." in entry.path:return fail("Definition path must be local JSON")
        if not entry.get("aliases",[]) is Array:return fail("Aliases must be an array")
        if not entry.get("trigger_phase","anticipation") is String or entry.get("trigger_phase","anticipation").is_empty():return fail("trigger_phase must be nonempty")
        var identifiers=[entry.id];identifiers.append_array(entry.get("aliases",[]))
        for id in identifiers:
            if not id is String or id.strip_edges().is_empty():return fail("IDs and aliases must be nonempty strings")
            if names.has(id):return fail("Duplicate ID or alias: "+id)
            names[id]=entry.id
        var definition=definitions.get(entry.path)
        if not validate_definition(definition,entry.id):return false
        staged[entry.id]={"definition":definition.duplicate(true),"aliases":entry.get("aliases",[]).duplicate(),"trigger_phase":entry.get("trigger_phase","anticipation")}
    _entries=staged;_aliases=names;last_error="";return true
func validate_definition(definition,expected_id:String)->bool:
    if not definition is Dictionary:return fail("Missing/invalid definition: "+expected_id)
    for key in definition:
        if key not in DEFINITION_KEYS:return fail("Unknown definition key: "+str(key))
    if definition.get("id")!=expected_id:return fail("Definition ID does not match registry")
    if not definition.get("title") is String or definition.title.is_empty():return fail("Title must be nonempty")
    for key in DEFINITION_KEYS:
        if key not in ["duration","keyframes"] and definition.has(key) and not definition[key] is String:return fail("Expected string metadata: "+key)
    if not number(definition.get("duration")) or definition.duration<=0:return fail("Duration must be positive and finite")
    if not definition.get("keyframes") is Array or definition.keyframes.size()<2:return fail("At least two keyframes are required")
    var previous=-1.0
    for frame in definition.keyframes:
        if not frame is Dictionary:return fail("Keyframe must be an object")
        for key in frame:
            if key not in ["time","phase","values"]:return fail("Unknown keyframe key: "+str(key))
        if not number(frame.get("time")) or frame.time<0 or frame.time>definition.duration or frame.time<=previous:return fail("Keyframe times must be finite, in range and strictly increasing")
        previous=frame.time
        if not frame.get("phase") is String or frame.phase.is_empty():return fail("Keyframe phase must be nonempty")
        if not frame.get("values") is Dictionary:return fail("Keyframe values must be an object")
        for channel in frame.values:
            if not CHANNEL_BOUNDS.has(channel):return fail("Unknown channel: "+str(channel))
            var value=frame.values[channel];var bounds=CHANNEL_BOUNDS[channel]
            if not number(value) or value<bounds[0] or value>bounds[1]:return fail("Out-of-range or nonfinite channel: "+channel)
    # Shared smoothstep between nonnegative endpoints must remain in one
    # domain. A neutral trio key separates width and opening segments.
    for frame in definition.keyframes:
        if not sealed_mouth_valid(frame.values):return fail("Positive mouth width or kiss requires mouth_open == 0")
    for index in range(definition.keyframes.size()-1):
        var a=definition.keyframes[index].values;var b=definition.keyframes[index+1].values
        if maxf(float(a.get("mouth_open",0.0)),float(b.get("mouth_open",0.0)))>0.0 and (width_present(a) or width_present(b)):
            return fail("Opening and sealed-mouth segments require an explicit zero-trio key")
    var first=definition.keyframes[0];var final=definition.keyframes[-1]
    if first.time!=0 or final.time!=definition.duration:return fail("Timeline must span time 0 through duration")
    for frame in [first,final]:
        for value in frame.values.values():
            if value!=0:return fail("Timeline endpoints must be neutral")
    last_error="";return true
func resolve(id:String)->String:return _aliases.get(id,"")
func definition(id:String)->Dictionary:
    return _entries.get(resolve(id),{}).get("definition",{}).duplicate(true)
func trigger_phase(id:String)->String:return _entries.get(resolve(id),{}).get("trigger_phase","anticipation")
func list_expressions()->Array:
    var result=[]
    for id in _entries:
        var e=_entries[id]
        result.append({"id":id,"title":e.definition.title,"duration":e.definition.duration,"aliases":e.aliases.duplicate()})
    return result
