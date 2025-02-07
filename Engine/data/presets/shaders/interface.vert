#version 330 core

in vec2 vertices;
in vec2 texCoord;
out vec2 uvs;

void main() {
    uvs = texCoord;
    gl_Position = vec4(vertices, 0.0, 1.0);
}
