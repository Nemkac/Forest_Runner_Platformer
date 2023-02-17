import pygame
import settings
#from settings import import_folder
import settings

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        #self.image = pygame.Surface((size,2*size))
        #self.image.fill('firebrick3')
        self.import_animations()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)  
        self.status = 'idle' 
        self.bottom = False   
        self.top = False
        self.left = False
        self.right = False

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate_enemy()

    def animate_enemy(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        width = image.get_rect().width
        height = image.get_rect().height
        image = pygame.transform.scale(image, (width +10, height +10))
        self.image = image
    
        if self.bottom and self.right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.bottom and self.left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.bottom:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

    def import_animations(self):
        character_path = 'images/enemy/'
        self.animations = {'idle':[], 'run':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = settings.import_folder(full_path)