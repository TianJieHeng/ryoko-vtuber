extends RefCounted
# Private bounded upper opening, exact approved repaired source, default zero.
var opening_px=0.0
var repaired_textures={}
var shared_opening_shader:Shader
var rig
var work=""
var out=""
var records=[]
var meshes=[]
var originals=[]
var old_iris_materials={}
var geometry=[]
func interp(image:Image,x:float)->float:
    var a=clampi(int(floor(x)),0,image.get_width()-1)
    var b=clampi(a+1,0,image.get_width()-1)
    return lerpf(image.get_pixel(a,0).r,image.get_pixel(b,0).r,x-floor(x))*255.0
func amplitude(x:float,bounds:Vector2)->float:
    if x<=bounds.x or x>=bounds.y:return 0.0
    return opening_px*pow(sin(PI*(x-bounds.x)/(bounds.y-bounds.x)),2.0)
func lift(p:Vector2,bounds:Vector2,upper:Image,lower:Image)->float:
    var t=interp(upper,p.x)
    var b=maxf(t+1.0,interp(lower,p.x)-2.0)
    return amplitude(p.x,bounds)*clampf((b-p.y)/(b-t),0.0,1.0)
func material(side:String,kind:int,bounds:Vector2):
    var ge=rig.face.gaze_manifest.eyes[side]
    var m=ShaderMaterial.new()
    if shared_opening_shader==null:
        shared_opening_shader=Shader.new()
        shared_opening_shader.code=FileAccess.get_file_as_string(work+"/transport.gdshader")
    m.shader=shared_opening_shader
    for key in ["profile_texture","shape_upper"]:m.set_shader_parameter(key,load("res://rig_assets/object_face/profile_"+side+".png"))
    for key in ["lower_profile_texture","shape_lower"]:m.set_shader_parameter(key,load("res://rig_assets/object_face/lower_profile_"+side+".png"))
    for key in ["aperture","iris","sclera"]:m.set_shader_parameter(key+"_texture",load("res://rig_assets/gaze_eyes/"+key+"_"+side+".png"))
    m.set_shader_parameter("iris_texture",repaired_textures[side])
    m.set_shader_parameter("eye_size",Vector2(ge.size[0],ge.size[1]))
    m.set_shader_parameter("iris_size",Vector2(ge.iris_size[0],ge.iris_size[1]))
    m.set_shader_parameter("iris_padding",Vector2(ge.iris_padding[0],ge.iris_padding[1]))
    m.set_shader_parameter("opening_px",opening_px)
    m.set_shader_parameter("bounds",bounds);m.set_shader_parameter("kind",kind)
    return m
func install_mesh(source,side:String,kind:int,bounds:Vector2):
    var size=source.texture.get_size()
    var upper=load("res://rig_assets/object_face/profile_"+side+".png").get_image()
    var lower=load("res://rig_assets/object_face/lower_profile_"+side+".png").get_image()
    var vertices=PackedVector3Array();var uvs=PackedVector2Array();var indices=PackedInt32Array()
    var nx=int(size.x*2.0)+1;var ny=int(size.y*2.0)+1;var peak=0.0
    for j in range(ny):
        for i in range(nx):
            var p=Vector2(float(i)*0.5,float(j)*0.5)
            var delta=lift(p-Vector2(0.5,0.5),bounds,upper,lower);peak=maxf(peak,delta)
            vertices.append(Vector3(p.x,p.y-delta,0.0));uvs.append(p/size)
    for j in range(ny-1):
        for i in range(nx-1):
            var a=j*nx+i
            for k in [a,a+1,a+nx+1,a,a+nx+1,a+nx]:indices.append(k)
    var arrays=[];arrays.resize(Mesh.ARRAY_MAX)
    arrays[Mesh.ARRAY_VERTEX]=vertices;arrays[Mesh.ARRAY_TEX_UV]=uvs;arrays[Mesh.ARRAY_INDEX]=indices
    var mesh=ArrayMesh.new();mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,arrays)
    var node=MeshInstance2D.new();node.name="private_transport_"+source.name
    node.mesh=mesh;node.texture=source.texture;node.position=source.position
    node.texture_filter=source.texture_filter;node.material=material(side,kind,bounds)
    source.get_parent().add_child(node);source.visible=false
    meshes.append(node);originals.append(source)
    geometry.append({"part":source.name,"vertices":vertices.size(),"triangles":indices.size()/3,"maximum_lift":peak,"bounds":[bounds.x,bounds.y]})
func install_opening(value:float):
    opening_px=clampf(value,0.0,4.0)
    # Opening is scoped to centered gaze with no closure. Safe handoff to existing anatomy.
    if rig.face.closure!=Vector2.ZERO or rig.face.gaze!=Vector2.ZERO:opening_px=0.0
    if opening_px==0.0:return
    for side in ["screen_left","screen_right"]:
        var bounds=Vector2(16.0,97.0) if side=="screen_left" else Vector2(10.0,85.0)
        install_mesh(rig.face.objects["sclera_"+side],side,0,bounds)
        install_mesh(rig.face.objects["upper_lash_"+side],side,1,bounds)
        var iris=rig.face.objects["iris_"+side]
        old_iris_materials[side]=iris.material;iris.material=material(side,2,bounds)
func restore():
    for node in meshes:node.visible=false
    for node in originals:node.visible=true
    for side in old_iris_materials:rig.face.objects["iris_"+side].material=old_iris_materials[side]
    for node in meshes:node.queue_free()
    meshes.clear();originals.clear();old_iris_materials.clear();opening_px=0.0
