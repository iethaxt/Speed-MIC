from ursina import *
import numpy as np

fur_shader = Shader(name='fur_shader', language=Shader.GLSL,
fragment='''
#version 140
uniform sampler2D p3d_Texture0;
uniform sampler2D mask_texture;
uniform vec4 p3d_ColorScale;
uniform vec2 texture_scale;
uniform float noise_scale;
in vec2 uv;
out vec4 fragColor;
void main() {
    vec4 mask = texture(mask_texture, uv*noise_scale);
    if (mask.r < 1.){
        mask.a = 0;
    }
    vec4 texture = texture(p3d_Texture0, uv * texture_scale);
    texture.a -= mask.r;
    fragColor = texture * p3d_ColorScale;
}
''',
default_input={
    'noise_scale' : 16
}
)

class Fur():
    def __init__(self, entity, layers=3, layerSize=0.003, shadow=10, scale=10):
        fade = 1

        for layer in np.arange(0, layerSize*layers, layerSize):
            fade += 1
            furLayer = duplicate(entity)
            furLayer.shader = fur_shader
            furLayer.set_shader_input("noise_scale", scale)
            furLayer.set_shader_input("mask_texture", load_texture("noise"))
            
            furLayer.parent = entity
            furLayer.scale = 1 + layer
            furLayer.position = Vec3(0, 0, 0)
            furLayer.collider =  None
            furLayer.color -= color.rgba(shadow / fade, shadow / fade, shadow / fade, 0)
        entity.color -= color.rgba(shadow, shadow, shadow, 0)
    
    

if __name__ == "__main__":
    app = Ursina()

    EditorCamera()

    cube = Entity(model="cube", color=color.white, texture="grass")
    furCube = Fur(entity=cube, scale=2, layers=4, layerSize=0.005, shadow=10)

    def update():
        cube.rotation_y += 10 * time.dt

    app.run()