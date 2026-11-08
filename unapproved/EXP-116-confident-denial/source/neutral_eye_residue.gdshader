shader_type canvas_item;
render_mode unshaded;
uniform sampler2D skin_texture : filter_linear, repeat_disable;
uniform sampler2D owner_texture : filter_linear, repeat_disable;
uniform float smile=0.0;
void fragment(){
 vec4 original=texture(TEXTURE,UV);
 vec3 skin=texture(skin_texture,UV).rgb;
 float owner=texture(owner_texture,UV).r;
 // Static filtered source-over factorization. RGB is NOT emotion-modulated.
 vec3 pigment=(original.rgb-skin*(1.0-owner))/max(owner,.000001);
 float threshold=mix(-2.0,2.0,smoothstep(.45,.95,smile));
 float spatial=smoothstep(threshold-.04,threshold+.04,UV.y);
 COLOR=vec4(pigment,owner*spatial);
}
