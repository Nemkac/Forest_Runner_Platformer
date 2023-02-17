import pygame
import settings
import numpy as np
import math

class Projectile(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        image = settings.projectile
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.collision_counter = 0
        self.gravity = -0.981
        pygame.draw.circle(settings.screen, settings.projectile_color, (x, y), settings.radius)
    
        self.GRAVITY = np.array([0, 981])
        self.DT = 0.02
        self.BALL_WIDTH, self.BALL_HEIGHT = 20, 20

        # Initial conditions
        self.velocity = np.array([self.direction*200, -200])
        self.rotation = 300
        self.rotational_velocity = 3
        self.angle = 5
        self.TORQUE = 3
        self.air_resistance = 0.008
        self.friction = 0.007
        
    def rk4(self, position, velocity, rotation, rotational_velocity):
        k1 = self.DT * velocity
        l1 = self.DT * (self.GRAVITY - 0.1 * velocity)
        r1 = self.DT * rotational_velocity
        t1 = self.DT * (self.TORQUE - 0.1 * rotational_velocity)
        
        k2 = self.DT * (velocity + 0.5 * l1)
        l2 = self.DT * (self.GRAVITY - 0.1 * (velocity + 0.5 * l1))
        r2 = self.DT * (rotational_velocity + 0.5 * t1)
        t2 = self.DT * (self.TORQUE - 0.1 * (rotational_velocity + 0.5 * t1))
        
        k3 = self.DT * (velocity + 0.5 * l2)
        l3 = self.DT * (self.GRAVITY - 0.1 * (velocity + 0.5 * l2))
        r3 = self.DT * (rotational_velocity + 0.5 * t2)
        t3 = self.DT * (self.TORQUE - 0.1 * (rotational_velocity + 0.5 * t2))
        
        k4 = self.DT * (velocity + l3)
        l4 = self.DT * (self.GRAVITY - 0.1 * (velocity + l3))
        r4 = self.DT * (rotational_velocity + 0.5 * t3)
        t4 = self.DT * (self.TORQUE - 0.1 * (rotational_velocity + t3))
        
        position = position + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        velocity = velocity + (l1 + 2 * l2 + 2 * l3 + l4) / 6 
        rotation = (rotation + (r1 + 2 * r2 + 2 * r3 + r4) / 6 )
        
        if self.direction > 0:
            rotational_velocity = (1-(self.air_resistance + self.friction))*rotational_velocity + (t1 + 2 * t2 + 2 * t3 + t4) / 6
        if self.direction < 0:
            rotational_velocity = (1-(self.air_resistance + self.friction))*rotational_velocity - (t1 + 2 * t2 + 2 * t3 + t4) / 6
        return position,velocity,rotation,rotational_velocity
        
    def stop_total(self):
        self.velocity[0] = 0
        self.velocity[1] = 0
        self.GRAVITY[0] = 0
        self.GRAVITY[1] = 0
        self.DT = 0
        self.rotation = 0
        self.rotational_velocity = 0
        self.angle = 0
        self.TORQUE = 0
        
    def stop_projectile(self):
        self.velocity[1] = 0


    def fall(self):
        # Initial conditions
        self.rotation = 0
        self.rotational_velocity = 0
        self.angle = 0
        self.TORQUE = 0
        self.velocity[0] = 0
        self.rect.y -= self.gravity
        self.collision_counter = -99999

    def change_movement(self):
        self.velocity_y -= self.gravity
        dx = 0
        dy = self.velocity_y
        #update projectile position
        self.rect.x += dx
        self.rect.y += dy
        

    '''def update(self,world_shift):
        pos,self.velocity,self.rotation,self.rotation_velocity = self.rk4((self.rect.x,self.rect.y),
                                                                          self.velocity,self.rotation,
                                                                          self.rotation_velocity)
        self.rect.x = pos[0] + world_shift
        self.rect.y = pos[1]

        rot_angle = math.radians(self.angle)
        cos_angle = math.cos(rot_angle)
        sin_angle = math.sin(rot_angle)
        
        self.rect.x = self.rect.x + self.rect.width / 2 * cos_angle
        self.rect.y = self.y + self.rect.height / 2 * sin_angle'''

    def update(self,world_shift):
        position, self.velocity, self.rotation, self.rotational_velocity = self.rk4(
        (self.rect.x,self.rect.y), self.velocity, self.rotation, self.rotational_velocity)
        self.rect.x = position[0] + world_shift
        self.rect.y = position[1]
        self.rect.x += self.rotational_velocity * math.cos(math.radians(self.rotation))
        self.rect.y += self.rotational_velocity * math.sin(math.radians(self.rotation))
        #m petakovic 53