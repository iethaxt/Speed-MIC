from ursina import *
from loader import *
import os
app = Ursina()

class GUI(Entity):
    def __init__(self):
        super().__init__()
        Text.default_resolution = 8000 * Text.size

        self.level_loader = LevelLoader()
        self.inGame = False

        self.level_index = 0
        self.levels = os.listdir("levels")
        self.level_loader.load_level(f"levels/{self.levels[self.level_index]}")

        self.timer = 0

        #Menu GUI
        self.next_button = Button(text="Next", position=window.bottom_right, origin=window.bottom_right, scale=Vec2(.25, .1), enabled=False)
        self.back_button = Button(text="Back", position=window.bottom_left, origin=window.bottom_left, scale=Vec2(.25, .1), enabled=False)

        self.title = Text(text=self.levels[self.level_index], position=window.bottom, origin=window.bottom, scale=4, color=color.black, enabled=False)
        
        f = open(f"levels/{self.levels[self.level_index]}", "r")
        f = f.read()
        f = f.split("\n")
        self.score = f[len(f) - 1]
        
        self.score_text = Text(text=self.score, position=window.bottom, origin=window.bottom, scale=4, color=color.black, enabled=False)
        self.score_text.y += .1
        
        self.next_button.on_click = lambda : self.switch_level("next")
        self.back_button.on_click = lambda : self.switch_level("back")

        #Game GUI
        self.timer_text = Text(text="0", position=window.bottom, origin=window.bottom, scale=3, color=color.black, enabled=False)
        self.coins = Text(text="Coins: 0/0", position=window.top, origin=window.top, scale=3, color=color.black, enabled=False)

    def switch_level(self, direction):
        self.level_loader.unload_level()

        if direction == "next":
            self.level_index += 1
        else:
            self.level_index -= 1
        
        if self.level_index > (len(self.levels) - 1):
            self.level_index = 0
        elif self.level_index < 0:
            self.level_index = len(self.levels) - 1

        self.level_loader.load_level(f"levels/{self.levels[self.level_index]}")
        self.title.text = self.levels[self.level_index]

        f = open(f"levels/{self.levels[self.level_index]}", "r")
        f = f.read()
        f = f.split("\n")
        
        self.score = f[len(f) - 1]
        

    def menu(self):
        self.title.enabled = True
        self.next_button.enabled = True
        self.back_button.enabled = True
        self.score_text.enabled = True

        self.timer_text.enabled = False
        self.coins.enabled = False

        self.score_text.text = self.score

    def game(self):
        self.title.enabled = False
        self.next_button.enabled = False
        self.back_button.enabled = False
        self.score_text.enabled = False

        self.timer_text.enabled = True
        self.coins.enabled = True

        self.timer_text.text = "{:.2f}".format(self.level_loader.timer)

        self.coins.text = f"Coins: {self.level_loader.player.coins}/{self.level_loader.coins}"

        
    def update(self):
        if not self.level_loader.inGame:
            self.menu()
        else:
            self.game()

        file = open(f"levels/{self.levels[self.level_index]}", "r")
        f = file.read()
        f = f.split("\n")
        
        self.score = f[len(f) - 1]
        file.close()


GUI()

app.run()