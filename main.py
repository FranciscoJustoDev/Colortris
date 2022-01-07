import pygame as pg
import random as rdm
import sys
from settings import *
from sprites import *
from computations import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        self.sector_data = sector_load()

    def new(self):
        # init all variables and setup
        self.all_sprites = pg.sprite.Group()
        self.chip_sprites = pg.sprite.Group()
        self.spawn_points = sector_anchors()
        self.chip = Chip(self.sector_data, self.spawn_points)
        self.chip_sprites.add(self.chip)
        self.all_sprites.add(self.chip)

    def run(self):
        # Game loop
        self.game_running = True
        while self.game_running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()
    
    def update(self):
        self.all_sprites.update()
        self.spawn_chip()

    def draw_grid(self):
        for x in range(0, WIDTH, GRIDSTEP):
            pg.draw.line(self.screen, WHITE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRIDSTEP):
            pg.draw.line(self.screen, WHITE, (0, y), (WIDTH, y))
    
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
    
    def spawn_chip(self):
        for chip in self.chip_sprites:
            if self.chip.mov == True:
                pass
            else:
                self.chip = Chip(self.sector_data, self.spawn_points)
                self.chip_sprites.add(self.chip)
                self.all_sprites.add(self.chip)
    
    def show_start_screen(self):
        pass
    
    def show_go_screen(self):
        pass

g = Game()
while True:
    g.show_start_screen()
    g.new()
    g.run()
    g.show_go_screen()