shader_type canvas_item;
// Static-mouth replacement blend; one preserves the original geometry.
uniform float native_part_weight = 1.0;
render_mode unshaded;
// Every owner uses fixed source UV. Only its Node2D pivot moves/rotates.
uniform float left_edge=0.0;
uniform float right_edge=80.0;
uniform bool upper_lip=true;
uniform bool corner=false;
uniform float opening=0.0;
uniform float smile=0.0;
uniform float spread=0.0;
uniform float purse=0.0;
uniform float corner_lift=0.0;
uniform vec2 corner_lift_sides=vec2(0.0);
uniform vec2 width_sides=vec2(0.0);
// Return the old horizontal shape coordinate for the same source column.
// Width changes placement only: aperture, vertical style and all inherited
// bilateral/purse differences keep their old arithmetic. Pigment UV is fixed.
float legacy_shape_x(float screen_x){
 if(width_sides==vec2(0.0)){return screen_x;}
 float side=screen_x<564.5 ? width_sides.x : width_sides.y;
 float horizontal_spread=spread+(1.0-spread)*side;
 return 564.5+(screen_x-564.5)*(35.5+20.0*spread-14.0*purse)/(35.5+20.0*horizontal_spread-14.0*purse);
}
uniform float offset_x=0.0;
uniform float joint_center=40.0;
uniform float offset_y=0.0;
uniform float angle=0.0;
uniform vec2 neighbor_left_top=vec2(0.0,0.0);
uniform vec2 neighbor_left_bottom=vec2(0.0,45.0);
uniform vec2 neighbor_right_top=vec2(80.0,0.0);
uniform vec2 neighbor_right_bottom=vec2(80.0,45.0);
uniform vec2 baseline_left_top=vec2(0.0,0.0);
uniform vec2 baseline_left_bottom=vec2(0.0,45.0);
uniform vec2 baseline_right_top=vec2(80.0,0.0);
uniform vec2 baseline_right_bottom=vec2(80.0,45.0);
// These fixed-owner transforms query the lower peer's coverage only. The
// rendered pigment always samples this owner's unchanged native source UV.
uniform vec2 lower_peer_x=vec2(1.0,0.0);
uniform vec2 lower_peer_y=vec2(0.0,1.0);
uniform vec2 lower_peer_origin=vec2(0.0);
uniform float lower_peer_angle=0.0;
uniform vec2 lower_peer_offset=vec2(0.0);
uniform sampler2D seam_texture : filter_linear, repeat_disable;
// New side channels use only the unspent old 12px corner-lift budget.
// The source radius follows rigid spread/purse coordinates. Pigment UV is untouched.
float independent_corner_delta(float screen_x){
 screen_x=legacy_shape_x(screen_x);
 float side=screen_x<564.5 ? corner_lift_sides.x : corner_lift_sides.y;
 if(side<=0.0){return 0.0;}
 float r=clamp(abs((screen_x-564.5)/(35.5+20.0*spread-14.0*purse)),0.0,1.0);
 return -12.0*(1.0-corner_lift)*side*r*r*r;
}
float lower_geometry_mask(float sx,float y,float own_angle,vec2 own_offset){
  float seam=texture(seam_texture,vec2(sx/80.0,.5)).r*63.75;
  // At smile=0 this is exactly the existing yawn lower-lip coverage.
  // Releasing this spatial clipping follows the same continuous control.
  float o=opening*(1.0-smile);
  if(purse>0.0){o*=1.0-purse;}
  float width=38.0-12.0*o;
  float px=525.0+sx;
  float hx=clamp(abs(px-564.5)/width,0.0,1.0);
  float boundary_curve=sqrt(max(0.0,1.0-pow(hx,4.0)));
  vec2 edge_point=vec2(sx-joint_center,seam+1.0-14.0);
  edge_point=mat2(vec2(cos(own_angle),sin(own_angle)),vec2(-sin(own_angle),cos(own_angle)))*edge_point+vec2(525.0+joint_center+own_offset.x,634.0+own_offset.y);
  float mask_x=legacy_shape_x(edge_point.x);
  float current_width=mix(38.0-12.0*opening,35.5,smile)+20.0*spread;
  if(purse>0.0){current_width-=14.0*purse;}
  float h=clamp(abs(mask_x-564.5)/current_width,0.0,1.0);
  float current_curve=mix(sqrt(max(0.0,1.0-pow(h,4.0))),pow(max(0.0,1.0-h*h),.72),smile);
  float current_seam=620.0+texture(seam_texture,vec2(clamp((spread==0.0 ? (mask_x-525.0) : (39.5+(mask_x-564.5)/(1.0+20.0*spread/35.5)))/80.0,0.0,1.0),.5)).r*63.75-4.0*spread-(4.0+5.0*spread)*smile*pow(h,1.5)-12.0*corner_lift*pow(clamp(abs((mask_x-564.5)/(35.5+20.0*spread)),0.0,1.0),3.0);
  if(purse>0.0){
   float r=clamp(abs((mask_x-564.5)/(35.5+20.0*spread-14.0*purse)),0.0,1.0);
   float native_x=39.5+(mask_x-564.5)/(1.0+20.0*spread/35.5-14.0*purse/35.5);
   current_seam=620.0+texture(seam_texture,vec2(clamp(native_x/80.0,0.0,1.0),.5)).r*63.75-4.0*spread-(4.0+5.0*spread)*smile*pow(h,1.5)-12.0*corner_lift*r*r*r+purse*(4.0+8.0*r*r);
   current_curve=mix(current_curve,sqrt(max(0.0,1.0-h*h)),purse);
  }
  if(corner_lift_sides!=vec2(0.0)){current_seam+=independent_corner_delta(edge_point.x);}
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
// Oriented normal-distance intrusion remains finite as a rigid edge becomes
// horizontal or reverses. Its length remains 45 source pixels, never zero.
float boundary_intrusion(vec2 top,vec2 bottom,float edge,float y,float side){
 vec2 direction=bottom-top;
 vec2 query=vec2(edge,y)-top;
 return side*(direction.x*query.y-direction.y*query.x)/max(.001,length(direction));
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
 float clip_left=left_edge;
 float clip_right=right_edge;
 if(purse>0.0){
  float l=boundary_intrusion(neighbor_left_top,neighbor_left_bottom,left_edge,y,1.0);
  float r=boundary_intrusion(neighbor_right_top,neighbor_right_bottom,right_edge,y,-1.0);
  float bl=boundary_intrusion(baseline_left_top,baseline_left_bottom,left_edge,y,1.0);
  float br=boundary_intrusion(baseline_right_top,baseline_right_bottom,right_edge,y,-1.0);
  clip_left+=.5*max(0.0,max(0.0,l)-max(0.0,bl));
  clip_right-=.5*max(0.0,max(0.0,r)-max(0.0,br));
 }
 float wl=smoothstep(clip_left-.75,clip_left+.75,sx);
 float wr=1.0-smoothstep(clip_right-.75,clip_right+.75,sx);
 float weight=max(0.0,wl+wr-1.0);
 // Static factorization across adjacent strips, never emotion opacity.
 pixel.a=pixel.a*weight/max(1.0-pixel.a*(1.0-wr),.000001);
 COLOR=pixel;
 COLOR.a *= native_part_weight;
}
