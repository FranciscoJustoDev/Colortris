import pygame as pg
from computations import *
from settings import *
import random as rdm

class Chip(pg.sprite.Sprite):
    def __init__(self, sector_data, current_column):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((CELL_SIZE, CELL_SIZE))
        self.type = rdm.randint(1, 4)
        self.sector = (-1, -1)
        self.color = CHIP_COLORS[self.type]
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        # start in current column
        self.rect.center = (current_column, GRID_ORIGIN[1] + CELL_SIZE / 2)
        self.sector_data = sector_data
        # currently moving
        self.active = True
        # chip before currently active
        self.locked = False
        # acknowledge in the map
        self.tracked = False
    
    def get_sector(self, pos, sec_data):
        # checks if pos (centerxy) is in given range
        for e in sec_data:
            if pos[0] in range(e[1][0], e[1][1]) and pos[1] in range(e[2][0], e[2][1]):
                return e[0]

    def update(self):
        self.sector = self.get_sector((self.rect.centerx, self.rect.centery), self.sector_data)
