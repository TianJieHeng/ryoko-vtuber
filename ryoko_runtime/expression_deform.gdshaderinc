// Facial feature rig in registered source pixels. Zero values are exact identity.
// Inverse-sampled local deformations keep outer skin/hair boundaries anchored.
uniform bool expression_deform_active = false;
uniform vec2 expression_eye = vec2(0.0);
uniform vec2 expression_brow = vec2(0.0);
uniform vec2 expression_brow_tilt = vec2(0.0);
uniform vec3 expression_mouth = vec3(0.0); // open, width, corner lift
uniform vec2 expression_mouth_shift = vec2(0.0);
uniform vec2 expression_cheek = vec2(0.0);
float feature_weight(vec2 p, vec2 center, vec2 radius) {
    vec2 q=(p-center)/radius;
    return 1.0-smoothstep(0.55,1.0,length(q));
}
// Piecewise monotonic map: compress/expand the mouth core while anchoring
// surrounding skin. Unlike a Gaussian displacement, large closure cannot fold
// UVs or repeat teeth along the feathered boundary.
float mouth_vertical(float y,float amount) {
    float core=amount<0.0 ? 60.0 : 36.0;
    float edge=87.0;
    float scale=1.0+amount*(amount>=0.0 ? 0.50 : 0.90);
    float moving_core=core*scale;
    float ay=abs(y);
    if(ay>=edge)return y;
    float mapped=ay<moving_core ? ay/scale : core+(ay-moving_core)*(edge-core)/(edge-moving_core);
    return sign(y)*mapped;
}
vec2 expression_uv(vec2 uv) {
    vec2 p=uv*vec2(1136.0,1384.0);
    vec2 shift=vec2(0.0);
    // Squint changes the aperture about each fixed eye center, never scales
    // the whole face. Positive = squint; negative = wide-eyed recoil.
    vec2 left=vec2(466.0,501.0), right=vec2(668.0,501.0);
    float wl=feature_weight(p,left,vec2(87.0,55.0));
    float wr=feature_weight(p,right,vec2(87.0,55.0));
    shift.y+=(p.y-left.y)*expression_eye.x*0.38*wl;
    shift.y+=(p.y-right.y)*expression_eye.y*0.38*wr;
    // Both lift and inner/outer slope act on expression-specific brow pixels.
    float bl=feature_weight(p,vec2(473.0,435.0),vec2(83.0,36.0));
    float br=feature_weight(p,vec2(660.0,435.0),vec2(83.0,36.0));
    shift.y+=(expression_brow.x*9.0+expression_brow_tilt.x*(p.x-473.0)*0.20)*bl;
    shift.y+=(expression_brow.y*9.0-expression_brow_tilt.y*(p.x-660.0)*0.20)*br;
    // Shape the authored emotional mouth. During speech, the same restrained
    // expression offsets shape the existing viseme; they do not create phonemes.
    vec2 mouth=vec2(568.0,646.0);
    float mw=feature_weight(p,mouth,vec2(112.0,61.0));
    shift.x+=((p.x-mouth.x)*(-expression_mouth.y*0.18)-expression_mouth_shift.x*5.0)*mw;
    float corners=smoothstep(12.0,52.0,abs(p.x-mouth.x));
    float mouth_horizontal=1.0-smoothstep(64.0,112.0,abs(p.x-mouth.x));
    shift.y+=(mouth_vertical(p.y-mouth.y,expression_mouth.x)-(p.y-mouth.y))*mouth_horizontal;
    shift.y+=(expression_mouth.z*8.0*corners-expression_mouth_shift.y*4.0)*mw;
    shift.y+=expression_cheek.x*5.0*feature_weight(p,vec2(461.0,558.0),vec2(69.0,37.0));
    shift.y+=expression_cheek.y*5.0*feature_weight(p,vec2(673.0,558.0),vec2(69.0,37.0));
    return (p+shift)/vec2(1136.0,1384.0);
}
