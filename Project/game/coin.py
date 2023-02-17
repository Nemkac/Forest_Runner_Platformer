import pygame
import settings

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.import_animations()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['coin'][self.frame_index]
        self.rect = self.image.get_rect()
        self.status = 'coin'
        self.rect.center = (x, y)
        pygame.draw.circle(settings.screen, settings.projectile_color, (x, y), settings.coin_radius)

    def import_animations(self):
        character_path = 'images/'
        self.animations = {'coin':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = settings.import_folder(full_path)
    
    def animate_coin(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        width = image.get_rect().width
        height = image.get_rect().height
        image = pygame.transform.scale(image, (width * 2.5, height * 2.5))
        self.image = image

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate_coin()


class Meat(pygame.sprite.Sprite):
    def __init__(self, pos):  
        super().__init__()
        image = settings.meat
        self.image = image
        self.rect = image.get_rect(topleft = pos)

    def update(self, x_shift):
        self.rect.x += x_shift

class Key(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        image = settings.key
        self.image = image
        self.rect = image.get_rect(topleft = pos)

    def update(self, x_shift):
        self.rect.x += x_shift