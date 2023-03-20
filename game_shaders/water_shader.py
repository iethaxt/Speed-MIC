from ursina import *

water_shader = Shader(
fragment='''
#version 430
uniform float osg_FrameTime;
uniform float intensity;
uniform float speed;
uniform sampler2D noise1;
uniform sampler2D noise2;
uniform vec4 p3d_ColorScale;
in vec2 uv;
out vec4 color;
void main() {
    float time = osg_FrameTime*speed;

    vec4 waterNoise1 = texture(noise1, uv-time);
    vec4 waterNoise2 = texture(noise2, uv + vec2(sin(time), cos(time)));

    vec4 water = waterNoise1 * waterNoise2;
    if (water.r < intensity){
        water.rgb = vec3(1.);
        water.a = .5;
    }
    else{
        water.rgb = vec3(1.);
        water.a = .8;
    }

    color = water * p3d_ColorScale;
}
''',
default_input={
    "speed" : .2,
    "intensity" : .52,
}
)

if __name__ == "__main__":
    app = Ursina()
    EditorCamera()

    e = Entity(model="sphere", scale=1, shader=water_shader)
    e.set_shader_input("noise1", load_texture("Perlin1"))
    e.set_shader_input("noise2", load_texture("Perlin2"))

    app.run()

    app.run()