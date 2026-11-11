shader_type canvas_item;
render_mode unshaded;
// PRIVATE c=0, centered gaze only. Full APPROVED gaze derivative, including its
// documented inferred white backing. No source PNG or import setting changed.
// Explicit alias of the owner texture avoids passing Godot built-in TEXTURE as a function argument.
uniform sampler2D source_texture : filter_linear, repeat_disable;
uniform sampler2D profile_texture : filter_nearest, repeat_disable;
uniform sampler2D lower_profile_texture : filter_nearest, repeat_disable;
uniform sampler2D shape_upper : filter_linear, repeat_disable;
uniform sampler2D shape_lower : filter_linear, repeat_disable;
uniform sampler2D aperture_texture : filter_linear, repeat_disable;
uniform sampler2D iris_texture : filter_linear, repeat_disable;
uniform sampler2D sclera_texture : filter_linear, repeat_disable;
uniform vec2 eye_size;
uniform vec2 iris_size;
uniform vec2 iris_padding;
uniform vec2 bounds;
uniform float opening_px=0.0;
uniform int kind=0; // 0 sclera, 1 upper lash, 2 stationary iris
varying vec2 destination_px;
float amplitude(float x) {
 float u=clamp((x-bounds.x)/(bounds.y-bounds.x),0.0,1.0);
 return clamp(opening_px,0.0,4.0)*pow(sin(3.141592653589793*u),2.0);
}
vec2 anchors(float x) {
 vec2 uv=vec2((x+0.5)/eye_size.x,0.5);
 float t=texture(shape_upper,uv).r*255.0;
 float b=texture(shape_lower,uv).r*255.0-2.0;
 return vec2(t,max(t+1.0,b));
}
float source_y(vec2 p) {
 vec2 tb=anchors(p.x);float a=amplitude(p.x);
 if(p.y<=tb.x-a) {return p.y+a;}
 if(p.y>=tb.y) {return p.y;}
 return (p.y+a*tb.y/(tb.y-tb.x))/(1.0+a/(tb.y-tb.x));
}
// Alpha-weighted interpolation: alpha-zero RGB contributes exactly zero.
// The returned alpha remains the same bilinear coverage, not repainted art.
vec4 safe_sample(sampler2D tex,vec2 p,vec2 size) {
 vec2 cell=floor(p);vec2 f=fract(p);vec4 sum=vec4(0.0);
 for(int j=0;j<2;j++) {for(int i=0;i<2;i++) {
  vec2 v=vec2(float(i),float(j));vec2 xy=clamp(cell+v,vec2(0.0),size-vec2(1.0));
  vec4 c=texture(tex,(xy+vec2(0.5))/size);
  float w=(i==0 ? 1.0-f.x : f.x)*(j==0 ? 1.0-f.y : f.y);
  sum+=vec4(c.rgb*c.a,c.a)*w;
 }}
 return vec4(sum.a>0.0 ? sum.rgb/sum.a : vec3(0.0),sum.a);
}
float q_at(vec2 p) {
 vec2 uv=(p+vec2(0.5))/eye_size;
 float upper=texture(profile_texture,uv).r*255.0;
 float bottom=texture(lower_profile_texture,uv).r*255.0;
 float inside=step(0.0,p.x+0.5)*step(p.x+0.5,eye_size.x)*step(0.0,p.y+0.5)*step(p.y+0.5,eye_size.y);
 return texture(aperture_texture,uv).r*inside*smoothstep(-0.5,0.5,p.y-upper)*(1.0-smoothstep(-0.5,0.5,p.y-(bottom+1.0)));
}
void vertex() {destination_px=VERTEX-vec2(0.5);}
void fragment() {
 vec4 source=texture(TEXTURE,UV);
 if(kind==2) {
  vec2 p=UV*iris_size-vec2(0.5)-iris_padding;
  vec2 s=vec2(p.x,source_y(p));
  COLOR=vec4(source.rgb,source.a*q_at(s));
 } else {
  vec2 p=UV*eye_size-vec2(0.5);
  bool moving=amplitude(p.x)>0.000001 && p.y<anchors(p.x).y;
  if(moving) {source=safe_sample(source_texture,p,eye_size);}
  if(kind==1) {
   vec4 prof=texture(profile_texture,UV)*255.0;
   float lower=texture(lower_profile_texture,UV).r*255.0;
   float threshold=min(prof.b-3.0,prof.a-2.0);
   float coverage=smoothstep(-0.5,0.5,p.y-threshold)*(1.0-smoothstep(-0.5,0.5,p.y-(lower+1.0)));
   COLOR=vec4(source.rgb,source.a*coverage);
  } else {
   float q=q_at(p);
   // Source alpha equals the approved aperture alpha byte-for-byte. Thus q
   // carries the material alpha with the deformed surface, never exposes
   // transparent backing. Iris remains in destination coordinates.
   vec2 iris_uv=(destination_px+iris_padding+vec2(0.5))/iris_size;
   float a=texture(iris_texture,iris_uv).a;
   float backing_alpha=q*(1.0-a)/max(1.0-q*a,0.000001);
   COLOR=vec4(source.rgb,backing_alpha);
  }
 }
}
