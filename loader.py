from ursina import *
from ground import *
from collectable import *
from player import Player


class LevelLoader(Entity):
    def __init__(self):
        super().__init__()
        self.collectables = []
        self.ground = []
        self.level = None
        
        self.player = None
        self.player_spawn = Vec3(0,0,0)

        self.inGame = False
        self.coins = 0
        self.timer = 0

        self.inital = 0

    def load_level(self, level):
        self.level = level
        f = open(self.level, "r")
        f = f.read()
        f = f.split("\n")

        for entity in range(len(f)):
            if f[entity] == "N\A":
                break
            f[entity] = f[entity].split(";")
            for property in range(len(f[entity])):
                f[entity][property] = f[entity][property].split(",")

        string_to_entity = {
            "Ground" : Ground, "Water" : Water, "Grass" : Grass,
            "Coin" : Coin, "HealthPack" : HealthPack, "Bomb" : Bomb
        }

        for entity in range(len(f) - 1):
            if f[entity][0][0] == "Player":
                self.player_spawn = Vec3(float(f[entity][1][0]), float(f[entity][1][1]), float(f[entity][1][2]))
                self.player = Player(
                    position = self.player_spawn
                )
            else:
                e = string_to_entity[f[entity][0][0]](
                    position = Vec3(float(f[entity][1][0]), float(f[entity][1][1]), float(f[entity][1][2])),
                    scale = Vec3(float(f[entity][2][0]), float(f[entity][2][1]), float(f[entity][2][2])),
                    color = color.rgb(float(f[entity][3][0]), float(f[entity][3][1]), float(f[entity][3][2]))
                )

                if isinstance(e, Collectable):
                    self.collectables.append(e)
                    if isinstance(e, Coin):
                        self.coins += 1
                else:
                    self.ground.append(e)
        
    def unload_level(self):
        destroy(self.player)
        for ground in self.ground:
            destroy(ground)
        for collectable in self.collectables:
            destroy(collectable)
        self.coins = 0
            
    def update(self):
        def respawn():
            self.player.moveable = False
            self.player.velocity = Vec3(0,0,0)
            self.player.position = self.player_spawn
            self.player.y += .1
            self.player.health = 1
            self.player.visual.rotation_y = 0

            for collectable in self.collectables:
                collectable.enabled = True
                collectable.visual.y = 0
                collectable.time = 0
                collectable.visual.rotation_y = 0

            self.inGame = False
            self.inital = time.perf_counter()

            self.player.coins = 0
        
        if isinstance(self.player, Player):
            if (self.player.health < .1) or (self.player.fallDeath >= 4):
                respawn()
                self.timer = 0
            if self.player.coins == self.coins:
                respawn()

                f = open(self.level, "r")
                f = f.read()
                f = f.split("\n")

                if (f[len(f) - 1] == "N/A") or (float(f[len(f) - 1]) > self.timer):
                    f2 = open(self.level, "w")
                    for line in range(len(f) - 1):
                        f2.write(f"{f[line]}\n")
                    f2.write("{:.2f}".format(self.timer))
                    f2.close()
                
                self.timer = 0
            
            if self.player.velocity.xz != Vec2(0,0) or self.inGame:
                self.inGame = True
                self.timer += time.dt

            if (time.perf_counter() - self.inital) > .3:
                self.player.moveable = True

        self.player.coinPitch = 1 + (self.player.coins / self.coins)
    


if __name__ == "__main__":
    app = Ursina()
    levelLoader = LevelLoader()

    load = Button(text="load", origin=window.bottom_left, position=window.bottom_left, scale=.2)
    load.on_click = lambda : levelLoader.load_level("levels/test")

    unload = Button(text="unload", origin=window.bottom_right, position=window.bottom_right, scale=.2)
    unload.on_click = lambda : levelLoader.unload_level()

    app.run()