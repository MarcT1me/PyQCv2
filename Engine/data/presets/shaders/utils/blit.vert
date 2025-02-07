#version 330

in vec2 in_vert;
in vec2 in_text;
out vec2 v_text;
uniform vec2 pos = vec2(0);

void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
    v_text = in_text-pos;
}