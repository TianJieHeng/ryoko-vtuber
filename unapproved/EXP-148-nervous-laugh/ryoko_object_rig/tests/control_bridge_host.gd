extends SceneTree
## Test-only local harness. Never loaded by the app; no test verb in the protocol.
var viewer
var directory := ""
var handled := 0
func _initialize():
    for argument in OS.get_cmdline_user_args():
        if argument.begins_with("--test-directory="):
            directory = argument.trim_prefix("--test-directory=")
    if directory.is_empty():
        quit(2)
        return
    call_deferred("run")
func run():
    viewer = load("res://expression_viewer.tscn").instantiate()
    root.add_child(viewer)
    viewer.rig.set_process(false)
    write_reply({"ready": true})
func snapshot() -> Dictionary:
    var state: Dictionary = viewer.rig.get_state()
    state.erase("last_error")
    state.face = viewer.rig.face.snapshot()
    state.restart = viewer.rig.restart_pose.duplicate(true)
    state.release = viewer.rig.release_pose.duplicate(true)
    state.elapsed = viewer.rig.elapsed
    state.current = viewer.rig.current_pose.duplicate(true)
    state.performance = viewer.rig.performance.duplicate(true)
    return state
func write_reply(result: Dictionary):
    result.sequence = handled
    var file = FileAccess.open(directory.path_join("reply.tmp"), FileAccess.WRITE)
    file.store_string(JSON.stringify(result));file.close()
    DirAccess.rename_absolute(directory.path_join("reply.tmp"), directory.path_join("reply.json"))
func _process(_delta):
    if viewer == null or not FileAccess.file_exists(directory.path_join("command.json")):
        return false
    var command = JSON.parse_string(FileAccess.get_file_as_string(directory.path_join("command.json")))
    if not command is Dictionary or command.get("sequence", 0) <= handled:
        return false
    handled = command.sequence
    match command.action:
        "snapshot": pass
        "advance": viewer.rig.advance(command.value)
        "run_clock": viewer.rig.set_process(command.value)
        "manual_slider": viewer.sliders.mouth_open.value = command.value
        "manual_invalid": viewer.apply_controls({"mouth_open": 2})
        "enable": viewer.bridge_button.pressed.emit()
        "key":
            var event = InputEventKey.new()
            event.keycode = int(command.value);event.pressed = true
            Input.parse_input_event(event);Input.flush_buffered_events()
        "stop": viewer.control_bridge.stop()
        "quit": quit()
    write_reply({"snapshot": snapshot(), "bridge": viewer.control_bridge.status(), "transport": {"received": viewer.control_bridge.received.size(), "outgoing": viewer.control_bridge.outgoing.size(), "last_id": viewer.control_bridge.last_id}})
    return false
