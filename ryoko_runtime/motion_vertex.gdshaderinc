uniform float head_tilt = 0.0;
uniform vec2 head_offset = vec2(0.0);
uniform float spine_tilt = 0.0;
uniform vec2 torso_offset = vec2(0.0);
uniform vec2 chest_offset = vec2(0.0);
uniform float breath = 0.0;
uniform float controlled_breath = 0.0;
uniform vec2 hair_offset = vec2(0.0);
uniform vec2 loose_hair_left = vec2(0.0);
uniform vec2 loose_hair_right = vec2(0.0);
vec2 rotate_point(vec2 p,float angle) {
    float c=cos(angle);float s=sin(angle);
    return vec2(c*p.x-s*p.y,s*p.x+c*p.y);
}
void vertex() {
    vec2 rest=VERTEX;
    // Crown/bun motion is rooted above the eyes. Facial geometry is untouched.
    vec2 hair_rest=rest+hair_offset*(1.0-smoothstep(120.0,330.0,rest.y));
    // Only lower OUTER locks. Roots, face, earrings and collar are excluded.
    float tips=smoothstep(600.0,690.0,rest.y)*(1.0-smoothstep(750.0,795.0,rest.y));
    float loose_left=tips*(1.0-smoothstep(335.0,390.0,rest.x));
    float loose_right=tips*smoothstep(746.0,790.0,rest.x);
    hair_rest+=loose_hair_left*loose_left+loose_hair_right*loose_right;
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

