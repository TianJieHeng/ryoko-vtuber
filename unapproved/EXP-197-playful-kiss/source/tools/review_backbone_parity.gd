extends SceneTree
## Run unchanged against isolated original and new projects. Outputs never go in source.
var stage
var out=""
var save_all=false
var hashes:Array=[]
var controls:Array=[]
func _initialize():call_deferred("run")
func record_frame(label:String,save:bool=false):
    await process_frame
    await RenderingServer.frame_post_draw
    var image=root.get_texture().get_image()
    var hash=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(image.get_data())
    hashes.append({"label":label,"sha256":hash.finish().hex_encode(),"width":image.get_width(),"height":image.get_height()})
    controls.append({"label":label,"pose":stage.primary.pose_now(),"phase":stage.primary.performance_phase,"time":stage.primary.performance_time})
    if save or save_all:image.save_png(out+"/"+label+".png")
func run():
    for arg in OS.get_cmdline_user_args():
        if arg=="--save-all":save_all=true
        if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
    if out.is_empty():push_error("Provide --output=<external-directory>");quit(2);return
    DirAccess.make_dir_recursive_absolute(out)
    stage=load("res://yawn_stage.tscn").instantiate();root.add_child(stage)
    stage.set_process(false);stage.primary.set_process(false)
    await process_frame;stage.apply_controls({"reset":true})
    var samples=[]
    for i in range(10001):samples.append(stage.primary.sample_yawn(i*5.8/10000.0))
    var file=FileAccess.open(out+"/dense_samples.json",FileAccess.WRITE);file.store_string(JSON.stringify(samples));file.close()
    # Identical 30 Hz time schedule through two complete performances, plus tail neutral.
    for tick in range(468):
        if tick in [30,255]:stage.apply_controls({"perform_expression":"EXP-163"})
        if tick>0:stage.advance(1.0/30.0)
        stage.status.text=("Cycle 1 / " if tick>=30 and tick<255 else ("Cycle 2 / " if tick>=255 else ""))+stage.primary.performance_phase.replace("_"," ")
        await record_frame("cycle_%03d"%tick,tick in [0,45,66,96,132,168,204,258,321,429,467])
    stage.apply_controls({"reset":true})
    for tick in range(180):
        if tick==0:stage.apply_controls({"perform_expression":"EXP-163"})
        if tick==45:stage.apply_controls({"perform_expression":"EXP-163"})
        if tick==75:stage.apply_controls({"release_performance":true})
        if tick==105:stage.apply_controls({"perform_expression":"EXP-163"})
        if tick==135:stage.apply_controls({"mouth_open":.24,"blink_R":.42})
        if tick==160:stage.apply_controls({"reset":true})
        # The trigger/release transaction frames are also captured before advancing.
        if tick in [45,75,135,160]:
            stage.status.text=stage.primary.performance_phase
            await record_frame("boundary_%03d"%tick,true)
        stage.advance(1.0/30.0);stage.status.text=stage.primary.performance_phase
        await record_frame("interrupt_%03d"%tick,tick in [0,44,45,74,75,90,104,134,135,159,160,179])
    file=FileAccess.open(out+"/frame_hashes.json",FileAccess.WRITE);file.store_string(JSON.stringify(hashes));file.close()
    file=FileAccess.open(out+"/controls.json",FileAccess.WRITE);file.store_string(JSON.stringify(controls));file.close()
    print("BACKBONE_PARITY_CAPTURE_PASS frames=",hashes.size()," dense_samples=",samples.size())
    quit()
