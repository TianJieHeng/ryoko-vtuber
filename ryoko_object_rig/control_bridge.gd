extends Node
const Limits=preload("res://control_limits.gd")
## Local transport adapter only. The viewer's one rig is the sole pose controller.
const StrictJSON = preload("res://strict_control_json.gd")
const PROTOCOL = 1
const MAX_LINE_BYTES = 4096
const MAX_RESPONSE_BYTES = 16384
const MAX_OUTPUT_BYTES = 32768
const MAX_PER_FRAME = 4
const RATE_PER_SECOND = 60.0
const RATE_BURST = 20.0
const PARTIAL_TIMEOUT_MS = 2000
const OUTPUT_TIMEOUT_MS = 2000
const IDLE_TIMEOUT_MS = 30000
const MAX_ID = 2147483647
const READ_VERBS = ["capabilities", "list_expressions", "get_state"]
const WRITE_VERBS = ["apply_controls", "play_expression", "release", "reset"]
var rig
var server := TCPServer.new()
var peer: StreamPeerTCP
var enabled := false
var external_enabled := false
var port := 0
var last_error := ""
var session := 0
var last_id := 0
var discovered := false
var received := PackedByteArray()
var outgoing := PackedByteArray()
var closing := false
var partial_since := -1
var output_since := -1
var last_activity := 0
var rate_tokens := RATE_BURST
var rate_updated_ms := 0

func _ready():
    # UI/input processing precedes this transport adapter, after the shared rig.
    process_priority = 20

func start(controller, requested_port: int) -> bool:
    if enabled or requested_port < 1024 or requested_port > 65535:
        last_error = "Port must be 1024..65535 and bridge must be stopped"
        return false
    if controller == null or not controller.registry_ready:
        last_error = "Shared registry/controller unavailable"
        return false
    var result := server.listen(requested_port, "127.0.0.1")
    if result != OK:
        last_error = "Cannot bind loopback port " + str(requested_port) + " (" + str(result) + ")"
        return false
    rig = controller
    port = requested_port
    enabled = true
    external_enabled = true
    last_error = ""
    return true

func stop():
    disconnect_client()
    server.stop()
    enabled = false
    external_enabled = false
    port = 0

func _exit_tree():
    stop()

func disconnect_client():
    if peer != null:
        peer.disconnect_from_host()
    peer = null
    received.clear()
    outgoing.clear()
    closing = false
    partial_since = -1
    output_since = -1
    last_id = 0
    discovered = false

func manual_takeover():
    if not enabled:
        return
    external_enabled = false
    # No deferred request survives a UI takeover. No pose action here.
    disconnect_client()

func allow_external():
    if not enabled:
        return
    # Re-enabling is a fresh connection, never a release of stale queued input.
    disconnect_client()
    external_enabled = true

func status() -> Dictionary:
    return {"listening": enabled, "host": "127.0.0.1", "port": port,
        "external_enabled": external_enabled, "connected": peer != null,
        "session": session, "last_error": last_error}

func _process(_delta):
    if not enabled:
        return
    var now := Time.get_ticks_msec()
    if peer != null:
        peer.poll()
        if peer.get_status() != StreamPeerTCP.STATUS_CONNECTED:
            disconnect_client()
    if server.is_connection_available():
        var candidate := server.take_connection()
        if peer == null:
            peer = candidate
            peer.set_no_delay(true)
            session += 1
            last_activity = now
            rate_tokens = RATE_BURST
            rate_updated_ms = now
        else:
            # One small best-effort error; never queue or service a second peer.
            candidate.put_partial_data((JSON.stringify({"protocol": PROTOCOL, "id": null,
                "ok": false, "error": {"code": "busy", "message": "One client is already connected"}}) + "\n").to_utf8_buffer())
            candidate.disconnect_from_host()
    if peer == null:
        return
    rate_tokens = minf(RATE_BURST, rate_tokens + maxf(now - rate_updated_ms, 0) * RATE_PER_SECOND / 1000.0)
    rate_updated_ms = now
    flush_output(now)
    if peer == null:
        return
    if closing:
        if outgoing.is_empty():
            disconnect_client()
        return
    if now - last_activity >= IDLE_TIMEOUT_MS:
        reject(null, "idle_timeout", "No complete request within 30 seconds")
        closing = true
        return
    if partial_since >= 0 and now - partial_since >= PARTIAL_TIMEOUT_MS:
        reject(null, "partial_timeout", "Incomplete message exceeded 2 seconds")
        closing = true
        return
    for _index in range(MAX_PER_FRAME):
        # Reserve the entire maximum response before executing any mutation.
        if outgoing.size() > MAX_OUTPUT_BYTES - MAX_RESPONSE_BYTES:
            break
        if received.find(10) < 0:
            var available := peer.get_available_bytes()
            if available <= 0:
                break
            var result := peer.get_partial_data(mini(available, MAX_LINE_BYTES + 1 - received.size()))
            if result[0] != OK:
                disconnect_client()
                return
            if received.is_empty():
                partial_since = now
            received.append_array(result[1])
        var newline := received.find(10)
        if newline < 0:
            if received.size() > MAX_LINE_BYTES:
                reject(null, "message_too_large", "Message exceeds 4096 bytes")
                closing = true
            break
        var line := received.slice(0, newline)
        received = received.slice(newline + 1)
        partial_since = -1 if received.is_empty() else now
        last_activity = now
        if rate_tokens < 1:
            reject(null, "rate_limited", "Request rate exceeded")
            closing = true
            break
        rate_tokens -= 1
        dispatch(line)
    flush_output(now)

