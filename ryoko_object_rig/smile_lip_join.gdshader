shader_type canvas_item;
render_mode unshaded;
// Explicit inferred hidden joint material, fixed native cross-section and UV.
uniform vec2 left_top=vec2(0.0,-14.0);
uniform vec2 left_bottom=vec2(0.0,31.0);
uniform vec2 right_top=vec2(0.0,-14.0);
uniform vec2 right_bottom=vec2(0.0,31.0);
uniform float source_x=40.0;
uniform vec2 atlas_origin_px=vec2(0.0);
uniform bool upper_lip=false;
uniform float opening=0.0;
uniform float smile=0.0;
uniform vec2 joint_origin=vec2(565.0,634.0);
uniform float angle=0.0;
uniform sampler2D seam_texture : filter_linear, repeat_disable;
void fragment(){
 vec4 p=texture(TEXTURE,UV);
 float x=UV.x/TEXTURE_PIXEL_SIZE.x-atlas_origin_px.x-6.0;
 float y=UV.y/TEXTURE_PIXEL_SIZE.y-atlas_origin_px.y;
 float ly=y-14.0;
 float left=mix(left_top.x,left_bottom.x,(ly-left_top.y)/max(.001,left_bottom.y-left_top.y));
 float right=mix(right_top.x,right_bottom.x,(ly-right_top.y)/max(.001,right_bottom.y-right_top.y));
 float width=max(0.0,right-left);
 float coverage=clamp(min(x-left+.75,right-x+.75),0.0,1.0)*min(width*2.0,1.0);
 if(!upper_lip){
  float o=opening*(1.0-smile);
  float width=38.0-12.0*o;
  float hx=clamp(abs(source_x-39.5)/width,0.0,1.0);
  float curve=sqrt(max(0.0,1.0-pow(hx,4.0)));
  float local_seam=620.0+texture(seam_texture,vec2(source_x/80.0,.5)).r*63.75-634.0+1.0;
  vec2 edge_point=mat2(vec2(cos(angle),sin(angle)),vec2(-sin(angle),cos(angle)))*vec2(x,local_seam)+joint_origin;
  float current_width=mix(38.0-12.0*opening,35.5,smile);
  float h=clamp(abs(edge_point.x-564.5)/current_width,0.0,1.0);
  float current_curve=mix(sqrt(max(0.0,1.0-pow(h,4.0))),pow(max(0.0,1.0-h*h),.72),smile);
  float current_seam=620.0+texture(seam_texture,vec2(clamp((edge_point.x-525.0)/80.0,0.0,1.0),.5)).r*63.75-4.0*smile*pow(h,1.5);
  float contact_gap=edge_point.y-(current_seam+56.0*opening*current_curve);
  float ellipse=pow((source_x-39.5)/(50.0-30.0*pow(o,1.6)),2.0)+pow((y-20.0)/(100.0-89.0*pow(o,1.6)),2.0);
  coverage*=(1.0-smoothstep(.82,1.0,ellipse))*(1.0-smoothstep(.25+.75*pow(1.0-smile,4.0),1.5+4.5*pow(1.0-smile,4.0),contact_gap));
 }
 COLOR=vec4(p.rgb,p.a*coverage);
}
