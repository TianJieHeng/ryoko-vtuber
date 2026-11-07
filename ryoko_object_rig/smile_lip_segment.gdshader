shader_type canvas_item;
render_mode unshaded;
// Every owner uses fixed source UV. Only its Node2D pivot moves/rotates.
uniform float left_edge=0.0;
uniform float right_edge=80.0;
uniform bool upper_lip=true;
uniform bool corner=false;
uniform float opening=0.0;
uniform float smile=0.0;
uniform float spread=0.0;
uniform float offset_x=0.0;
uniform float joint_center=40.0;
uniform float offset_y=0.0;
uniform float angle=0.0;
// These fixed-owner transforms query the lower peer's coverage only. The
// rendered pigment always samples this owner's unchanged native source UV.
uniform vec2 lower_peer_x=vec2(1.0,0.0);
uniform vec2 lower_peer_y=vec2(0.0,1.0);
uniform vec2 lower_peer_origin=vec2(0.0);
uniform float lower_peer_angle=0.0;
uniform vec2 lower_peer_offset=vec2(0.0);
uniform sampler2D seam_texture : filter_linear, repeat_disable;
float lower_geometry_mask(float sx,float y,float own_angle,vec2 own_offset){
  float seam=texture(seam_texture,vec2(sx/80.0,.5)).r*63.75;
  // At smile=0 this is exactly the existing yawn lower-lip coverage.
  // Releasing this spatial clipping follows the same continuous control.
  float o=opening*(1.0-smile);
  float width=38.0-12.0*o;
  float px=525.0+sx;
  float hx=clamp(abs(px-564.5)/width,0.0,1.0);
  float boundary_curve=sqrt(max(0.0,1.0-pow(hx,4.0)));
  vec2 edge_point=vec2(sx-joint_center,seam+1.0-14.0);
  edge_point=mat2(vec2(cos(own_angle),sin(own_angle)),vec2(-sin(own_angle),cos(own_angle)))*edge_point+vec2(525.0+joint_center+own_offset.x,634.0+own_offset.y);
  float current_width=mix(38.0-12.0*opening,35.5,smile)+20.0*spread;
  float h=clamp(abs(edge_point.x-564.5)/current_width,0.0,1.0);
  float current_curve=mix(sqrt(max(0.0,1.0-pow(h,4.0))),pow(max(0.0,1.0-h*h),.72),smile);
  float current_seam=620.0+texture(seam_texture,vec2(clamp((spread==0.0 ? (edge_point.x-525.0) : (39.5+(edge_point.x-564.5)/(1.0+20.0*spread/35.5)))/80.0,0.0,1.0),.5)).r*63.75-4.0*spread-(4.0+5.0*spread)*smile*pow(h,1.5);
  float contact_gap=edge_point.y-(current_seam+56.0*opening*current_curve);
  float ellipse_h=100.0-89.0*pow(o,1.6);
  float ellipse_w=50.0-30.0*pow(o,1.6);
  float ellipse=pow((px-564.5)/ellipse_w,2.0)+pow((y-20.0)/ellipse_h,2.0);
  return (1.0-smoothstep(.82,1.0,ellipse))*(1.0-smoothstep(.25+.75*pow(1.0-smile,4.0),1.5+4.5*pow(1.0-smile,4.0),contact_gap));

}
float source_lower_weight(float sx,float y){
 float seam=texture(seam_texture,vec2(sx/80.0,.5)).r*63.75;
 return smoothstep(seam+.45,seam+1.55,y)*smoothstep(8.5,9.5,sx)*(1.0-smoothstep(69.5,70.5,sx));
}
void fragment(){
 vec4 pixel=texture(TEXTURE,UV);
 float sx=UV.x/TEXTURE_PIXEL_SIZE.x;
 float y=UV.y/TEXTURE_PIXEL_SIZE.y;
 float seam=texture(seam_texture,vec2(UV.x,.5)).r*63.75;
 float lower_owner=smoothstep(seam+.45,seam+1.55,y)*smoothstep(8.5,9.5,sx)*(1.0-smoothstep(69.5,70.5,sx));
 if(true){
  float la=pixel.a*lower_owner;
  if(upper_lip){
   vec2 peer=lower_peer_x*sx+lower_peer_y*y+lower_peer_origin;
   float peer_alpha=0.0;
   if(peer.x>=0.0 && peer.x<=80.0 && peer.y>=0.0 && peer.y<=45.0){
    peer_alpha=texture(TEXTURE,peer*TEXTURE_PIXEL_SIZE).a*source_lower_weight(peer.x,peer.y)*lower_geometry_mask(peer.x,peer.y,lower_peer_angle,lower_peer_offset);
   }
   // Compensation is valid only where the separately transformed lower
   // source owner still covers this pixel. A separated lip has a genuinely
   // antialiased observed perimeter, not an opaque (a-la)/(1-la) cliff.
   pixel.a=clamp((pixel.a-la)/max(1.0-peer_alpha,.000001),0.0,1.0);
  }
  else{pixel.a=la;}
 }
 if(!upper_lip){pixel.a*=lower_geometry_mask(sx,y,angle,vec2(offset_x,offset_y));}
 float wl=smoothstep(left_edge-.75,left_edge+.75,sx);
 float wr=1.0-smoothstep(right_edge-.75,right_edge+.75,sx);
 float weight=max(0.0,wl+wr-1.0);
 // Static factorization across adjacent strips, never emotion opacity.
 pixel.a=pixel.a*weight/max(1.0-pixel.a*(1.0-wr),.000001);
 COLOR=pixel;
}
