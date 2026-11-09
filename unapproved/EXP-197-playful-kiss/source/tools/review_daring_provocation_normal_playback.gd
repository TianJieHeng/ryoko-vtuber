extends "res://tools/review_daring_provocation_trajectory.gd"
## Separate real-time native playback. Execution is not itself a claim of human/CUA observation.
func run():
 for a in OS.get_cmdline_user_args():
  if a=="--coordinator-godot-slot-granted":runtime_lease=true
  if a=="--coordinator-display-lease-granted":display_lease=true
  if a=="--independent-pre-render-review-approved":review_approved=true
  if a.begins_with("--output="):output=a.trim_prefix("--output=")
 if output.is_empty() or not runtime_lease or not display_lease or not review_approved or DisplayServer.get_name()=="headless":quit(2);return
 DirAccess.make_dir_recursive_absolute(output)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();full_head=rig.head.transform;full_body=rig.body.transform;full_rig=rig.transform
 rig.reset();var neutral=actual_snapshot();var cycles=[]
 for view in ["bust","native"]:
  set_view(view)
  for cycle in range(2):
   rig.reset();await create_timer(.75).timeout
   check(rig.play_expression(ID),"normal playback trigger")
   var started=Time.get_ticks_usec();var previous=started;var samples=[]
   # Wall-time frame deltas drive the ordinary public advance API, not a synthetic frame clock.
   while rig.active_performance!="" and failures.is_empty():
    await process_frame
    var now=Time.get_ticks_usec();var delta=float(now-previous)/1000000.0;previous=now
    check(rig.advance(delta),"actual frame advance")
    check(rig.head.transform==full_head and rig.body.transform==full_body and rig.transform==full_rig,"fixed camera-only presentation")
    samples.append({"wall_seconds":float(now-started)/1000000.0,"frame_delta":delta,"state":rig.get_state()})
   check(rig.pose_now()==rig.neutral_pose() and actual_snapshot()==neutral,"normal cycle exact canonical neutral")
   cycles.append({"view":view,"cycle":cycle,"wall_seconds":float(Time.get_ticks_usec()-started)/1000000.0,"samples":samples})
   if not failures.is_empty():break
  if not failures.is_empty():break
 rig.reset();check(actual_snapshot()==neutral,"final exact restore")
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"cycles":cycles,"real_time_playback_executed":true,"normal_speed_playback_observed":false,"observation_note":"Independent supported CUA observations must be recorded separately; elapsed time alone does not establish visual acceptance.","display_server":DisplayServer.get_name(),"renderer":RenderingServer.get_video_adapter_name(),"profile_sha256":digest(FileAccess.get_file_as_bytes("res://expressions/EXP-114.json"))}
 var f=FileAccess.open(output+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print("DARING_PROVOCATION_NORMAL_",result.status," cycles=",cycles.size()," checks=",checks);quit(0 if failures.is_empty() else 1)
