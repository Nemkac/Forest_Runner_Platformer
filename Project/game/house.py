import pygame
import settings

class House(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        image = settings.house
        self.image = image
        self.rect = image.get_rect(topleft = pos)

    def update(self, x_shift):
        self.rect.x += x_shift