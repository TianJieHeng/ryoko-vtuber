extends SceneTree
## Actual Godot runtime draw-state sampling; no independent animation model.
var rig
var out = "res://full_body/face_review/samples"
var only = "EXP-002"
var fps = 15
var textures = {}
var shaders = {}
var draw_states = []
var draw_indices = {}
var frames = []
var uniform_cache = {}
var binary_files = {}
func _initialize():call_deferred("run")
func arr(v):
    if v is Vector2:return [v.x,v.y]
    if v is Vector3:return [v.x,v.y,v.z]
    if v is Vector4:return [v.x,v.y,v.z,v.w]
    if v is Color:return [v.r,v.g,v.b,v.a]
    if v is Texture2D:return {"texture":save_texture(v)}
    return v
func save_texture(texture):
    var key = str(texture.get_instance_id())
    if not textures.has(key):
        var name = "texture_%04d.png" % textures.size()
        var image = texture.get_image()
        image.save_png(out + "/" + name)
        textures[key] = {"file":name,"size":[image.get_width(),image.get_height()],"source":texture.resource_path}
    return key
func matrix(node):
    var t = node.global_transform
    return [t.x.x,t.x.y,t.y.x,t.y.y,t.origin.x,t.origin.y]
func material(node):
    if not node.material is ShaderMaterial:return {}
    var m = node.material
    var shader = m.shader
    var key = str(shader.get_instance_id())
    if not shaders.has(key):
        var name = "shader_%02d.glsl" % shaders.size()
        var file = FileAccess.open(out + "/" + name,FileAccess.WRITE)
        file.store_string(shader.code);file.close()
        shaders[key] = {"file":name,"source":shader.resource_path}
        var regex = RegEx.new();regex.compile("uniform\\s+(\\w+)\\s+(\\w+)")
        uniform_cache[key] = []
        for result in regex.search_all(shader.code):uniform_cache[key].append(result.get_string(2))
    var uniforms = {}
    for name in uniform_cache[key]:
        var value = m.get_shader_parameter(name)
        if value != null:uniforms[name] = arr(value)
    return {"shader":key,"uniforms":uniforms}
func points(values):
    var result = []
    for v in values:result.append([v.x,v.y])
    return result
func binary_blob(bytes:PackedByteArray)->String:
    var hash_context = HashingContext.new();hash_context.start(HashingContext.HASH_SHA256);hash_context.update(bytes)
    var key = hash_context.finish().hex_encode()
    if not binary_files.has(key):
        var name = "geometry_" + key + ".bin.gz"
        var file = FileAccess.open(out + "/" + name,FileAccess.WRITE)
        file.store_buffer(bytes.compress(FileAccess.COMPRESSION_GZIP));file.close()
        binary_files[key] = name
    return binary_files[key]
