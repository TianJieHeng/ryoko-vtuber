shader_type canvas_item;
render_mode unshaded;
// Fixed UV, RGB and scale. Upper lashes alone are translated by the node controller.
uniform sampler2D profile_texture : filter_nearest, repeat_disable;
uniform sampler2D lower_profile_texture : filter_nearest, repeat_disable;
uniform float closure : hint_range(0.0,1.0) = 0.0;
uniform int role = 0; // 0 interior,1 rigid upper,2 static lower,3 disabled,4 closed lash,5 static surround
void fragment() {
 vec4 source=texture(TEXTURE,UV);
 vec4 p=texture(profile_texture,UV)*255.0;
 float y=UV.y/TEXTURE_PIXEL_SIZE.y-0.5;
 float lower=texture(lower_profile_texture,UV).r*255.0;
 float c=clamp(closure,0.0,1.0);
 float coverage=1.0;
 if(role==0) {coverage=smoothstep(-0.5,0.5,y-(p.r+36.0*c));}
 else if(role==1) {
  float threshold=p.b-3.0+(p.r-p.b+5.0)*clamp((c-0.65)/0.2,0.0,1.0);
  coverage=smoothstep(-0.5,0.5,y-threshold)*(1.0-smoothstep(-0.5,0.5,y+36.0*c-(lower+1.0)));
 }
 else if(role==2) {coverage=1.0-smoothstep(0.0,1.0,y-(lower+7.0-max(0.0,(c-0.65)/0.35)*24.0));}
 else if(role==3) {coverage=0.0;}
 else if(role==4) {
  float threshold=p.g+2.0-clamp((c-0.55)/0.3,0.0,1.0)*(p.g-p.a+4.0);
  coverage=smoothstep(-0.5,0.5,y-threshold);
 }
 else if(role==5) {
  float threshold=p.b-3.0+(p.r-p.b+4.0)*min(c/0.15,1.0);
  coverage=smoothstep(-0.5,0.5,y-threshold);
 }
 COLOR=vec4(source.rgb,source.a*coverage);
}
