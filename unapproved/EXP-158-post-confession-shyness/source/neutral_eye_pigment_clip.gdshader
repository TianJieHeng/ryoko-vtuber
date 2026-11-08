shader_type canvas_item;
render_mode unshaded;
uniform float smile=0.0;
uniform bool continuation=false;
uniform sampler2D original_texture : filter_linear, repeat_disable;
uniform sampler2D hair_texture : filter_linear, repeat_disable;
void fragment(){
 vec4 p=texture(TEXTURE,UV);
 float original_alpha=texture(original_texture,UV).a;
 float hair_alpha=texture(hair_texture,UV).a;
 // Exact filtered alpha deficit beneath the retained foreground. Neutral
 // pigment RGB equals original RGB, so the full moving neutral composite is
 // restored, not merely source-pixel-center samples.
 float residual=clamp((original_alpha-hair_alpha)/max(1.0-hair_alpha,.000001),0.0,1.0);
 float threshold=mix(-2.0,2.0,smoothstep(.45,.95,smile));
 float outgoing=smoothstep(threshold-.04,threshold+.04,UV.y);
 float a=residual*outgoing;
 if(continuation){a=residual*(1.0-outgoing)/max(1.0-residual*outgoing,.000001);}
 COLOR=vec4(p.rgb,a);
}
