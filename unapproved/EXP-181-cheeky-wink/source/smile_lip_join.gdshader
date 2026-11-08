shader_type canvas_item;
render_mode unshaded;
// Explicit inferred hidden joint material, fixed native cross-section and UV.
uniform vec2 left_top=vec2(0.0,-14.0);
uniform vec2 left_bottom=vec2(0.0,31.0);
uniform vec2 right_top=vec2(0.0,-14.0);
uniform vec2 right_bottom=vec2(0.0,31.0);
uniform float source_x=40.0;
uniform float half_width=6.0;
uniform bool outer_extension=false;
uniform sampler2D previous_sleeve_texture : filter_linear, repeat_disable;
uniform vec2 previous_atlas_origin_px=vec2(0.0);
uniform vec2 baseline_left_top=vec2(0.0,-14.0);
uniform vec2 baseline_left_bottom=vec2(0.0,31.0);
uniform vec2 baseline_right_top=vec2(0.0,-14.0);
uniform vec2 baseline_right_bottom=vec2(0.0,31.0);
uniform vec2 atlas_origin_px=vec2(0.0);
uniform bool upper_lip=false;
uniform float opening=0.0;
uniform float smile=0.0;
uniform float spread=0.0;
uniform float purse=0.0;
uniform float corner_lift=0.0;
uniform vec2 corner_lift_sides=vec2(0.0);
uniform vec2 joint_origin=vec2(565.0,634.0);
uniform float angle=0.0;
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
 vec4 p=texture(TEXTURE,UV);
 float x=UV.x/TEXTURE_PIXEL_SIZE.x-atlas_origin_px.x-half_width;
 float y=UV.y/TEXTURE_PIXEL_SIZE.y-atlas_origin_px.y;
 float ly=y-14.0;
 float left=mix(left_top.x,left_bottom.x,(ly-left_top.y)/max(.001,left_bottom.y-left_top.y));
 float right=mix(right_top.x,right_bottom.x,(ly-right_top.y)/max(.001,right_bottom.y-right_top.y));
 float width=max(0.0,right-left);
 float coverage=clamp(min(x-left+.75,right-x+.75),0.0,1.0)*min(width*2.0,1.0);
 if(!upper_lip){
  float o=opening*(1.0-smile);
  if(purse>0.0){o*=1.0-purse;}
  float width=38.0-12.0*o;
  float hx=clamp(abs(source_x-39.5)/width,0.0,1.0);
  float curve=sqrt(max(0.0,1.0-pow(hx,4.0)));
  float local_seam=620.0+texture(seam_texture,vec2(source_x/80.0,.5)).r*63.75-634.0+1.0;
  vec2 edge_point=mat2(vec2(cos(angle),sin(angle)),vec2(-sin(angle),cos(angle)))*vec2(x,local_seam)+joint_origin;
  float current_width=mix(38.0-12.0*opening,35.5,smile)+20.0*spread;
  if(purse>0.0){current_width-=14.0*purse;}
  float h=clamp(abs(edge_point.x-564.5)/current_width,0.0,1.0);
  float current_curve=mix(sqrt(max(0.0,1.0-pow(h,4.0))),pow(max(0.0,1.0-h*h),.72),smile);
  float current_seam=620.0+texture(seam_texture,vec2(clamp((spread==0.0 ? (edge_point.x-525.0) : (39.5+(edge_point.x-564.5)/(1.0+20.0*spread/35.5)))/80.0,0.0,1.0),.5)).r*63.75-4.0*spread-(4.0+5.0*spread)*smile*pow(h,1.5)-12.0*corner_lift*pow(clamp(abs((edge_point.x-564.5)/(35.5+20.0*spread)),0.0,1.0),3.0);
  if(purse>0.0){
   float r=clamp(abs((edge_point.x-564.5)/(35.5+20.0*spread-14.0*purse)),0.0,1.0);
   float native_x=39.5+(edge_point.x-564.5)/(1.0+20.0*spread/35.5-14.0*purse/35.5);
   current_seam=620.0+texture(seam_texture,vec2(clamp(native_x/80.0,0.0,1.0),.5)).r*63.75-4.0*spread-(4.0+5.0*spread)*smile*pow(h,1.5)-12.0*corner_lift*r*r*r+purse*(4.0+8.0*r*r);
   current_curve=mix(current_curve,sqrt(max(0.0,1.0-h*h)),purse);
  }
  if(corner_lift_sides!=vec2(0.0)){current_seam+=independent_corner_delta(edge_point.x);}
  float contact_gap=edge_point.y-(current_seam+56.0*opening*current_curve);
  float ellipse=pow((source_x-39.5)/(50.0-30.0*pow(o,1.6)),2.0)+pow((y-20.0)/(100.0-89.0*pow(o,1.6)),2.0);
  coverage*=(1.0-smoothstep(.82,1.0,ellipse))*(1.0-smoothstep(.25+.75*pow(1.0-smile,4.0),1.5+4.5*pow(1.0-smile,4.0),contact_gap));
 }
 float alpha=p.a*coverage;
 if(outer_extension){
  vec2 previous_uv=(previous_atlas_origin_px+vec2(x+6.0,y))/vec2(textureSize(previous_sleeve_texture,0));
  float previous_alpha=texture(previous_sleeve_texture,previous_uv).a*coverage;
  if(abs(x)>=10.0 || y<0.0 || y>=45.0){previous_alpha=0.0;}
  // Local geometry, not expression opacity: no extension is exposed until
  // the actual endpoint gap reaches the previous sleeve edge. Each row
  // derives its boundary from both rigid owners' transformed edge lines.
  float baseline_left=mix(baseline_left_top.x,baseline_left_bottom.x,(ly-baseline_left_top.y)/max(.001,baseline_left_bottom.y-baseline_left_top.y));
  float baseline_right=mix(baseline_right_top.x,baseline_right_bottom.x,(ly-baseline_right_top.y)/max(.001,baseline_right_bottom.y-baseline_right_top.y));
  float extra_gap=max(abs(left),abs(right))-max(abs(baseline_left),abs(baseline_right));
  float support_reveal=smoothstep(0.0,.75,extra_gap);
  float target_alpha=previous_alpha+max(0.0,alpha-previous_alpha)*support_reveal;
  alpha=max(0.0,target_alpha-previous_alpha)/max(1.0-previous_alpha,.000001);
 }
 COLOR=vec4(p.rgb,alpha);
}
