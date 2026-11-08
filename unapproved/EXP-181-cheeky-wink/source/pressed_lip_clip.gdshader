shader_type canvas_item;
render_mode unshaded;
// Inferred hidden inner-upper-lip tissue. Pigment uses fixed native UV.
// Its upper-lip parent alone translates/rotates; no UV or mesh deformation.
uniform float left_edge=0.0;
uniform float right_edge=80.0;
uniform float joint_center=40.0;
uniform vec2 joint_origin=vec2(565.0,634.0);
uniform float angle=0.0;
uniform float opening=0.0;
uniform float smile=0.0;
uniform float spread=0.0;
uniform float purse=0.0;
uniform float corner_lift=0.0;
uniform vec2 corner_lift_sides=vec2(0.0);
uniform float lip_press=0.0;
uniform sampler2D seam_texture : filter_linear, repeat_disable;
// New side channels use only the unspent old 12px corner-lift budget.
// The source radius follows rigid spread/purse coordinates. Pigment UV is untouched.
float independent_corner_delta(float screen_x){
 float side=screen_x<564.5 ? corner_lift_sides.x : corner_lift_sides.y;
 if(side<=0.0){return 0.0;}
 float r=clamp(abs((screen_x-564.5)/(35.5+20.0*spread-14.0*purse)),0.0,1.0);
 return -12.0*(1.0-corner_lift)*side*r*r*r;
}
void fragment(){
 vec4 pigment=texture(TEXTURE,UV);
 vec2 src=UV/TEXTURE_PIXEL_SIZE;
 vec2 p=mat2(vec2(cos(angle),sin(angle)),vec2(-sin(angle),cos(angle)))*vec2(src.x-joint_center,src.y-14.0)+joint_origin;
 float source_x=spread==0.0 ? p.x-525.0 : 39.5+(p.x-564.5)/(1.0+20.0*spread/35.5);
 if(purse>0.0){source_x=39.5+(p.x-564.5)/(1.0+20.0*spread/35.5-14.0*purse/35.5);}
 float width=mix(38.0-12.0*opening,35.5,smile)+20.0*spread;
 if(purse>0.0){width-=14.0*purse;}
 float h=clamp(abs(p.x-564.5)/width,0.0,1.0);
 float r=clamp(abs((p.x-564.5)/(35.5+20.0*spread)),0.0,1.0);
 if(purse>0.0){r=clamp(abs((p.x-564.5)/(35.5+20.0*spread-14.0*purse)),0.0,1.0);}
 float seam=620.0+texture(seam_texture,vec2(clamp(source_x/80.0,0.0,1.0),.5)).r*63.75-4.0*spread-(4.0+5.0*spread)*smile*pow(h,1.5)-12.0*corner_lift*r*r*r;
 float curve=mix(sqrt(max(0.0,1.0-pow(h,4.0))),pow(max(0.0,1.0-h*h),.72),smile);
 if(purse>0.0){seam+=purse*(4.0+8.0*r*r);curve=mix(curve,sqrt(max(0.0,1.0-h*h)),purse);}
 if(corner_lift_sides!=vec2(0.0)){seam+=independent_corner_delta(p.x);}
 float inside=clamp(min(p.y-seam,seam+56.0*opening*curve-p.y),0.0,1.0);
 float depth=4.0*lip_press;
 float tissue=clamp(min(p.y-seam,seam+depth-p.y)/.75,0.0,1.0);
 float side=clamp((width-abs(p.x-564.5))/.7,0.0,1.0);
 // Shared spatial boundaries partition overlapping fixed native hidden
 // pigment. This fills rigid-owner gaps without stretching source UV.
 float wl=smoothstep(left_edge-.75,left_edge+.75,source_x);
 float wr=1.0-smoothstep(right_edge-.75,right_edge+.75,source_x);
 float weight=max(0.0,wl+wr-1.0);
 pigment.a*=inside*tissue*side;
 pigment.a=pigment.a*weight/max(1.0-pigment.a*(1.0-wr),.000001);
 COLOR=pigment;
}
