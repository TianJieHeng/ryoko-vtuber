shader_type canvas_item;
uniform float head_tilt = 0.0;
uniform vec2 head_offset = vec2(0.0);
uniform float spine_tilt = 0.0;
uniform vec2 torso_offset = vec2(0.0);
uniform vec2 chest_offset = vec2(0.0);
uniform float breath = 0.0;
uniform float controlled_breath = 0.0;
uniform vec2 hair_offset = vec2(0.0);
vec2 rotate_point(vec2 p,float angle) {
    float c=cos(angle);float s=sin(angle);
    return vec2(c*p.x-s*p.y,s*p.x+c*p.y);
}
void vertex() {
    vec2 rest=VERTEX;
    // Crown/bun motion is rooted above the eyes. Facial geometry is untouched.
    vec2 hair_rest=rest+hair_offset*(1.0-smoothstep(120.0,330.0,rest.y));
    // Head deformation stops in the neck, ABOVE clavicles/shoulders.
    float head_weight=1.0-smoothstep(710.0,855.0,rest.y);
    vec2 head=rotate_point(hair_rest-vec2(568.0,790.0),head_tilt)+vec2(568.0,790.0)+head_offset;
    vec2 neck=mix(hair_rest,head,head_weight);
    // Shoulders, shirt, clavicles and chest share ONE rigid upper-torso frame.
    // Only the bottom abdomen blends back to the anchored lower edge.
    float torso_weight=1.0-smoothstep(1260.0,1384.0,rest.y);
    vec2 torso=rotate_point(neck-vec2(568.0,1340.0),spine_tilt)+vec2(568.0,1340.0)+torso_offset+vec2(0.0,-breath*1.2);
    // Broad full-chest follow-through remains below the shoulders. The shared
    // torso transform is still primary; neck, shoulders and bottom remain fixed.
    // A wide plateau carries both sides of the bust and shirt together;
    // taper only toward the outside jacket and anchored lower edge.
    float soft_weight=smoothstep(920.0,1050.0,rest.y)*(1.0-smoothstep(1280.0,1384.0,rest.y))*(1.0-smoothstep(310.0,480.0,abs(rest.x-568.0)));
    // Connected shoulder/chest lift and shallow rib expansion; face and base
    // are anchored. This is opt-in and never drives the chest spring.
    float lift=smoothstep(650.0,830.0,rest.y)*(1.0-smoothstep(1250.0,1384.0,rest.y));
    float ribs=smoothstep(850.0,1000.0,rest.y)*(1.0-smoothstep(1250.0,1384.0,rest.y));
    vec2 inhale=vec2((rest.x-568.0)*.012*ribs,-4.0*lift)*controlled_breath;
    VERTEX=mix(neck,torso,torso_weight)+chest_offset*soft_weight+rotate_point(inhale,spine_tilt);
}

// Rigid iris textures translate under fixed eyelid/hair aperture masks.
uniform bool ornament_separate = false;
uniform vec2 gaze_direction=vec2(0.0);
uniform vec2 gaze_open=vec2(0.0);
uniform sampler2D iris_screen_left;
uniform sampler2D iris_screen_right;
uniform sampler2D sclera_screen_left;
uniform sampler2D sclera_screen_right;
uniform sampler2D aperture_screen_left;
uniform sampler2D aperture_screen_right;
vec4 eye_layer(vec4 base,vec2 uv,vec2 shift,sampler2D iris,sampler2D sclera,sampler2D aperture) {
    float mask=texture(aperture,uv).r;
    vec4 bg=texture(sclera,uv);
    vec4 pupil=texture(iris,uv-shift);
    vec3 eye=mix(bg.rgb,pupil.rgb,pupil.a);
    return vec4(mix(base.rgb,eye,mask),base.a);
}
uniform vec2 brow_amount=vec2(0.0);
uniform bool brow_enabled=false;
uniform sampler2D brow_screen_left;
uniform sampler2D brow_screen_right;
uniform sampler2D brow_skin_screen_left;
uniform sampler2D brow_skin_screen_right;
uniform sampler2D brow_allow_screen_left;
uniform sampler2D brow_allow_screen_right;
vec4 brow_layer(vec4 base,vec2 uv,float amount,sampler2D brow,sampler2D skin,sampler2D allow) {
    if(abs(amount)<.00001)return base;
    vec4 bg=texture(skin,uv);
    vec3 cleared=mix(base.rgb,bg.rgb,bg.a);
    vec4 moved=texture(brow,uv+vec2(0.0,amount*5.0/1384.0));
    float a=moved.a*texture(allow,uv).r;
    return vec4(mix(cleared,moved.rgb,a),base.a);
}
uniform vec2 earring_separate=vec2(0.0);
uniform sampler2D earring_underpaint;
uniform sampler2D earring_clear_masks;
void fragment() {
    vec4 base=texture(TEXTURE,UV);
    {
        vec2 shift=gaze_direction*vec2(7.0,2.0)/vec2(1136.0,1384.0);
        if(gaze_open.x>.5)base=eye_layer(base,UV,shift,iris_screen_left,sclera_screen_left,aperture_screen_left);
        if(gaze_open.y>.5)base=eye_layer(base,UV,shift,iris_screen_right,sclera_screen_right,aperture_screen_right);
    }
    if(brow_enabled) {
        base=brow_layer(base,UV,brow_amount.x,brow_screen_left,brow_skin_screen_left,brow_allow_screen_left);
        base=brow_layer(base,UV,brow_amount.y,brow_screen_right,brow_skin_screen_right,brow_allow_screen_right);
    }
    if(earring_separate.x>.5)base=mix(base,texture(earring_underpaint,UV),texture(earring_clear_masks,UV).r);
    if(earring_separate.y>.5)base=mix(base,texture(earring_underpaint,UV),texture(earring_clear_masks,UV).g);
    // The existing hanging ornament is rendered as a rigid, pivoted cutout.
    // Only its isolated source rectangle is removed; the pin stays attached.
    vec2 px=UV*vec2(1136.0,1384.0);
    if(ornament_separate && px.x>=781.0 && px.x<803.0 && px.y>=184.0 && px.y<315.0)base=vec4(0.0);
    COLOR=base;
}