func flush_output(now: int):
    if outgoing.is_empty():
        output_since = -1
        return
    if output_since < 0:
        output_since = now
    if now - output_since >= OUTPUT_TIMEOUT_MS:
        disconnect_client()
        return
    var result := peer.put_partial_data(outgoing)
    if result[0] != OK:
        disconnect_client()
        return
    if result[1] > 0:
        outgoing = outgoing.slice(result[1])
        # Total blocked-output timeout, not extended indefinitely by trickle reads.
    if outgoing.is_empty():
        output_since = -1

func positive_integer(value: Variant) -> bool:
    return (value is int or value is float) and is_finite(float(value)) and value >= 1 and value <= MAX_ID and float(value) == floor(float(value))

func dispatch(line: PackedByteArray):
    var parser := StrictJSON.new()
    if not parser.parse(line):
        reject(null, "invalid_json", parser.error)
        return
    var request = parser.value
    if not request is Dictionary:
        reject(null, "invalid_request", "Request must be an object")
        return
    var id = request.get("id")
    if not positive_integer(id):
        reject(null, "invalid_id", "id must be an integer from 1 through 2147483647")
        return
    id = int(id)
    if id <= last_id:
        reject(id, "stale_id", "Request IDs must strictly increase within a connection")
        return
    last_id = id
    if not positive_integer(request.get("protocol")) or request.protocol != PROTOCOL:
        reject(id, "unsupported_protocol", "protocol must be 1")
        return
    var verb = request.get("verb")
    if not verb is String or (verb not in READ_VERBS and verb not in WRITE_VERBS):
        reject(id, "unknown_verb", "Unsupported verb")
        return
    var write: bool = verb in WRITE_VERBS
    var fields := ["protocol", "id", "verb", "args"]
    if write:
        fields.append("session")
    for key in request:
        if key not in fields:
            reject(id, "unknown_field", "Unknown envelope field: " + key)
            return
    var args = request.get("args", {})
    if not args is Dictionary:
        reject(id, "invalid_args", "args must be an object")
        return
    if verb == "play_expression":
        if args.size() != 1 or not args.has("expression_id") or not args.expression_id is String:
            reject(id, "invalid_args", "play_expression requires only a string expression_id")
            return
    elif verb != "apply_controls" and not args.is_empty():
        reject(id, "invalid_args", "This verb takes no arguments")
        return
    if write:
        if not discovered or not positive_integer(request.get("session")) or request.session != session:
            reject(id, "stale_session", "Read get_state or capabilities on this connection before writing")
            return
        if not external_enabled:
            reject(id, "manual_lock", "Manual takeover: re-enable external control in the viewer")
            return
    match verb:
        "capabilities":
            discovered = true
            acknowledge(id, capabilities())
        "list_expressions":
            acknowledge(id, rig.list_expressions())
        "get_state":
            discovered = true
            acknowledge(id, {"rig": rig.get_state(), "bridge": status()})
        _:
            var controls: Dictionary = args
            if verb == "play_expression":
                controls = {"perform_expression": args.expression_id}
            elif verb == "release":
                controls = {"release_performance": true}
            elif verb == "reset":
                controls = {"reset": true}
            if not rig.apply_controls(controls):
                reject(id, "invalid_controls", rig.last_error)
                return
            acknowledge(id, {"rig": rig.get_state(), "bridge": status()})

