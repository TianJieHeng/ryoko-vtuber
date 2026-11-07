shader_type canvas_item;
render_mode unshaded;
// Fixed UV, RGB and scale. Upper lashes alone are translated by the node controller.
uniform sampler2D profile_texture : filter_nearest, repeat_disable;
uniform sampler2D lower_profile_texture : filter_nearest, repeat_disable;
// Interior profiles and aperture live in stationary eye coordinates, not
// translating sprite UV. Only texture sampling and a rigid node translation
// move the iris. All RGB texels remain unchanged during motion.
uniform sampler2D aperture_texture : filter_linear, repeat_disable;
uniform sampler2D iris_texture : filter_linear, repeat_disable;
uniform vec2 eye_size = vec2(123.0,60.0);
uniform vec2 iris_size = vec2(147.0,92.0);
uniform vec2 iris_padding = vec2(12.0,16.0);
uniform vec2 sprite_origin = vec2(0.0);
uniform bool iris_present = true;
uniform vec2 rigid_gaze = vec2(0.0);
uniform float closure : hint_range(0.0,1.0) = 0.0;
uniform int role = 0; // 0 interior,1 rigid upper,2 static lower,3 disabled,4 closed lash,5 static surround
// Spatial ownership boundary, in stationary eye pixels. The reveal envelope
// keeps the closed contour's higher tips hidden until its center can join it.
// Both lash owners use this same boundary; there is no image crossfade.
float lash_handoff_seam(vec4 profile, float c) {
 float moving_top=profile.b-3.0+(profile.r-profile.b+5.0)*clamp((c-0.65)/0.2,0.0,1.0)+36.0*c;
 float closed_reveal=mix(profile.a-2.0,profile.g+2.0,clamp((c-0.70)/0.15,0.0,1.0));
 // A four-pixel terminal guard covers the measured bilinear footprint of
 // adjacent profile columns without a special-case endpoint or texture swap.
 return min(moving_top,closed_reveal)+4.0*smoothstep(0.85,1.0,c);
}
void fragment() {
 vec4 source=texture(TEXTURE,UV);
 vec4 p=texture(profile_texture,UV)*255.0;
 float y=UV.y/TEXTURE_PIXEL_SIZE.y-0.5;
 float lower=texture(lower_profile_texture,UV).r*255.0;
 float c=clamp(closure,0.0,1.0);
 float coverage=1.0;
 if(role==0) {coverage=smoothstep(-0.5,0.5,y-(p.r+36.0*c));}
 else if(role==1) {
  float threshold=lash_handoff_seam(p,c)-36.0*c;
  coverage=smoothstep(-0.5,0.5,y-threshold)*(1.0-smoothstep(-0.5,0.5,y+36.0*c-(lower+1.0)));
 }
 else if(role==2) {
  coverage=(1.0-smoothstep(0.0,1.0,y-(lower+7.0-max(0.0,(c-0.65)/0.35)*24.0)))*smoothstep(-0.5,0.5,y-(p.r+36.0*c-1.5));
 }
 else if(role==3) {coverage=0.0;}
 else if(role==4) {
  // Complement the moving upper lash's top clip in fixed eye coordinates.
  // Both owners meet at one seam instead of revealing two separated bands.
  float threshold=lash_handoff_seam(p,c);
  float handoff=(1.0-smoothstep(-0.5,0.5,y-threshold))*smoothstep(-0.5,0.5,y-(p.a-2.0));
  // Keep the original fixed boundary's filtered fringe in every pose.
  // It is a spatial ownership mask, not an endpoint branch or opacity blend.
  float original_boundary=smoothstep(-0.5,0.5,y-(p.g+2.0));
  coverage=max(handoff,original_boundary);
 }
 else if(role==5) {
  float threshold=p.b-3.0+(p.r-p.b+4.0)*min(c/0.15,1.0);
  coverage=smoothstep(-0.5,0.5,y-threshold);
 }
 if(role==6 || role==7) {
  vec2 eye_px=UV/TEXTURE_PIXEL_SIZE-vec2(0.5)+sprite_origin;
  if(role==7) {eye_px+=rigid_gaze;}
  vec2 fixed_uv=(eye_px+vec2(0.5))/eye_size;
  float upper=texture(profile_texture,fixed_uv).r*255.0;
  float bottom=texture(lower_profile_texture,fixed_uv).r*255.0;
  float aperture=texture(aperture_texture,fixed_uv).r;
  float inside=step(0.0,eye_px.x+0.5)*step(eye_px.x+0.5,eye_size.x)*step(0.0,eye_px.y+0.5)*step(eye_px.y+0.5,eye_size.y);
  float q=aperture*inside*smoothstep(-0.5,0.5,eye_px.y-(upper+36.0*c))*(1.0-smoothstep(-0.5,0.5,eye_px.y-(bottom+1.0)));
  if(role==7) {COLOR=vec4(source.rgb,source.a*q);}
  else {
   vec2 iris_uv=(eye_px-rigid_gaze+iris_padding+vec2(0.5))/iris_size;
   float a=texture(iris_texture,iris_uv).a*(iris_present ? 1.0 : 0.0);
   // Factor a single aperture's source-over opacity across two independent
   // objects. This prevents doubled coverage/fringes during partial blinking.
   float backing_alpha=q*(1.0-a)/max(1.0-q*a,0.000001);
   COLOR=vec4(source.rgb,backing_alpha);
  }
 } else {COLOR=vec4(source.rgb,source.a*coverage);}
}
