shader_type canvas_item;
// SubViewport stores transparent layers premultiplied; preserve their edges.
render_mode blend_premul_alpha;
#include "res://motion_vertex.gdshaderinc"
// No gaze/brow/earring fragment replacement and no added shader samplers.
void fragment() {
    COLOR = texture(TEXTURE, UV);
}
