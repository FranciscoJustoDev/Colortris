import pygame as pg
import random as rdm
import sys

from pygame import sprite
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
        self.sector_map = sector_map_pop()

    def new(self):
        # init all variables and setup
        self.all_sprites = pg.sprite.Group()
        self.chip_sprites = pg.sprite.Group()
        self.col_pos = WIDTH / 2
        self.no_chips = True

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
        self.dwn_mov()
        self.update_sector_map()
        self.chip_logic()

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
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    for chip in self.chip_sprites:
                        if chip.active:
                            for e in self.sector_data:
                                if e[0] == chip.sector:
                                    if chip.rect.x > 0:
                                        if self.sector_map[chip.sector[1]][chip.sector[0] - 1] == 0:
                                            chip.rect.x -= GRIDSTEP
                                            self.col_pos -= GRIDSTEP
                if event.key == pg.K_RIGHT:
                    for chip in self.chip_sprites:
                        if chip.active:
                            for e in self.sector_data:
                                if e[0] == chip.sector:
                                    if chip.rect.x < WIDTH - GRIDSTEP:
                                        if self.sector_map[chip.sector[1]][chip.sector[0] + 1] == 0:
                                            chip.rect.x += GRIDSTEP
                                            self.col_pos += GRIDSTEP
    
    def spawn_chip(self):
        if self.no_chips:
            self.no_chips = False
            self.chip = Chip(self.sector_data, self.col_pos)
            self.chip_sprites.add(self.chip)
            self.all_sprites.add(self.chip)

        for chip in self.chip_sprites:
            if not(chip.active) and not(chip.locked) and not(chip.tracked):
                chip.locked = True
                self.chip = Chip(self.sector_data, self.col_pos)
                self.chip_sprites.add(self.chip)
                self.all_sprites.add(self.chip)
    
    def dwn_mov(self):
        for chip in self.chip_sprites:
            if chip.active and not(chip.locked) and not(chip.tracked):
                if chip.active:
                    if chip.sector[1] < N_ROWS - 1:
                        if self.sector_map[chip.sector[1] + 1][chip.sector[0]] != 0:
                            for e in self.sector_data:
                                if e[0] == chip.sector:
                                    chip.rect.centery = e[4]
                                    chip.active = False
                    if chip.rect.bottom <= HEIGHT:
                            chip.rect.y += SPEED
                    else:
                        chip.rect.bottom = HEIGHT
                        chip.active = False

    def update_sector_map(self):
        for chip in self.chip_sprites:
            if not(chip.active) and chip.locked and not(chip.tracked):
                x = chip.sector[0]
                y = chip.sector[1]
                self.sector_map[y][x] = chip.type
                chip.tracked = True
    
    def chip_logic(self):
        hor = False
        ver = False
        to_kill = []
        for chip in self.chip_sprites:
            if not(chip.active) and chip.locked and chip.tracked:
                if chip.sector[0] > 0 and chip.sector[0] < N_COLS - 1:
                    if self.sector_map[chip.sector[1]][chip.sector[0] + 1] == chip.type:
                        if self.sector_map[chip.sector[1]][chip.sector[0] - 1] == chip.type:
                            hor = True
                            to_kill = (chip.sector[0], chip.sector[1]), (chip.sector[0] + 1, chip.sector[1]), (chip.sector[0] - 1, chip.sector[1])
                if chip.sector[1] < N_ROWS - 1:
                    if self.sector_map[chip.sector[1] + 1][chip.sector[0]] == chip.type:
                        if self.sector_map[chip.sector[1] - 1][chip.sector[0]] == chip.type:
                            ver = True
                            to_kill = (chip.sector[0], chip.sector[1]), (chip.sector[0], chip.sector[1] + 1), (chip.sector[0], chip.sector[1] - 1)
        if hor:
            for chip in self.chip_sprites:
                if chip.sector == to_kill[0] or chip.sector == to_kill[1] or chip.sector == to_kill[2]:
                    chip.kill()
                    self.sector_map[chip.sector[1]][chip.sector[0]] = 0
        if ver:
            for chip in self.chip_sprites:
                if chip.sector == to_kill[0] or chip.sector == to_kill[1] or chip.sector == to_kill[2]:
                    chip.kill()
                    self.sector_map[chip.sector[1]][chip.sector[0]] = 0
        
        for chip in self.chip_sprites:
            if not(chip.active) and chip.locked and chip.tracked:
                if chip.sector[1] < N_ROWS - 1:
                    if self.sector_map[chip.sector[1] + 1][chip.sector[0]] == 0:
                        chip.tracked = False
                        chip.rect.y += GRIDSTEP
                        self.sector_map[chip.sector[1]][chip.sector[0]] = 0

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