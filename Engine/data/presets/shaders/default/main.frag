#version 430

// the final value of the pixel color
out vec4 fragColor;

// global input data (shader initialization)
uniform vec2 resolution;
uniform vec3 bg_color = vec3(0.2, 0.4, 0.4);

// other uniform variables and functions


void main() {
    // the main function of the shader
    vec2 uv = gl_FragCoord.xy / resolution.xy;
    vec4 color = vec4(bg_color, 1.0);

    // data output
    fragColor = color;
}
