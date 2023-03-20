from ursina import *

camera_distort_shader = Shader(
fragment='''
#version 430
uniform sampler2D tex;
uniform float osg_FrameTime;
uniform float speed;
uniform float size;
uniform float intensity;
uniform float level;
uniform sampler2D noise;
in vec2 uv;
out vec4 color;
void main() {
    vec4 noise = texture(noise, (uv*size)+(osg_FrameTime*speed));

    vec2 textureUV = uv;
    textureUV -= vec2(noise.r / intensity) * level;
    
    vec3 rgb = texture(tex, textureUV).rgb;
    color = vec4(rgb, 1.0);
}
''',
default_input={
    "size" : 4,
    "speed" : 1,
    "intensity" : 100,
    "level" : 0
}
)

if __name__ == "__main__":
    app = Ursina()
    EditorCamera()


    camera.shader = camera_distort_shader
    camera.set_shader_input("noise", load_texture("camera_distortion"))

    Entity(model="cube", texture="grass")

    app.run()