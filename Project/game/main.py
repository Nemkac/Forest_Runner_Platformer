import pygame, sys
import settings
from level import Level
from menus import *
from player import Player
from pygame import mixer


pygame.init()
mixer.init(44100, -16,2,2048)
bg_music = mixer.music.load("sounds\\bgmusic.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.6)
mixer.set_num_channels(64)


def draw_bg(bg_images, bg_width, scroll):
    for x in range(len(settings.level_map_3) * settings.tile_size):
        speed = 1
        for i in bg_images:
            settings.screen.blit(i, (x * bg_width + scroll * speed, 0))
            speed += 0.2

def run():
    
    player = pygame.sprite.GroupSingle()

    bg_images = []
    for i in range(1, 3):
        background = pygame.transform.scale(pygame.image.load(f"images\\bg-{i}.png").convert_alpha(), (settings.screen_width, len(settings.level_map) * settings.tile_size))
        bg_images.append(background)
    bg_width = bg_images[0].get_width()

    bg_scroll = 0

    clock = pygame.time.Clock()
    
    if settings.current_level == 1:
        level_map = settings.level_map
    elif settings.current_level == 2:
        level_map = settings.level_map_2
    elif settings.current_level == 3:
        level_map = settings.level_map_3
    else:
        level_map = settings.level_map

    for row_index,row in enumerate(level_map):
        for col_index,cell in enumerate(row):
            x = col_index * settings.tile_size #skaliranje
            y = row_index * settings.tile_size
            if cell == 'P':
                character = Player((x, y))
                player.add(character)

    pl = player.sprite
    player_x = pl.rect.centerx
    running = True

    level = Level(level_map, settings.screen)
    while running:
        if settings.grass_sound_timer > 0:
            settings.grass_sound_timer -= 1

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        if player_x < settings.screen_width/2 :
            bg_scroll -= 0.5
        elif player_x > settings.screen_width - (settings.screen_width/2):
            bg_scroll += 0.2

        draw_bg(bg_images, bg_width, bg_scroll)

        level.run()
        settings.next_level()

        #Draw projectile bar
        if settings.projectile_counter == 5:
            settings.screen.blit(settings.p5, (30, 30))
        elif settings.projectile_counter == 4:
            settings.screen.blit(settings.p4, (30, 30))
        elif settings.projectile_counter == 3:
            settings.screen.blit(settings.p3, (30, 30))
        elif settings.projectile_counter == 2:
            settings.screen.blit(settings.p2, (30, 30))
        elif settings.projectile_counter == 1:
            settings.screen.blit(settings.p1, (30, 30))
        else:
            settings.screen.blit(settings.p0, (30, 30))


        #Draw health bar
        if settings.health_counter == 5:
            settings.screen.blit(settings.h5, (900, 30))
        elif settings.health_counter == 4:
            settings.screen.blit(settings.h4, (900, 30))
        elif settings.health_counter == 3:
            settings.screen.blit(settings.h3, (900, 30))
        elif settings.health_counter == 2:
            settings.screen.blit(settings.h2, (900, 30))
        elif settings.health_counter == 1:
            settings.screen.blit(settings.h1, (900, 30))
        else:
            running = False
            # pygame.quit()
            # sys.exit()

        pygame.display.update()
        clock.tick(60)
    
if __name__ == "__main__":
    main_menu()