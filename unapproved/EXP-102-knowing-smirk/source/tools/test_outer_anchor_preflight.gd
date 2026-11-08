extends SceneTree
const Limits=preload('res://control_limits.gd')
var checks=0
var failures=[]
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func _initialize():call_deferred('run')
func run():
 var rig=load('res://expression_rig.tscn').instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,'ready')
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 var max_error=0.0
 for tilt in [-1.0,-.7,0.0,.4,1.0]:
  for vertical in [-1.0,-.25,0.0,.25,1.0]:
   for left_lift in [0.0,.001,.25,.5,.999,1.0]:
    for right_lift in [0.0,.001,.25,.5,.999,1.0]:
     var cmd={'brow_tilt_screen_left':tilt,'brow_tilt_screen_right':-tilt,'brow_screen_left':vertical,'brow_screen_right':-vertical,'brow_inner_lift_screen_left':left_lift,'brow_inner_lift_screen_right':right_lift}
     check(rig.apply_controls(cmd),'apply')
     for side in ['screen_left','screen_right']:
      var key='brow_'+side;var home=rig.face.homes[key];var node=home.node
      var theta=(Vector2(cmd['brow_tilt_screen_left'],cmd['brow_tilt_screen_right'])*deg_to_rad(8))[0 if side=='screen_left' else 1]
      var a=Limits.BROW_OUTER_ANCHORS[side]-home.pivot
      var v=Vector2(0,-cmd['brow_'+side]*10)
      var expected=home.pivot+v+a.rotated(theta)
      var actual=node.position+a.rotated(node.rotation)
      var error=actual.distance_to(expected);max_error=maxf(max_error,error)
      check(error<0.00015,'tail fixed '+side)
      check(node.scale==Vector2.ONE and rig.face.objects[key].scale==Vector2.ONE,'unit scale')
      check(rig.face.objects[key].modulate.a==1,'no opacity')
      if cmd['brow_inner_lift_'+side]==0:
       check(node.position==home.pivot+v and node.rotation==theta,'zero exact old transform')
 rig.reset()
 check(rig.get_state().controls.brow_inner_lift_screen_left==0 and rig.get_state().controls.brow_inner_lift_screen_right==0,'reset')
 print('OUTER_ANCHOR_PREFLIGHT_', 'PASS' if failures.is_empty() else 'FAIL',' checks=',checks,' max_tail_error_px=',max_error,' failures=',failures)
 quit(0 if failures.is_empty() else 1)
