shader_type canvas_item;
uniform float head_tilt = 0.0;
uniform vec2 head_offset = vec2(0.0);
uniform float spine_tilt = 0.0;
uniform vec2 torso_offset = vec2(0.0);
uniform vec2 chest_offset = vec2(0.0);
uniform float breath = 0.0;
vec2 rotate_point(vec2 p,float angle) {
    float c=cos(angle);float s=sin(angle);
    return vec2(c*p.x-s*p.y,s*p.x+c*p.y);
}
void vertex() {
    vec2 rest=VERTEX;
    // Head deformation stops in the neck, ABOVE clavicles/shoulders.
    float head_weight=1.0-smoothstep(710.0,855.0,rest.y);
    vec2 head=rotate_point(rest-vec2(568.0,790.0),head_tilt)+vec2(568.0,790.0)+head_offset;
    vec2 neck=mix(rest,head,head_weight);
    // Shoulders, shirt, clavicles and chest share ONE rigid upper-torso frame.
    // Only the bottom abdomen blends back to the anchored lower edge.
    float torso_weight=1.0-smoothstep(1260.0,1384.0,rest.y);
    vec2 torso=rotate_point(neck-vec2(568.0,1340.0),spine_tilt)+vec2(568.0,1340.0)+torso_offset+vec2(0.0,-breath*1.2);
    // Broad full-chest follow-through remains below the shoulders. The shared
    // torso transform is still primary; neck, shoulders and bottom remain fixed.
    // A wide plateau carries both sides of the bust and shirt together;
    // taper only toward the outside jacket and anchored lower edge.
    float soft_weight=smoothstep(920.0,1050.0,rest.y)*(1.0-smoothstep(1280.0,1384.0,rest.y))*(1.0-smoothstep(310.0,480.0,abs(rest.x-568.0)));
    VERTEX=mix(neck,torso,torso_weight)+chest_offset*soft_weight;
}
