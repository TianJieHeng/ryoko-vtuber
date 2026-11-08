shader_type canvas_item;
// Alpha-only aperture. Original UV is never displaced or rescaled.
uniform vec2 origin = vec2(0.0);
uniform vec2 rigid_offset = vec2(0.0);
uniform vec2 eye_center = vec2(475.0,500.0);
uniform float closure = 0.0;
varying vec2 source_pixel;
void vertex() { source_pixel = VERTEX + origin + rigid_offset; }
void fragment() {
    vec4 c = texture(TEXTURE, UV);
    float u = clamp((source_pixel.x-eye_center.x)/58.0,-1.0,1.0);
    float edge = u*u;
    float top = mix(480.0+13.0*edge,502.0+2.0*edge,closure);
    float bottom = mix(520.0-14.0*edge,502.0+2.0*edge,closure);
    float aperture = smoothstep(top-0.65,top+0.65,source_pixel.y) * (1.0-smoothstep(bottom-0.65,bottom+0.65,source_pixel.y));
    c.a *= aperture * (1.0-smoothstep(0.965,1.0,closure));
    COLOR = c;
}
