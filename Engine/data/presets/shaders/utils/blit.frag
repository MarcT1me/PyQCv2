#version 330

in vec2 v_text;
out vec4 f_color;

uniform sampler2D u_texture_0;

void main() {
    f_color = texture(u_texture_0, v_text);
}