import pygame
from tiles import Tile
import settings
from player import Player
from enemy import Enemy
import settings
from projectile import Projectile 
import random
import math
from house import House
from coin import Coin, Meat, Key
import numpy as np

class Level:
    def __init__(self,level_data,surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.level_map = level_data
        self.world_shift = 0
        self.jump = 1
        self.spawned_balls = []
        self.current_x = 0
        self.projectiles = 5
        self.projectiles_list = []
        self.cooldown = 0
        self.font = pygame.font.Font("images\PressStart2P-Regular.ttf", 16)
        self.font2 = pygame.font.Font("images\PressStart2P-Regular.ttf", 14)
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.world_shift_counter = 0
        self.projectile = None
        self.collision_flag = 0
        self.collision_limiter = 0
    
    def shift(self):
        return self.world_shift

    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemy = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.houses = pygame.sprite.GroupSingle()
        self.coins = pygame.sprite.Group()
        self.snacks = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()
        self.void_tiles = pygame.sprite.Group()

        for row_index,row in enumerate(layout):
            for col_index,cell in enumerate(row):
                x = col_index * settings.tile_size #skaliranje
                y = row_index * settings.tile_size
                if cell == 'X':
                    kind = 'grass'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == 'Y':
                    kind = 'dirt'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == 'I':
                    kind = 'island_grass'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == 'R':
                    kind = 'dot_grass_right'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == 'L':
                    kind = 'dot_grass_left'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == 'Q':
                    kind = 'dirt_pillar'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == 'W':
                    kind = 'grass_pillar'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == 'K':
                    kind = 'GLD'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == '1':
                    kind = 'left_corner_grass'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == '2':
                    kind = 'right_corner_grass'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == '3':
                    kind = 'dirt_left'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == '4':
                    kind = 'dirt_right'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == '5':
                    kind = 'dirt_corner_left'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == '6':
                    kind = 'dirt_corner_right'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == '7':
                    kind = 'down_dirt'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == '8':
                    kind = 'island_grass_left'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == '9':
                    kind = 'island_grass_right'
                    tile = Tile((x,y),settings.tile_size, kind)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x,y))
                    self.starting_position = (x,y)
                    self.player.add(player_sprite)
                if cell == 'E':
                    enemy_sprite = Enemy((x,y),32)
                    self.enemy.add(enemy_sprite) 
                if cell == 'H':
                    kind = 'house'
                    house = House((x, y), settings.tile_size)
                    self.houses.add(house)
                if cell == 'C':
                    coin = Coin(x + 10, y + 20)
                    self.coins.add(coin)
                if cell == 'M':
                    meat = Meat((x+10, y+20))
                    self.snacks.add(meat)
                if cell == '+':
                    key = Key((x+10, y+20))
                    self.keys.add(key)

    def find_current_position(self):
        player = self.player.sprite
        return (player.rect.x - 80, player.rect.y)
                
    def scroll_x(self):
        #ball = self.ball.sprites
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < settings.screen_width/3 and direction_x < 0:
            self.world_shift = 6
            self.world_shift_counter += 6
            player.player_speed = 0
        elif player_x > settings.screen_width - (settings.screen_width/3) and direction_x > 0:
            self.world_shift = -6
            self.world_shift_counter -= 6
            player.player_speed = 0
        else:
            self.world_shift = 0
            #RK4 method that updates player's speed once scroll is done
            player.initial_speed = 350
            k1_x = player.initial_speed * settings.dt
            k2_x = (player.initial_speed + k1_x / 2) * settings.dt
            k3_x = (player.initial_speed + k2_x / 2) * settings.dt
            k4_x = (player.initial_speed + k3_x) * settings.dt
            x = (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
            player.player_speed = x
            player.player_speed = player.player_speed

    def respawn(self):
        player = self.player.sprite
        if player.rect.y > 800:
            self.world_shift = -self.world_shift_counter
            self.world_shift_counter = 0
            player_sprite = Player(self.starting_position)
            self.player.add(player_sprite)
            settings.health_counter -= 1
            player.status = 'hurt'

    #collisions 
    def horizontal_movement_collision(self):    #rect on rect
        player = self.player.sprite
        player.rect.x += player.direction.x * player.player_speed
        
        for sprite in self.tiles.sprites():
            if self.intersect_rect(player.rect, sprite.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right + 5
                    player.left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left - 3
                    player.right = True
                    self.current_x = player.rect.right

        if player.left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.left = False
        if player.right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.right = False
        
    def vertical_movement_collision(self):  #rect on rect
        player = self.player.sprite
        player.apply_gravity()

        player.canJump = 1
        for sprite in self.tiles.sprites():
            if self.intersect_rect(player.rect, sprite.rect):
                if player.direction.x != 0:
                    if settings.grass_sound_timer == 0:
                        settings.grass_sound_timer = 30
                        random.choice(settings.grass_sounds).play()

                if player.direction.y > 0 :
                    player.rect.bottom  = sprite.rect.top
                    player.direction.y = 0
                    player.bottom = True
                elif player.direction.y < 0:
                    player.canJump = 0
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.top = True

        if player.bottom and player.direction.y < 0 or player.direction.y > 1:
            player.bottom = False
        if player.top and player.direction.y > 0:
            player.top = False 

    def enemy_ground_collision(self):   #rect on rect
        enemy = self.enemy.sprites
        for sprite in self.tiles.sprites():
            for enemy in self.enemy.sprites():
                if self.intersect_rect(sprite.rect, enemy.rect):
                    enemy.rect.bottom = sprite.rect.top
                    enemy.bottom = True      
                                        
    def player_enemy_collision(self):
        player = self.player.sprite
        for enemy in self.enemy.sprites():
            if self.intersect_rect(player.rect, enemy.rect):
                self.world_shift = -self.world_shift_counter
                self.world_shift_counter = 0
                player_sprite = Player(self.starting_position)
                self.player.add(player_sprite)
                settings.health_counter -= 1
                player.hurt_status()

    def player_projectile_collision(self):  #circle on rect
        player = self.player.sprite
        projectiles = self.projectile_group.sprites()

        for projectile in projectiles:
            projectile_center = (projectile.rect.centerx, projectile.rect.centery)
            if self.intersect_circle(player.rect, settings.radius, projectile_center):
                pygame.sprite.Sprite.kill(projectile)
                self.projectiles += 1
                settings.projectile_counter += 1

    def projectile_ground_collision(self):  #circle on rect
        projectiles = self.projectile_group.sprites()
        tiles = self.tiles.sprites()

        for tile in tiles:
            for projectile in projectiles:
                projectile_center = (projectile.rect.centerx, projectile.rect.centery)

                if self.intersect_circle(tile.rect, settings.radius, projectile_center):
                    projectile.collision_counter += 1

                    if projectile.direction > 0 :
                        self.collision_limiter = 9
                    elif projectile.direction < 0:
                        self.collision_limiter = 25
                    if projectile.collision_counter > self.collision_limiter:
                        projectile.fall()
                        
                    if self.collision_flag == 1:
                        projectile.stop_projectile()
                    elif self.collision_flag == 2:
                        projectile.fall()
                    else:
                        pass

    def projectile_enemy_collision(self):   #circle on rect
        projectiles = self.projectile_group.sprites()
        enemy_list = self.enemy.sprites()

        for enemy in enemy_list:
            for projectile in projectiles:
                projectile_center = (projectile.rect.centerx, projectile.rect.centery)

                if self.intersect_circle(enemy.rect, settings.radius, projectile_center):
                    pygame.sprite.Sprite.kill(projectile)
                    pygame.sprite.Sprite.kill(enemy)
                    self.projectiles += 1
                    settings.projectile_counter += 1

    def level_end(self):
        player = self.player.sprite
        house = self.houses.sprite

        if self.intersect_rect(player.rect, house.rect):
            settings.current_level += 1


    def collect_coin(self):
        player = self.player.sprite
        coins = self.coins.sprites()

        for coin in coins:
            if self.intersect_circle(player.rect, settings.coin_radius, coin.rect.center):
                pygame.sprite.Sprite.kill(coin)
                settings.score += 10
                settings.coin_pickup_sound.play()

    def collect_snack(self):
        player = self.player.sprite
        snacks = self.snacks.sprites()

        for snack in snacks:
            if self.intersect_rect(player.rect, snack.rect):
                if settings.health_counter < 5:
                    pygame.sprite.Sprite.kill(snack)
                    settings.health_counter += 1
                    settings.eat_sound.play()

    def collect_key(self):
        player = self.player.sprite
        keys = self.keys.sprites()

        for key in keys:
            if self.intersect_rect(player.rect, key.rect):
                pygame.sprite.Sprite.kill(key)
                settings.key_sound.play()
                settings.key_collected = True

    def next_level(self):
        player = self.player.sprite
        house = self.houses.sprite

        if self.intersect_rect(player.rect, house.rect):
            if player.rect.left == house.rect.left and settings.key_collected:
                settings.next_level_trigger = True


    # sat
    def intersect_rect(self,r1, r2):
        player_axes = [
            (r1.x + r1.width, 0),
            (0, r1.y + r1.height)
        ]

        sprite_axes = [
            (r2.x + r2.width, 0),
            (0, r2.y + r2.height)
        ]

        for axis in player_axes + sprite_axes:
            axis_min_player, axis_max_player = self.project(r1, axis)
            axis_min_rect, axis_max_rect = self.project(r2, axis)

            if axis_max_player <= axis_min_rect or axis_max_rect <= axis_min_player:
                return False
        return True

    def intersect_circle(self, rect, radius, center):
            circle_distance_x = abs(center[0] - rect.centerx)
            circle_distance_y = abs(center[1] - rect.centery)
            if circle_distance_x > rect.w/2.0 + radius or circle_distance_y > rect.h/2.0 + radius:
                return False
            if circle_distance_x < rect.w/2.0:
                #up-down collision
                self.collision_flag = 1
                return True
            if circle_distance_y <= rect.h/2.0:
                #left-right collision
                self.collision_flag = 2
                return True

            self.collision_flag = 3
            corner_x = circle_distance_x - rect.w/2.0
            corner_y = circle_distance_y - rect.h/2.0
            corner_distance = corner_x**2.0 + corner_y**2.0
            return corner_distance <= radius**2.0

    def project(self,rect, axis):
        dot_product = rect.x * axis[0] + rect.y * axis[1]
        return dot_product, dot_product + rect.width * axis[0] + rect.height * axis[1]

    def can_jump(self):
        return self.jump
    
    # projectile
    def can_throw(self):    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.cooldown == 0 and self.projectiles > 0:
            self.cooldown = 180
            self.throw_projectile()
            self.projectiles -= 1
            settings.projectile_counter -= 1
            
    def throw_projectile(self):
        player = self.player.sprite
        if (player.facing_right):
            direction = 1
            proj_x = player.rect.centerx + 30
            proj_y = player.rect.centery - 30
        else:
            direction = -1
            proj_x = player.rect.centerx - 30
            proj_y = player.rect.centery - 30
        # proj_x = player.rect.centerx + 30
        # proj_y = player.rect.centery - 30
        projectile_coords = (proj_x, proj_y)
        projectile = Projectile(proj_x,proj_y,direction)
        self.projectile_thrown = True
        self.projectile_group.add(projectile)
        self.projectiles_list.append(self.projectile)

    def projectile_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def draw_reload(self):
        if (self.cooldown) > 0:
            x = round(self.cooldown / 60,2)
            text = 'PROJECTILE COOLDOWN :' + str(x)
        else:
            text = 'PROJECTILE IS READY'
        
        img = self.font.render(text,True,self.black)
        settings.screen.blit(img,(30,60))

        text_score = "Score: " + str(settings.score)
        score_img = self.font.render(text_score, True, self.black)
        settings.screen.blit(score_img, (30, 90))

    def run(self):
        # tiles
        self.enemy.update(self.world_shift)
        self.tiles.update(self.world_shift)
        self.projectile_group.update(self.world_shift)
        self.void_tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.void_tiles.draw(self.display_surface)
        self.scroll_x()
        self.draw_reload()
        
        # enemy
        self.enemy.draw(self.display_surface)
        self.enemy_ground_collision()
        self.projectile_enemy_collision()

        # projectile
        self.can_throw()
        self.projectile_cooldown()
        self.projectile_ground_collision()
        self.player_projectile_collision()
        self.projectile_group.draw(self.display_surface)

        
        # player
        self.player.update()
        self.can_jump()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        self.player_enemy_collision()
        self.respawn()
        self.level_end()

        #house
        self.houses.draw(self.display_surface)
        self.houses.update(self.world_shift)

        #self.stampaj()
        #Objects
        self.coins.draw(self.display_surface)
        self.coins.update(self.world_shift)
        self.collect_coin()
        self.snacks.draw(self.display_surface)
        self.collect_snack()
        self.snacks.update(self.world_shift)
        self.keys.draw(self.display_surface)
        self.keys.update(self.world_shift)
        self.collect_key()

    def movement(self, player_direction, speed, dt):
        player = self.player.sprite
        k1_x = speed * dt
        k2_x = (speed + k1_x / 2) * dt
        k3_x = (speed + k2_x / 2) * dt
        k4_x = (speed + k3_x) * dt     

        player.rect.x += player_direction * (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6

