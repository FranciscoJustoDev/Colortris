import pygame as pg
import random as rdm
import sys
from os import path

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
        # init all variables and level setup
        self.all_sprites = pg.sprite.Group()
        self.monster_sprites = pg.sprite.Group()
        self.spawn_column = GRID_WIDTH / 2 + (GRID_ORIGIN[0] - GRID_ORIGIN[0] / 2)
        self.no_monsters = True
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
        self.spawn_monster()
        self.dwn_mov()
        self.update_grid_map()
        self.monster_logic()

    def draw_grid(self):
        # Visual aid for development
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
                    for monster in self.monster_sprites:
                        if monster.active:
                            for e in self.grid_data:
                                if e[0] == monster.sector:
                                    if monster.rect.x > GRID_ORIGIN[0]:
                                        if self.grid_map[monster.sector[1]][monster.sector[0] - 1] == 0:
                                            monster.rect.x -= CELL_SIZE
                                            self.spawn_column -= CELL_SIZE
                if event.key == pg.K_RIGHT:
                    for monster in self.monster_sprites:
                        if monster.active:
                            for e in self.grid_data:
                                if e[0] == monster.sector:
                                    if monster.rect.x < GRID_WIDTH - CELL_SIZE:
                                        if self.grid_map[monster.sector[1]][monster.sector[0] + 1] == 0:
                                            monster.rect.x += CELL_SIZE
                                            self.spawn_column += CELL_SIZE
                if event.key == pg.K_DOWN:
                    for monster in self.monster_sprites:
                        if monster.active:
                            self.speed = 2

            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN:
                    for monster in self.monster_sprites:
                        if monster.active:
                            self.speed = 1
    
    def spawn_monster(self):
        monster_type = rdm.randint(1, 4)
        if self.no_monsters:
            self.no_monsters = False
            self.monster = Monster(self.grid_data, self.spawn_column, monster_type)
            self.monster_sprites.add(self.monster)
            self.all_sprites.add(self.monster)

        for monster in self.monster_sprites:
            if not(monster.active) and not(monster.locked) and not(monster.tracked):
                monster.locked = True
                self.monster = Monster(self.grid_data, self.spawn_column, monster_type)
                self.monster_sprites.add(self.monster)
                self.all_sprites.add(self.monster)
    
    def dwn_mov(self):
        for monster in self.monster_sprites:
            if monster.active and not(monster.locked) and not(monster.tracked):
                if monster.sector[1] < N_ROWS - 1:
                    if self.grid_map[monster.sector[1] + 1][monster.sector[0]] != 0:
                        for e in self.grid_data:
                            if e[0] == monster.sector:
                                monster.rect.centery = e[4]
                                monster.active = False
                if monster.active:
                    if monster.sector[1] < N_ROWS - 1:
                        monster.rect.y += SPEED * self.speed
                    else:
                        for e in self.grid_data:
                            if monster.sector == e[0]:
                                monster.rect.centery = e[4]
                                monster.active = False

    def update_grid_map(self):
        for monster in self.monster_sprites:
            if not(monster.active) and monster.locked and not(monster.tracked):
                x = monster.sector[0]
                y = monster.sector[1]
                self.grid_map[y][x] = monster.type
                monster.tracked = True
    
    def monster_logic(self):
        hor = False
        ver = False
        hor_kill_queue = []
        ver_kill_queue = []
        # Check for basic match!!
        for monster in self.monster_sprites:
            if not(monster.active) and monster.locked and monster.tracked:
                if monster.sector[0] > 0 and monster.sector[0] < N_COLS - 1:
                    if self.grid_map[monster.sector[1]][monster.sector[0] + 1] == monster.type:
                        if self.grid_map[monster.sector[1]][monster.sector[0] - 1] == monster.type:
                            hor = True
                            hor_kill_queue = [(monster.sector[0] - 1, monster.sector[1]), (monster.sector[0], monster.sector[1]), (monster.sector[0] + 1, monster.sector[1])]
                if monster.sector[1] < N_ROWS - 1 and monster.sector[1] > 0:
                    if self.grid_map[monster.sector[1] + 1][monster.sector[0]] == monster.type:
                        if self.grid_map[monster.sector[1] - 1][monster.sector[0]] == monster.type:
                            ver = True
                            ver_kill_queue = [(monster.sector[0], monster.sector[1] - 1), (monster.sector[0], monster.sector[1]), (monster.sector[0], monster.sector[1] + 1)]
        
        # Check for additional matches!!
        if hor:
            for monster in self.monster_sprites:
                if monster.sector == hor_kill_queue[0]:
                    if monster.sector[0] > 0:
                        if self.grid_map[monster.sector[1]][monster.sector[0] - 1] == monster.type:
                            hor_kill_queue.append((monster.sector[0] - 1, monster.sector[1]))
                elif monster.sector == hor_kill_queue[2]:
                    if monster.sector[0] < N_COLS - 1:
                        if self.grid_map[monster.sector[1]][monster.sector[0] + 1] == monster.type:
                            hor_kill_queue.append((monster.sector[0] + 1, monster.sector[1]))
        if ver:
            for monster in self.monster_sprites:
                if monster.sector == ver_kill_queue[0]:
                    if monster.sector[1] > 0:
                        if self.grid_map[monster.sector[1] - 1][monster.sector[0]] == monster.type:
                            ver_kill_queue.append((monster.sector[0], monster.sector[1] - 1))
                elif monster.sector == ver_kill_queue[2]:
                    if monster.sector[1] < N_ROWS - 1:
                        if self.grid_map[monster.sector[1] + 1][monster.sector[0]] == monster.type:
                            ver_kill_queue.append((monster.sector[0], monster.sector[1] + 1))
        
        # Execute order 66... >:3
        for monster in self.monster_sprites:
                for k in hor_kill_queue:
                    if monster.sector == k:
                        monster.kill()
                        self.grid_map[monster.sector[1]][monster.sector[0]] = 0

        for monster in self.monster_sprites:
                for k in ver_kill_queue:
                    if monster.sector == k:
                        monster.kill()
                        self.grid_map[monster.sector[1]][monster.sector[0]] = 0

        # update floating sprites
        for monster in self.monster_sprites:
            if not(monster.active) and monster.locked and monster.tracked:
                if monster.sector[1] < N_ROWS - 1:
                    if self.grid_map[monster.sector[1] + 1][monster.sector[0]] == 0:
                        monster.tracked = False
                        monster.rect.y += CELL_SIZE
                        self.grid_map[monster.sector[1]][monster.sector[0]] = 0

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