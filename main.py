import pygame as pg
import random as rdm
import sys

from pygame import sprite
from pygame.constants import KEYDOWN
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
        self.grid_data = grid_data_load()
        self.grid_map = grid_map_pop()

    def new(self):
        # init all variables and setup
        self.all_sprites = pg.sprite.Group()
        self.chip_sprites = pg.sprite.Group()
        self.col_pos = GRID_WIDTH / 2 + (GRID_ORIGIN[0] - GRID_ORIGIN[0] / 2)
        self.no_chips = True
        self.speed = 1

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
        self.update_grid_map()
        self.chip_logic()

    def draw_grid(self):
        for x in range(GRID_ORIGIN[0], GRID_WIDTH, CELL_SIZE):
            pg.draw.line(self.screen, WHITE, (x, GRID_ORIGIN[1]), (x, GRID_HEIGHT))
        pg.draw.line(self.screen, WHITE, (GRID_ORIGIN[0], GRID_HEIGHT), (GRID_WIDTH, GRID_HEIGHT))

        for y in range(GRID_ORIGIN[1], GRID_HEIGHT, CELL_SIZE):
            pg.draw.line(self.screen, WHITE, (GRID_ORIGIN[0], y), (GRID_WIDTH, y))
        pg.draw.line(self.screen, WHITE, (GRID_WIDTH, GRID_ORIGIN[1]), (GRID_WIDTH, GRID_HEIGHT))
    
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
                            for e in self.grid_data:
                                if e[0] == chip.sector:
                                    if chip.rect.x > GRID_ORIGIN[0]:
                                        if self.grid_map[chip.sector[1]][chip.sector[0] - 1] == 0:
                                            chip.rect.x -= CELL_SIZE
                                            self.col_pos -= CELL_SIZE
                if event.key == pg.K_RIGHT:
                    for chip in self.chip_sprites:
                        if chip.active:
                            for e in self.grid_data:
                                if e[0] == chip.sector:
                                    if chip.rect.x < GRID_WIDTH - CELL_SIZE:
                                        if self.grid_map[chip.sector[1]][chip.sector[0] + 1] == 0:
                                            chip.rect.x += CELL_SIZE
                                            self.col_pos += CELL_SIZE
                if event.key == pg.K_DOWN:
                    for chip in self.chip_sprites:
                        if chip.active:
                            self.speed = 2

            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN:
                    for chip in self.chip_sprites:
                        if chip.active:
                            self.speed = 1
    
    def spawn_chip(self):
        if self.no_chips:
            self.no_chips = False
            self.chip = Chip(self.grid_data, self.col_pos)
            self.chip_sprites.add(self.chip)
            self.all_sprites.add(self.chip)

        for chip in self.chip_sprites:
            if not(chip.active) and not(chip.locked) and not(chip.tracked):
                chip.locked = True
                self.chip = Chip(self.grid_data, self.col_pos)
                self.chip_sprites.add(self.chip)
                self.all_sprites.add(self.chip)
    
    def dwn_mov(self):
        for chip in self.chip_sprites:
            if chip.active and not(chip.locked) and not(chip.tracked):
                if chip.sector[1] < N_ROWS - 1:
                    if self.grid_map[chip.sector[1] + 1][chip.sector[0]] != 0:
                        for e in self.grid_data:
                            if e[0] == chip.sector:
                                chip.rect.centery = e[4]
                                chip.active = False
                if chip.active:
                    if chip.sector[1] < N_ROWS - 1:
                        chip.rect.y += SPEED * self.speed
                    else:
                        for e in self.grid_data:
                            if chip.sector == e[0]:
                                chip.rect.centery = e[4]
                                chip.active = False

    def update_grid_map(self):
        for chip in self.chip_sprites:
            if not(chip.active) and chip.locked and not(chip.tracked):
                x = chip.sector[0]
                y = chip.sector[1]
                self.grid_map[y][x] = chip.type
                chip.tracked = True
    
    def chip_logic(self):
        hor = False
        ver = False
        hor_kill_queue = []
        ver_kill_queue = []
        # Check for basic match!!
        for chip in self.chip_sprites:
            if not(chip.active) and chip.locked and chip.tracked:
                if chip.sector[0] > 0 and chip.sector[0] < N_COLS - 1:
                    if self.grid_map[chip.sector[1]][chip.sector[0] + 1] == chip.type:
                        if self.grid_map[chip.sector[1]][chip.sector[0] - 1] == chip.type:
                            hor = True
                            hor_kill_queue = [(chip.sector[0] - 1, chip.sector[1]), (chip.sector[0], chip.sector[1]), (chip.sector[0] + 1, chip.sector[1])]
                if chip.sector[1] < N_ROWS - 1 and chip.sector[1] > 0:
                    if self.grid_map[chip.sector[1] + 1][chip.sector[0]] == chip.type:
                        if self.grid_map[chip.sector[1] - 1][chip.sector[0]] == chip.type:
                            ver = True
                            ver_kill_queue = [(chip.sector[0], chip.sector[1] - 1), (chip.sector[0], chip.sector[1]), (chip.sector[0], chip.sector[1] + 1)]
        
        # Check for additional matches!!
        if hor:
            for chip in self.chip_sprites:
                if chip.sector == hor_kill_queue[0]:
                    if chip.sector[0] > 0:
                        if self.grid_map[chip.sector[1]][chip.sector[0] - 1] == chip.type:
                            hor_kill_queue.append((chip.sector[0] - 1, chip.sector[1]))
                elif chip.sector == hor_kill_queue[2]:
                    if chip.sector[0] < N_COLS - 1:
                        if self.grid_map[chip.sector[1]][chip.sector[0] + 1] == chip.type:
                            hor_kill_queue.append((chip.sector[0] + 1, chip.sector[1]))
        if ver:
            if chip.sector == ver_kill_queue[0]:
                if chip.sector[1] > 0:
                    if self.grid_map[chip.sector[1] - 1][chip.sector[0]] == chip.type:
                        ver_kill_queue.append((chip.sector[0], chip.sector[1] - 1))
            elif chip.sector == ver_kill_queue[2]:
                if chip.sector[1] < N_ROWS - 1:
                    if self.grid_map[chip.sector[1] + 1][chip.sector[0]] == chip.type:
                        ver_kill_queue.append((chip.sector[0], chip.sector[1] + 1))
        
        # Execute order 66... >:3
        for chip in self.chip_sprites:
                for k in hor_kill_queue:
                    if chip.sector == k:
                        chip.kill()
                        self.grid_map[chip.sector[1]][chip.sector[0]] = 0

        for chip in self.chip_sprites:
                for k in ver_kill_queue:
                    if chip.sector == k:
                        chip.kill()
                        self.grid_map[chip.sector[1]][chip.sector[0]] = 0

        # update floating sprites
        for chip in self.chip_sprites:
            if not(chip.active) and chip.locked and chip.tracked:
                if chip.sector[1] < N_ROWS - 1:
                    if self.grid_map[chip.sector[1] + 1][chip.sector[0]] == 0:
                        chip.tracked = False
                        chip.rect.y += CELL_SIZE
                        self.grid_map[chip.sector[1]][chip.sector[0]] = 0

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