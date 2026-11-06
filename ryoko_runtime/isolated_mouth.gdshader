shader_type canvas_item;
render_mode unshaded;
uniform sampler2D cleared_mouth:filter_linear,repeat_disable;
uniform sampler2D oral_feature:filter_linear_mipmap,repeat_disable;
uniform vec2 oral_size=vec2(178.0,130.0);
uniform vec2 oral_pivot=vec2(90.5,62.0);
uniform vec2 oral_scale=vec2(1.0);
uniform float oral_curve=0.0;
uniform vec2 oral_shift=vec2(0.0);
// EXP-005 source-specific immovable nose/jaw guards in patch coordinates.
uniform vec4 oral_guard=vec4(15.0,2.0,167.0,124.0);
uniform vec4 nose_guard=vec4(53.0,0.0,129.0,10.0);
void fragment() {
    vec4 original=texture(TEXTURE,UV);
    if(length(oral_scale-vec2(1.0))<0.000001 && abs(oral_curve)<0.000001 && length(oral_shift)<0.000001) {
        COLOR=original;
    } else {
        vec2 p=UV*oral_size;
        vec2 q=(p-oral_pivot-oral_shift)/oral_scale+oral_pivot;
        q.y+=oral_curve*8.0*smoothstep(12.0,52.0,abs(q.x-oral_pivot.x));
        vec4 feature=vec4(0.0);
        if(q.x>=0.0 && q.y>=0.0 && q.x<oral_size.x && q.y<oral_size.y)feature=texture(oral_feature,q/oral_size);
        vec3 skin=texture(cleared_mouth,UV).rgb;
        // Composite within the ORIGINAL patch coverage, not two alpha-over
        // sprites. Face skin, nose, jaw and neck geometry are never moved.
        bool protected_pixel=p.x<oral_guard.x || p.x>=oral_guard.z || p.y<oral_guard.y || p.y>=oral_guard.w;
        protected_pixel=protected_pixel || (p.x>=nose_guard.x && p.x<nose_guard.z && p.y>=nose_guard.y && p.y<nose_guard.w);
        COLOR=protected_pixel ? original : vec4(mix(skin,feature.rgb,feature.a),original.a);
    }
}
