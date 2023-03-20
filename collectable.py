from ursina import *

class Collectable(Entity):
    def __init__(self,visual=Entity(scale=0.5), **kwargs):
        super().__init__(**kwargs)
        from player import Player
        self.player = Player
        self.collider = BoxCollider(self, center=Vec3(0,0,0), size=Vec3(.5,.9,.5))

        visual.parent = self
        self.visual = visual
        self.time = 0
    
    def update(self):
        self.visual.rotation_y += time.dt * 100
        self.visual.y += sin(self.time * 3) / 3 * time.dt
        self.time += time.dt
        
    def collected(self):
        self.enabled = False

class Coin(Collectable):
    def __init__(self, **kwargs):
        super().__init__(visual=Entity(model="models/Coin.dae", scale=0.5, color=color.hex("#ffcd42")), **kwargs)
    
    def collected(self):
        for entity in self.intersects().entities:
            if isinstance(entity, self.player):
                player = self.intersects().entities[self.intersects().entities.index(entity)]
        
        player.coins += 1
        player.coinSound.pitch = player.coinPitch
        player.coinSound.play()

        self.enabled = False

class HealthPack(Collectable):
    def __init__(self, **kwargs):
        super().__init__(visual=Entity(model="models/HealthPack.dae", scale=.35, color=color.green), **kwargs)
    
    def collected(self):
        for entity in self.intersects().entities:
            if isinstance(entity, self.player):
                player = self.intersects().entities[self.intersects().entities.index(entity)]

        player.y += 1 - player.health
        player.health = 1
        player.upgradeSound.play()

        self.enabled = False

class Bomb(Collectable):
    def __init__(self, **kwargs):
        super().__init__(visual=Entity(model="models/bomb.dae", scale=0.5, color=color.gray), **kwargs)
    
    def collected(self):
        for entity in self.intersects().entities:
            if isinstance(entity, self.player):
                player = self.intersects().entities[self.intersects().entities.index(entity)]
        
        player.health *= .5
        player.bombSound.play()

        self.enabled = False