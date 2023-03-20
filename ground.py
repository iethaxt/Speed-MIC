from ursina import *
from game_shaders.camera_distort_shader import camera_distort_shader
from game_shaders.fur_shader import Fur
from game_shaders.water_shader import water_shader

class Ground(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, model="cube", collider="box")
        self.friction = .02

class Grass(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, collider="box")
        scale = (self.scale.x + self.scale.y) / 2.5
        self.friction = .1

        self.visual = Entity(model="cube", position=self.position, scale=self.scale, color=self.color, texture="textures/tile.png")
        self.visual.texture_scale = self.scale.xz / 2
        self.visual.scale -= 4 * 0.005
        self.fur = Fur(entity=self.visual, scale=scale, layers=4, layerSize=0.005, shadow=10)
        self.on_destroy = lambda:self.onDestroy()
    def onDestroy(self):
        destroy(self.visual)

class Water(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, model="cube", collider="box")
        self.friction = 0

        self.shader = water_shader
        self.set_shader_input("noise1", load_texture("textures/Perlin1"))
        self.set_shader_input("noise2", load_texture("textures/Perlin2"))

if __name__ == "__main__":
    app = Ursina()
    EditorCamera()

    Ground(x=-1)
    Water(x=0)
    Grass(x=1)

    app.run()