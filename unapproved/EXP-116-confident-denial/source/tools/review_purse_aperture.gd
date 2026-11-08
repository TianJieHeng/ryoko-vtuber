extends SceneTree
## Isolated production cavity-shader raster probe, not a character/movie render.
var out=""
func _initialize():call_deferred("run")
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
 if out.is_empty():quit(2);return
 DirAccess.make_dir_recursive_absolute(out)
 root.size=Vector2i(160,110);root.transparent_bg=true
 var im=Image.create(160,110,false,Image.FORMAT_RGBA8);im.fill(Color.WHITE)
 var node=Sprite2D.new();node.centered=false;node.texture=ImageTexture.create_from_image(im)
 var mat=ShaderMaterial.new();mat.shader=load("res://object_mouth_clip.gdshader")
 mat.set_shader_parameter("origin",Vector2(485,580));mat.set_shader_parameter("seam_texture",load("res://rig_assets/yawn_mouth/neutral_seam.png"));node.material=mat;root.add_child(node)
 var records=[];var maximum=0.0;var maximum_rows=0;var failures=[]
 for o in [0.0,.000001,.05,.3,.6,1.0]:
  for smile in [0.0,.5,1.0]:
   for spread in [0.0,.5,1.0]:
    for corner in [0.0,.5,1.0]:
     for purse in [0.0,.000001,.4,1.0]:
      mat.set_shader_parameter("opening",o*.55);mat.set_shader_parameter("smile",smile);mat.set_shader_parameter("spread",spread*smile);mat.set_shader_parameter("corner_lift",corner);mat.set_shader_parameter("purse",purse)
      await process_frame;await RenderingServer.frame_post_draw
      var picture=root.get_texture().get_image();var integrated=0.0;var rows=0
      for x in range(picture.get_width()):
       var sum=0.0;var count=0
       for y in range(picture.get_height()):
        var a=picture.get_pixel(x,y).a;sum+=a
        if a>0.0:count+=1
       integrated=maxf(integrated,sum);rows=maxi(rows,count)
      maximum=maxf(maximum,integrated);maximum_rows=maxi(maximum_rows,rows)
      if integrated>30.800001:failures.append(records.size())
      records.append({"mouth_open":o,"mouth_smile":smile,"mouth_spread":spread,"mouth_corner_lift":corner,"mouth_purse":purse,"integrated_column_px":integrated,"nonzero_rows":rows})
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"probe":"production cavity shader with opaque white test source; pressure can only occlude it; purse is evaluated through the exact production shader","poses":records,"maximum_integrated_source_px":maximum,"maximum_nonzero_rows":maximum_rows,"physical_cap":30.8,"failures":failures},"  "));f.close()
 print("PURSE_APERTURE_", "PASS" if failures.is_empty() else "FAIL"," poses=",records.size()," max=",maximum," raster_rows=",maximum_rows);quit(0 if failures.is_empty() else 1)
