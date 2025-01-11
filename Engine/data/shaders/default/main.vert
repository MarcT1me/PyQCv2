#version 430

// global input data (shader initialization)
layout (location = 0) in vec3 in_position;

// other uniform variables and functions


void main() {
    // the main function of the shader
    gl_Position = vec4(in_position, 1.0);
}
