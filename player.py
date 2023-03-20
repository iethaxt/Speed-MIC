from ursina import *
from ground import *
from collectable import *
from game_shaders.camera_distort_shader import *

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(collider="box", **kwargs)
        camera.rotation_x = 20
        camera.shader = camera_distort_shader
        camera.set_shader_input("noise", load_texture("textures/camera_distortion.png"))

        self.health = 1
        self.coins = 0
        self.spawn = self.position
        self.fallDeath = 0

        self.velocity = Vec3(0,0,0)
        self.moveable = True
        self.friction = 0.01

        self.groundCheck = Entity(parent=self, collider="box")
        self.groundCheck.scale *= Vec3(.8, 1.2, .8)
        self.visual = Entity(parent=self, model="cube")
        self.movementReferance = Entity()

        self.slide = Audio("audio/brown_noise.wav", loop=True, autoplay=False)
        self.fall = Audio("audio/white_noise.wav", loop=True, autoplay=True)
        self.bounceSound = Audio("audio/hit.wav", autoplay=False)
        self.upgradeSound = Audio("audio/upgrade.wav", autoplay=False)
        self.bombSound = Audio("audio/bomb.mp3", autoplay=False)
        self.coinSound = Audio("audio/coin.wav", autoplay=False)
        self.coinPitch = 0

    def isground(self, object):
        if (isinstance(object.intersects(ignore=[self, self.groundCheck]).entities[0], Ground)
            or isinstance(object.intersects(ignore=[self, self.groundCheck]).entities[0], Water)
            or isinstance(object.intersects(ignore=[self, self.groundCheck]).entities[0], Grass)):
            return True
        else:
            return False

    def movement(self):
        self.movement_input = (((self.movementReferance.left * held_keys["a"]) + (self.movementReferance.right * held_keys["d"])) + 
                               ((self.movementReferance.forward * held_keys["w"]) + (self.movementReferance.back * held_keys["s"]))).normalized() * self.moveable
        self.velocity += self.movement_input / (8 + (self.friction * 80))

        if self.groundCheck.intersects(ignore=[self, self.groundCheck]):
            if self.isground(self.groundCheck):
                self.velocity.y *= -.6
                self.fallDeath = 0

                self.friction = self.groundCheck.intersects(ignore=[self, self.groundCheck]).entities[0].friction
            
                #if no keys are pressed slowdown (while on ground)
                if self.movement_input.x == 0:
                    self.velocity.x -= self.velocity.x * self.friction
                if self.movement_input.z == 0:
                    self.velocity.z -= self.velocity.z * self.friction

                if not self.slide.playing:
                    self.slide.play()
        else:
            self.velocity.y -= .2
            if self.velocity.y < 0:
                self.fallDeath += time.dt
            if self.slide.playing and (self.fallDeath > 0.1):
                self.friction = 0
                self.slide.pause()
            
        self.bounce()
        self.position += self.velocity * time.dt

    def animation(self):
        self.visual.rotation_y += self.velocity.x

        camera.position = Vec3(self.x, self.y+8, self.z-20)
        camera.set_shader_input("level", self.fallDeath / 3)
    
    def bounce(self):
        def bounce():
            self.position -= self.velocity.normalized() / 50
            self.velocity.xz *= -.9
            self.velocity.y += (abs(self.velocity.x) + abs(self.velocity.z) / 4)
            self.velocity.y *= 1.02
            self.bounceSound.play()
            self.bounceSound.volume = (abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)) / 10
            self.bounceSound.pitch = (abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)) / 10
        
        if self.intersects(ignore=[self, self.groundCheck]):
            if self.isground(self):
                bounce()
            elif isinstance(self.intersects(ignore=[self, self.groundCheck]).entities[0], Collectable):
                self.intersects(ignore=[self, self.groundCheck]).entities[0].collected()

    def melt(self):
        if self.movement_input != Vec3(0,0,0):
            self.health -= .1 * time.dt

        self.scale = self.health

        
    def update(self):
        self.movement()
        self.animation()
        self.melt()

        self.slide.volume = (abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)) / 4
        self.slide.pitch = self.friction * 60
        self.fall.volume = self.fallDeath / 32

if __name__ == "__main__":
    app = Ursina()

    Player(y=2, x=-.5)

    Ground(scale=Vec3(8, 1, 3))

    app.run()