shader_type canvas_item;
render_mode unshaded;
// Every owner uses fixed source UV. Only its Node2D pivot moves/rotates.
uniform float left_edge=0.0;
uniform float right_edge=80.0;
uniform bool upper_lip=true;
uniform bool corner=false;
uniform float opening=0.0;
uniform float smile=0.0;
uniform float joint_center=40.0;
uniform float offset_y=0.0;
uniform float angle=0.0;
uniform sampler2D seam_texture : filter_linear, repeat_disable;
void fragment(){
 vec4 pixel=texture(TEXTURE,UV);
 float sx=UV.x/TEXTURE_PIXEL_SIZE.x;
 float y=UV.y/TEXTURE_PIXEL_SIZE.y;
 float seam=texture(seam_texture,vec2(UV.x,.5)).r*63.75;
 float lower_owner=smoothstep(seam+.45,seam+1.55,y)*smoothstep(8.5,9.5,sx)*(1.0-smoothstep(69.5,70.5,sx));
 if(true){
  float la=pixel.a*lower_owner;
  if(upper_lip){pixel.a=(pixel.a-la)/max(1.0-la,.000001);}
  else{pixel.a=la;}
 }
 if(!upper_lip){
  // At smile=0 this is exactly the existing yawn lower-lip coverage.
  // Releasing this spatial clipping follows the same continuous control.
  float o=opening*(1.0-smile);
  float width=38.0-12.0*o;
  float px=525.0+sx;
  float hx=clamp(abs(px-564.5)/width,0.0,1.0);
  float boundary_curve=sqrt(max(0.0,1.0-pow(hx,4.0)));
  vec2 edge_point=vec2(sx-joint_center,seam+1.0-14.0);
  edge_point=mat2(vec2(cos(angle),sin(angle)),vec2(-sin(angle),cos(angle)))*edge_point+vec2(525.0+joint_center,634.0+offset_y);
  float current_width=mix(38.0-12.0*opening,35.5,smile);
  float h=clamp(abs(edge_point.x-564.5)/current_width,0.0,1.0);
  float current_curve=mix(sqrt(max(0.0,1.0-pow(h,4.0))),pow(max(0.0,1.0-h*h),.72),smile);
  float current_seam=620.0+texture(seam_texture,vec2(clamp((edge_point.x-525.0)/80.0,0.0,1.0),.5)).r*63.75-4.0*smile*pow(h,1.5);
  float contact_gap=edge_point.y-(current_seam+56.0*opening*current_curve);
  float ellipse_h=100.0-89.0*pow(o,1.6);
  float ellipse_w=50.0-30.0*pow(o,1.6);
  float ellipse=pow((px-564.5)/ellipse_w,2.0)+pow((y-20.0)/ellipse_h,2.0);
  pixel.a*=(1.0-smoothstep(.82,1.0,ellipse))*(1.0-smoothstep(.25+.75*pow(1.0-smile,4.0),1.5+4.5*pow(1.0-smile,4.0),contact_gap));
 }
 float wl=smoothstep(left_edge-.75,left_edge+.75,sx);
 float wr=1.0-smoothstep(right_edge-.75,right_edge+.75,sx);
 float weight=max(0.0,wl+wr-1.0);
 // Static factorization across adjacent strips, never emotion opacity.
 pixel.a=pixel.a*weight/max(1.0-pixel.a*(1.0-wr),.000001);
 COLOR=pixel;
}
