import pygame as pg
from computations import *
from settings import *
import random as rdm

class Text(pg.sprite.Sprite):
    def __init__(self, font, text, color, pos):
        pg.sprite.Sprite.__init__(self)
        self.font = font
        self.text = text
        self.color = color
        self.image = self.font.render(text, False, color)
        self.rect = self.image.get_rect()
        self.rect.center = pos

class Monster(pg.sprite.Sprite):
    def __init__(self, sector_data, spawn_col, monster_type, sprites):
        pg.sprite.Sprite.__init__(self)
        self.sprites = sprites
        self.image = self.sprites[0]
        self.type = monster_type
        self.sector = (-1, -1)
        self.rect = self.image.get_rect()
        # start in current column
        self.rect.center = (spawn_col, GRID_ORIGIN[1] + CELL_SIZE / 2)
        self.sector_data = sector_data
        # currently moving
        self.active = True
        # chip before currently active
        self.locked = False
        # acknowledge in the map
        self.tracked = False
        self.last_update = pg.time.get_ticks()
        self.anim_frame = 0
        self.init_frame = 0
        self.n_frames = 3
        self.love_sfx = True
        self.upset_sfx = True
    
    def get_sector(self, pos, sec_data):
        # checks if pos (centerxy) is in given range
        for e in sec_data:
            if pos[0] in range(e[1][0], e[1][1]) and pos[1] in range(e[2][0], e[2][1]):
                return e[0]

    def update(self):
        self.sector = self.get_sector((self.rect.centerx, self.rect.centery), self.sector_data)
        now = pg.time.get_ticks()
        if now - self.last_update > MONSTER_ANIM_FPS:
            self.last_update = now
            if self.n_frames > 2:
                self.n_frames = 0
                self.anim_frame = self.init_frame
            else:
                self.image = self.sprites[self.anim_frame]
                self.anim_frame += 1
                self.n_frames += 1
