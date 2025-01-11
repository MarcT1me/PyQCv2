#version 330 core

in vec2 uvs;
out vec4 f_color;

uniform sampler2D interfaceTexture;
uniform float alpha = 1.0;

void main() {
    vec4 tex = texture(interfaceTexture, uvs);
    f_color = tex * alpha;
}