func capabilities() -> Dictionary:
    return {"name": "ryoko-shared-rig-control", "protocol": PROTOCOL,
        "transport": "tcp-json-lines-loopback", "verbs": READ_VERBS + WRITE_VERBS,
        "expressions": rig.list_expressions(), "bridge": status(),
        "controls": {"mouth_open": [0.0, 1.0], "mouth_smile": [0.0, 1.0], "mouth_spread": [0.0, 1.0], "mouth_corner_lift": [0.0, 1.0], "mouth_lip_press": [0.0, 1.0], "mouth_oral_lift": [0.0, 1.0], "mouth_purse": [0.0, 1.0], "blush_intensity": [0.0, 1.0], "eye_smile_R": [0.0, 1.0], "eye_smile_L": [0.0, 1.0], "blink": [0.0, 1.0], "blink_L": [0.0, 1.0], "blink_R": [0.0, 1.0],
            "brow_raise": [-1.0, 1.0], "brow_screen_left": [-1.0, 1.0], "brow_screen_right": [-1.0, 1.0],
            "brow_tilt_screen_left": [-1.0, 1.0], "brow_tilt_screen_right": [-1.0, 1.0],
            "hair_sway": [-0.07, 0.07], "gaze_x": [Limits.GAZE_MIN, Limits.GAZE_MAX], "gaze_y": [Limits.GAZE_MIN, Limits.GAZE_MAX],
            "auto_blink": "boolean", "reset": "boolean", "release_performance": "boolean",
            "perform_expression": "registered ID or alias", "mouth": ["REST", "RELEASE", "NEUTRAL"], "viseme": ["REST", "RELEASE", "NEUTRAL"]},
        "limits": {"message_bytes": MAX_LINE_BYTES, "response_bytes": MAX_RESPONSE_BYTES,
            "queued_output_bytes": MAX_OUTPUT_BYTES, "requests_per_frame": MAX_PER_FRAME,
            "requests_per_second": RATE_PER_SECOND, "burst_requests": RATE_BURST,
            "json_depth": StrictJSON.MAX_DEPTH, "json_values": StrictJSON.MAX_TOKENS,
            "clients": 1, "idle_timeout_ms": IDLE_TIMEOUT_MS, "partial_timeout_ms": PARTIAL_TIMEOUT_MS},
        "gaze": Limits.gaze_capabilities(), "physical_mouth_max": 0.55, "lateral_mouth": {"effective": "mouth_spread * mouth_smile", "maximum_half_width_increment_source_px": 20.0, "maximum_additional_corner_lift_source_px": 5.0, "maximum_center_lift_source_px": 4.0}, "closed_smile": {"control": "mouth_corner_lift", "maximum_additional_corner_lift_source_px": 12.0, "shape": "cubic source-radius lift", "independent_of_opening_and_spread": true, "lip_press_control": "mouth_lip_press", "maximum_inner_lip_depth_source_px": 4.0}, "blush_effect": {"control": "blush_intensity", "default": 0.0, "fixed_registered_source": true, "anatomy_unchanged": true, "foreground_hair_occludes": true}, "oral_surface": {"control": "mouth_oral_lift", "owner": "spread_lower_oral_surface", "maximum_total_rise_source_px": 40.0, "additional_rise_source_px": "40 * (1 - mouth_spread * mouth_smile) * mouth_oral_lift", "default": 0.0, "fixed_source_and_unit_scale": true}, "lip_purse": {"control": "mouth_purse", "default": 0.0, "scope": "bounded shared control"}, "ai_model_connected": false, "tts_connected": false}

func acknowledge(id: int, result: Variant):
    enqueue({"protocol": PROTOCOL, "id": id, "session": session, "ok": true, "result": result})

func reject(id: Variant, code: String, message: String):
    enqueue({"protocol": PROTOCOL, "id": id, "session": session, "ok": false,
        "error": {"code": code, "message": message}})

func enqueue(response: Dictionary):
    var bytes := (JSON.stringify(response) + "\n").to_utf8_buffer()
    if bytes.size() > MAX_RESPONSE_BYTES:
        bytes = (JSON.stringify({"protocol": PROTOCOL, "id": response.id, "session": session,
            "ok": false, "error": {"code": "response_too_large", "message": "Response exceeds bounded transport capacity"}}) + "\n").to_utf8_buffer()
    if outgoing.size() + bytes.size() > MAX_OUTPUT_BYTES:
        # An exhausted peer cannot be promised delivery. Never grow the queue.
        disconnect_client()
        return
    outgoing.append_array(bytes)
