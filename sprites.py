import pygame as pg
from computations import *
from settings import *
import random as rdm

class Chip(pg.sprite.Sprite):
    def __init__(self, sector_data, spwn):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((GRIDSTEP, GRIDSTEP))
        self.type = rdm.randint(1, 4)
        self.color = CHIP_COLORS[self.type]
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.l = len(spwn) - 1
        self.x = rdm.randint(0, self.l)
        self.rect.center = (spwn[self.x], -GRIDSTEP)
        self.mov = True
        self.sector_data = sector_data
        self.locked = False
    
    def get_sector(self, pos, sector_data):
        for e in sector_data:
            if pos[0] in range(e[1][0], e[1][1]) and pos[1] in range(e[2][0], e[2][1]):
                return e[0]
    
    def movement(self):
        if self.rect.bottom < HEIGHT:
                self.rect.y += SPEED
        else:
            self.rect.bottom = HEIGHT
            self.mov = False

    def update(self):
        if self.mov:
            self.movement()
        elif not(self.locked):
            # lock it and update sector map!
            self.sector = self.get_sector((self.rect.centerx, self.rect.centery), self.sector_data)
            self.locked = True