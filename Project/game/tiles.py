import pygame
import numpy as np
import settings

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size, kind):
        super().__init__()
        if kind == 'grass':
            image = settings.grass_image
            self.image = image
        if kind == 'dirt':
            image = settings.dirt_image
            self.image = image
        if kind == 'left_corner_grass':
            image = settings.corner_grassL
            self.image = image
        if kind == 'right_corner_grass':
            image = settings.corner_grassR
            self.image = image
        if kind == 'dirt_left':
            image = settings.left_dirt
            self.image = image
        if kind == 'dirt_right':
            image = settings.right_dirt
            self.image = image
        if kind == 'dirt_corner_left':
            image = settings.left_down_dirt
            self.image = image
        if kind == 'dirt_corner_right':
            image = settings.right_down_dirt
            self.image = image
        if kind == 'down_dirt':
            image = settings.down_dirt
            self.image = image
        if kind == 'island_grass_left':
            image = settings.islandL
            self.image = image
        if kind == 'island_grass_right':
            image = settings.islandR
            self.image = image
        if kind == 'island_grass':
            image = settings.island
            self.image = image
        if kind == 'dot_grass_right':
            image = settings.dot_grass_r
            self.image = image
        if kind == 'dot_grass_left':
            image = settings.dot_grass_L
            self.image = image
        if kind == 'dirt_pillar':
            image = settings.dirt_pillar
            self.image = image
        if kind == 'grass_pillar':
            image = settings.grass_pillar
            self.image = image
        if kind == 'GLD':
            image = settings.grassL_dirt
            self.image = image
        #self.image = pygame.Surface((size,size))
        #self.image.fill('darkolivegreen')
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift):
        self.rect.x += x_shift