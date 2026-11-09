shader_type canvas_item;
render_mode unshaded;
// Two independently rigged pigment families meet at one CLOSED contour.
// No UV displacement or emotion opacity crossfade. Handover is spatial.
uniform float left_edge=0.0;
uniform float right_edge=123.0;
uniform bool outgoing=true;
uniform float source_center=40.0;
uniform float shape=0.0;
void fragment(){
 vec4 pixel=texture(TEXTURE,UV);
 float sx=UV.x/TEXTURE_PIXEL_SIZE.x;
 float y=UV.y/TEXTURE_PIXEL_SIZE.y-.5;
 float radius=mix(-1.0,32.0,shape);
 float incoming=1.0-smoothstep(radius-.75,radius+.75,abs(y-source_center));
 float old_radius=mix(32.0,-1.0,smoothstep(.35,.85,shape));
 float old_cover=1.0-smoothstep(old_radius-.75,old_radius+.75,abs(y-source_center));
 float coverage=outgoing ? old_cover : incoming;
 pixel.a*=coverage;
 float wl=smoothstep(left_edge-2.5,left_edge+2.5,sx);
 float wr=1.0-smoothstep(right_edge-2.5,right_edge+2.5,sx);
 pixel.a=pixel.a*wl*wr/max(1.0-pixel.a*(1.0-wr),.000001);
 COLOR=pixel;
}
