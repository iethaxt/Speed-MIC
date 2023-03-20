from ursina import *
from ground import *
from loader import *
import tkinter.filedialog

class Player(Entity):
    def __init__(self):
        super().__init__(
            model="cube"
        )
        camera.parent = self
        camera.rotation_x = 20
        camera.y = 8

        self.buildzone = Entity(model="cube", scale=1.2, collider="box")
        self.buildzone.collider = BoxCollider(self.buildzone, size=Vec3(.8,.8,.8))   
        self.buildColors = {False : color.rgba(0, 255, 0, 64), True : color.rgba(255, 0, 0, 64)}
        self.selected = False

        self.propertyHoverTime = 0
        self.entityHoverTime = 0

        self.entities = []

        self.positionText = Text(text=f"position: {self.buildzone.x}, {self.buildzone.y}, {self.buildzone.z}", origin=window.top_left, position=window.top_left)
        self.ColorProperties = WindowPanel(
            title="Color Properties",
            enabled=False,
        content=(
            Space(),
            Slider(),
            Slider(),
            Slider()
            ))
        
        self.GroundProperties = WindowPanel(
            title="Ground Properties",
            enabled=False,
        content=(
            Space(),
            Button(text="Ground"),
            Button(text="Grass"),
            Button(text="Water")
            ))
        
        self.saveButton = Button(text="Save", scale=Vec2(.2, .1), origin=window.bottom_left, position=window.bottom_left)
        self.saveButton.on_click = lambda : self.save()
        
        self.initialPos = Vec3(0,0,0)
        self.finalPos = Vec3(0,0,0)
        self.buildscale = Vec3(0,0,0)
    
    def movement(self):
        self.movement_input = (((self.left * held_keys["a"]) + (self.right * held_keys["d"])) + 
                               ((self.forward * held_keys["w"]) + (self.back * held_keys["s"])) +
                               ((self.up * held_keys["q"]) + (self.down * held_keys["e"]))).normalized()
        self.position += self.movement_input * time.dt * 6

    def buildCheck(self):
        self.buildzone.position = Vec3(self.X, self.Y, self.Z)

        if self.buildzone.intersects(ignore=[self.buildzone]):
            self.selected = True
        else:
            self.selected = False
        
        self.buildzone.color = self.buildColors[self.selected]
    
    def properties(self):
        if self.selected:
            self.propertyHoverTime += time.dt
            if held_keys["z"] and self.propertyHoverTime > .2:
                if self.ColorProperties.enabled:
                    self.ColorProperties.enabled = False
                else:
                    self.ColorProperties.enabled = True
                    self.ColorProperties.content[1].value = self.buildzone.intersects(ignore=[self.buildzone]).entities[0].color.r
                    self.ColorProperties.content[2].value = self.buildzone.intersects(ignore=[self.buildzone]).entities[0].color.g
                    self.ColorProperties.content[3].value = self.buildzone.intersects(ignore=[self.buildzone]).entities[0].color.b
                self.propertyHoverTime = 0
            
            if held_keys["x"] and self.propertyHoverTime > .2:
                if self.GroundProperties.enabled:
                    self.GroundProperties.enabled = False
                else:
                    def typeSwitch(type):
                            entity = self.buildzone.intersects(ignore=[self.buildzone]).entities[0]
                            newEntity = type(position=entity.position, scale=entity.scale, color=entity.color)
                            self.entities.remove(entity)
                            self.entities.append(newEntity)
                            if isinstance(newEntity, Collectable):
                                newEntity.visual.position = Vec3(0,0,0)
                            destroy(entity)
                    
                    if (isinstance(self.buildzone.intersects(ignore=[self]).entities[0], Ground) or
                        isinstance(self.buildzone.intersects(ignore=[self]).entities[0], Grass) or
                        isinstance(self.buildzone.intersects(ignore=[self]).entities[0], Water)):
                        self.GroundProperties.title = "Ground Properties"
                        self.GroundProperties.content[1].text = "Ground"
                        self.GroundProperties.content[2].text = "Grass"
                        self.GroundProperties.content[3].text = "Water"

                        self.GroundProperties.content[1].on_click = lambda:typeSwitch(Ground)
                        self.GroundProperties.content[2].on_click = lambda:typeSwitch(Grass)
                        self.GroundProperties.content[3].on_click = lambda:typeSwitch(Water)
                    
                        self.GroundProperties.enabled = True
                    else:
                        self.GroundProperties.title = "Collectable Properties"
                        self.GroundProperties.content[1].text = "Coin"
                        self.GroundProperties.content[2].text = "HealthPack"
                        self.GroundProperties.content[3].text = "Bomb"

                        self.GroundProperties.content[1].on_click = lambda:typeSwitch(Coin)
                        self.GroundProperties.content[2].on_click = lambda:typeSwitch(HealthPack)
                        self.GroundProperties.content[3].on_click = lambda:typeSwitch(Bomb)

                        self.GroundProperties.enabled = True
                self.propertyHoverTime = 0
        else:
            self.ColorProperties.enabled = False
            self.GroundProperties.enabled = False

        if self.ColorProperties.enabled:
            self.buildzone.intersects(ignore=[self.buildzone]).entities[0].color = color.rgba(self.ColorProperties.content[1].value * 255,
                                                                                              self.ColorProperties.content[2].value * 255,
                                                                                              self.ColorProperties.content[3].value * 255, 255)
        
    def build(self):
        if held_keys["1"]:
            self.buildzone.scale = self.finalPos - self.initialPos
            self.buildzone.scale = Vec3(abs(self.buildzone.scale_x), abs(self.buildzone.scale_y), abs(self.buildzone.scale_z))
            self.buildscale = self.buildzone.scale
            self.buildscale += Vec3(1, 1, 1)

            self.buildzone.scale += Vec3(1.2, 1.2, 1.2)
    
    def input(self, key):
        self.finalPos = self.buildzone.position
        if key == "1":
            self.initialPos = self.buildzone.position
        elif key == "1 up":
            if self.selected:
                for entity in self.buildzone.intersects(ignore=[self]).entities:
                    self.entities.remove(entity)
                    destroy(entity)
            else:
                entity = Ground(position=self.buildzone.position, scale=self.buildscale)
                self.entities.append(entity)
            self.buildzone.scale = 1.2
        if key == "2 up":
            if self.selected:
                self.entities.remove(self.buildzone.intersects(ignore=[self]).entities[0])
                destroy(self.buildzone.intersects(ignore=[self]).entities[0])
            else:
                entity = Coin(position=self.buildzone.position)
                self.entities.append(entity)
        if key == "3 up":
            if self.selected:
                self.entities.remove(self.buildzone.intersects(ignore=[self]).entities[0])
                destroy(self.buildzone.intersects(ignore=[self]).entities[0])
            else:
                entity = Entity(model="sphere", color=color.rgba(255, 0, 255, 64), position=self.buildzone.position, collider="box")
                self.entities.append(entity)
    
    def save(self):
        file = tkinter.filedialog.asksaveasfilename()
        if file != "":
            file = open(file, "w")
            for item in self.entities:
                if type(item).__name__ == "Entity":
                        file.write(
                            f"Player;{item.x},{item.y},{item.z}\n"
                        )
                else:
                    file.write(
                        f"{type(item).__name__};{item.x},{item.y},{item.z};{item.scale_x},{item.scale_y},{item.scale_z};{item.color.r * 255}, {item.color.g * 255}, {item.color.b * 255}\n"
                    )
            file.write("N/A")
            file.close()

    def update(self):
        self.movement()
        self.buildCheck()
        self.properties()
        self.build()

        self.positionText.text = f"position: {self.buildzone.x}, {self.buildzone.y}, {self.buildzone.z}"
        
        
if __name__ == "__main__":
    app = Ursina()

    Player()

    app.run()