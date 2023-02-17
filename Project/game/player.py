import pygame, sys
import numpy as np
import settings
import settings
from projectile import Projectile
from level import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.import_animations()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.initial_speed = 360
        self.status = 'idle'
        self.facing_right = True     
        self.bottom = False   
        self.top = False
        self.left = False
        self.right = False

        #Players movement using RK4 before screen scroll begins
        self.direction = pygame.math.Vector2(0,0)
        k1_x = self.initial_speed * settings.dt
        k2_x = (self.initial_speed + k1_x / 2) * settings.dt
        k3_x = (self.initial_speed + k2_x / 2) * settings.dt
        k4_x = (self.initial_speed + k3_x) * settings.dt
        x = (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
        self.player_speed = x
        self.gravity = -0.981
        self.initial_jump_speed = -20
        self.canJump = 1

    def import_animations(self):
        character_path = 'images/character/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[], 'hurt':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = settings.import_folder(full_path)

    def animate_player(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        width = image.get_rect().width
        height = image.get_rect().height
        image = pygame.transform.scale(image, (width * 2.5, height * 2.5))
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        if self.bottom and self.right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.bottom and self.left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.bottom:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.top and self.right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.top and self.left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.top:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if self.rect.y > 800:
            pygame.quit()
            sys.exit()

        if keys[pygame.K_UP]:
            if self.direction.y == 0 and self.canJump:
                settings.jump_sound.play()
                self.jump()

    def animation_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else: 
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def hurt_status(self):
        self.status = 'hurt'

    def apply_gravity(self):
        self.direction.y -= self.gravity
        k1_y = self.initial_jump_speed * settings.dt
        k2_y = (self.initial_jump_speed + k1_y / 2) * settings.dt
        k3_y = (self.initial_jump_speed + k2_y / 2) * settings.dt
        k4_y = (self.initial_jump_speed + k3_y) * settings.dt
        jump_speed = (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6
        self.direction.y -= jump_speed
        self.rect.y += self.direction.y

    def jump(self):
        k1_y = self.initial_jump_speed * settings.dt
        k2_y = (self.initial_jump_speed + k1_y / 2) * settings.dt
        k3_y = (self.initial_jump_speed + k2_y / 2) * settings.dt
        k4_y = (self.initial_jump_speed + k3_y) * settings.dt
        jump_speed = (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6
        self.direction.y = jump_speed
        self.direction.y += self.initial_jump_speed

    def update(self):
        self.get_input()
        self.animation_status()
        self.animate_player()


        
        