func traverse(node, parent_z, parent_color, draws):
    var z = parent_z
    var color = parent_color
    if node is CanvasItem:
        if not node.is_visible_in_tree():return
        z = parent_z + node.z_index if node.z_as_relative else node.z_index
        color *= node.modulate
    if (node is Sprite2D or node is Polygon2D or node is MeshInstance2D) and node.texture != null:
        var texture = node.texture
        var item = {"name":str(rig.get_path_to(node)),"z":z,"matrix":matrix(node),"color":arr(color * node.self_modulate),"material":material(node)}
        if item.color[3] > 0.000001:
            if node is Sprite2D:
                var rect = node.get_rect()
                item.vertices = [[rect.position.x,rect.position.y],[rect.end.x,rect.position.y],[rect.end.x,rect.end.y],[rect.position.x,rect.end.y]]
                item.triangles = [[0,1,2],[0,2,3]]
                if texture is AtlasTexture:
                    var uvrect = texture.region
                    var size = texture.atlas.get_size()
                    item.uv = [[uvrect.position.x/size.x,uvrect.position.y/size.y],[uvrect.end.x/size.x,uvrect.position.y/size.y],[uvrect.end.x/size.x,uvrect.end.y/size.y],[uvrect.position.x/size.x,uvrect.end.y/size.y]]
                    texture = texture.atlas
                else:item.uv = [[0,0],[1,0],[1,1],[0,1]]
            elif node is MeshInstance2D:
                assert(node.mesh.get_surface_count()==1,"Unexpected multi-surface mesh")
                var mesh_arrays = node.mesh.surface_get_arrays(0)
                var vertex_2d = PackedVector2Array()
                for vertex in mesh_arrays[Mesh.ARRAY_VERTEX]:vertex_2d.append(Vector2(vertex.x,vertex.y))
                item.vertex_file = binary_blob(vertex_2d.to_byte_array())
                item.uv_file = binary_blob(mesh_arrays[Mesh.ARRAY_TEX_UV].to_byte_array())
                item.index_file = binary_blob(mesh_arrays[Mesh.ARRAY_INDEX].to_byte_array())
            else:
                item.vertices = points(node.polygon)
                item.uv = []
                for uv in node.uv:item.uv.append([uv.x/texture.get_width(),uv.y/texture.get_height()])
                item.triangles = []
                if node.polygons.size():
                    for tri in node.polygons:item.triangles.append(Array(tri))
                else:
                    var tri = Geometry2D.triangulate_polygon(node.polygon)
                    for index in range(0,tri.size(),3):item.triangles.append([tri[index],tri[index+1],tri[index+2]])
            item.texture = save_texture(texture)
            var key = JSON.stringify(item)
            if not draw_indices.has(key):
                draw_indices[key] = draw_states.size();draw_states.append(item)
            draws.append(draw_indices[key])
    for child in node.get_children():traverse(child,z,color,draws)
func run():
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--output="):out = arg.trim_prefix("--output=")
        elif arg.begins_with("--expression="):only = arg.trim_prefix("--expression=")
        elif arg.begins_with("--fps="):fps = int(arg.trim_prefix("--fps="))
    DirAccess.make_dir_recursive_absolute(out)
    rig = load("res://full_body/full_body_rig.tscn").instantiate();root.add_child(rig)
    if not rig.ready_for_controls:push_error(rig.last_error);quit(1);return
    rig.set_physics_process(false);rig.expression_rig.set_process(false)
    var catalogue = rig.list_expressions()
    for entry in catalogue:
        if only != "all" and entry.id != only:continue
        rig.reset()
        if not rig.play_expression(entry.id):push_error(rig.last_error);quit(1);return
        var duration = rig.expression_rig.registry.definition(entry.id).duration
        for frame in range(int(ceil(duration*fps))+1):
            if frame > 0:rig.expression_rig.advance(1.0/fps)
            # Actual opening components queue obsolete dense meshes for freeing.
            # Allow that queue to drain with all automatic animation disabled.
            await process_frame
            var draws = []
            traverse(rig,0,Color.WHITE,draws)
            frames.append({"id":entry.id,"title":entry.title,"time":minf(frame/float(fps),duration),"duration":duration,"phase":rig.expression_rig.performance_phase,"pose":rig.expression_rig.pose_now(),"draws":draws,"head_matrix":matrix(rig.expression_rig.head)})
        print("SAMPLED_LIVE_FACE ",entry.id," frames=",frames.size()," states=",draw_states.size())
    var file = FileAccess.open(out + "/scene.json",FileAccess.WRITE)
    file.store_string(JSON.stringify({"source":"Actual Godot 4.6.3 full_body_rig scene: original expression controller, global transforms, draw geometry, colors, shader parameters and texture pixels. This is draw-state evidence, not native rendered pixel evidence.","fps":fps,"canvas":rig.registration.canvas,"catalogue":catalogue,"textures":textures,"shaders":shaders,"draw_states":draw_states,"frames":frames}));file.close()
    print("LIVE_FACE_SAMPLE_PASS frames=",frames.size()," textures=",textures.size()," shaders=",shaders.size());quit()
