shader_type canvas_item;
render_mode unshaded;
uniform vec2 clip_center = vec2(0.5);
uniform vec2 clip_radius = vec2(0.24, 0.32);
uniform vec2 gaze_uv = vec2(0.0);
void fragment() {
    vec2 q = (UV - clip_center) / clip_radius;
    if (dot(q, q) > 1.0) discard;
    vec2 sample_uv = UV - gaze_uv;
    if (sample_uv.x < 0.0 || sample_uv.x > 1.0 || sample_uv.y < 0.0 || sample_uv.y > 1.0) discard;
    COLOR = texture(TEXTURE, sample_uv);
}
