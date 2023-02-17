import pygame
from os import walk
from pygame import mixer
from level import Level

#Grass Left - 1
#Grass Right - 2
#Dirt Left - 3
#Dirt Right - 4
#Corner dirt Left - 5
#Corner dirt right - 6
#Down dirt - 7
#Island grass left - 8
#island grass right - 9
#island dirt - I
#dot grass right = R
#dirt pillar - Q
#grass pillar - W
#grass dot left dirt - K
#dot_grass_left - L
#coin - C
#meat - M
#house - H
#key - +
#void - 0

level_map = [
'                            ',
'                            ',
'                      H     ',
' 12   8II9            89    ',
' 34 P        EM             ',
' 3RX2     8XXXI9         89 ',
' 3Y76      3Y4     E        ',
' 56    W   3Y4    12 8X2C   ',
'      EQ  1LY4CE  34  3R2+  ',
' C  1XXK  3YYRX2  34  3YR2  ',
'1XXXLYY4  3YYYY4  34  3YY4  ',]

level_map_2 = [
    '                                                                             ',
    '                                                                             ',
    '                                                                             ',
    '                                                              C              ',
    '                                        M                 E 1XXI9     EH     ',
    '                                       8II9            1XXXXLY4      1XX2    ',
    '                                   E       89    C    8777YYYY4     1LYYR2   ',
    '       EC     EC     1X2         1XX9           1X9       3YYY4    1LYYYY4   ',
    '      1XX9  8IXX2   877RX2      1LY4           1L4  W  C  3YYY4+E 8LYYYY6    ',
    '  P 1XLY4     3Y4      3Y4C  E M3YYR2   C      3Y4  Q1XXXXLYYYRX2  57776     ',
    ' 1XXLYYY4     3Y4      3YRXXXXXXLYYYRXXXXXX2  1LY4  Q3YYYYYYYYYY4            ',]


level_map_3 = [
    '                                                                                                                                  ',
    '                                                                                                                                  ',
    '                                1XXX2                                                                                             ',
    '                   E C   E      3YYYRXXXXXX2                                                                                      ',
    '                C 1XXXXXXXXX2   57777777777RXXXXXX2                                   E M                                 E  +H   ',
    '             E 1XXLYYYY777776              57777777IIII9                     E     8IXXXX2                              8IIXXXX9  ',
    '    P       1XXLYY77776                                                     8II9     3YYYRXI9                  C  1XXX9    3YY4   ',
    ' 8IXXXI9  8ILYYYY4                               M                 1XXX2             57YYY6    C              1XXXLYY4     3YY4   ',
    '   3Y4      3YYYY4        E                     1X2             1XXLYYYRI9             576    8IXX2  E  C 1XXXLYYYYYY4     3YY4   ',
    '   3Y4      3YYYY4  C   1XXXX2  1XXXXXX2  C    1LYR2      E   8XLYYYYYY4                        3YRXXXXXXXLYYYYYYYYYY4     3YY4   ',
    '   3Y4      3YYYYRXXXXXXLYYYY4003YYYYYYRXXXXXXXLYYYRXXXXXXXX2  3YYYYYYY4                        3YYYYYYYYYYYYYYYYYYYY4     3YY4   ',]


#INITIAL GAME SETTINGS
pygame.mixer.init(44100, -16,2,2048)
tile_size = 64
screen_width = 1200
screen_height = len(level_map) * tile_size
fps = 10
dt = 1/60
screen = pygame.display.set_mode((screen_width,screen_height))
current_level = 1
score = 0
coin_radius = 15
key_collected = False
next_level_trigger = False


#IMAGES
day_bg = pygame.transform.scale(pygame.image.load("images\\bg-1.png"), (1200, 800))
night_bg = pygame.image.load("images\\nightBG.png")
icon = pygame.image.load("images\character\idle\9.png")
pygame.display.set_caption("Forest Runner")
pygame.display.set_icon(icon)
projectile = pygame.transform.scale(pygame.image.load("images\projectile.png"), (20, 20))

#MAP IMAGES
grass_image = pygame.transform.scale(pygame.image.load("images\\tiles\grass.png"), (65, 65))
dirt_image = pygame.transform.scale(pygame.image.load("images\\tiles\dirt.png"), (65, 65))
corner_grassL = pygame.transform.scale(pygame.image.load("images\\tiles\corner_grass.png"), (65, 65))
corner_grassR = pygame.transform.scale(pygame.image.load("images\\tiles\corner_grassR.png"), (65, 65))
corner_dirtL = pygame.transform.scale(pygame.image.load("images\\tiles\dirt_cornerL.png"), (65, 65))
corner_dirtR = pygame.transform.scale(pygame.image.load("images\\tiles\dirt_cornerR.png"), (65, 65))
down_dirt = pygame.transform.scale(pygame.image.load("images\\tiles\dirtD.png"), (65, 65))
left_down_dirt = pygame.transform.scale(pygame.image.load("images\\tiles\dirt_cornerL.png"), (65, 65))
right_down_dirt = pygame.transform.scale(pygame.image.load("images\\tiles\dirt_cornerR.png"), (65, 65))
left_dirt = pygame.transform.scale(pygame.image.load("images\\tiles\dirtL.png"), (65, 65))
right_dirt = pygame.transform.scale(pygame.image.load("images\\tiles\dirtR.png"), (65, 65))
islandL = pygame.transform.scale(pygame.image.load("images\\tiles\islandL.png"), (65, 65))
island = pygame.transform.scale(pygame.image.load("images\\tiles\island.png"), (65, 65))
islandR = pygame.transform.scale(pygame.image.load("images\\tiles\islandR.png"), (65, 65))
dot_grass_r = pygame.transform.scale(pygame.image.load("images\\tiles\dot_grassR.png"), (65, 65))
dot_grass_L = pygame.transform.scale(pygame.image.load("images\\tiles\dot_grassL.png"), (65, 65))
dirt_pillar = pygame.transform.scale(pygame.image.load("images\\tiles\dirt_pillar.png"), (65, 65))
grass_pillar = pygame.transform.scale(pygame.image.load("images\\tiles\grass_pilar.png"), (65, 65))
grassL_dirt = pygame.transform.scale(pygame.image.load("images\\tiles\grassL_dirt.png"), (65, 65))
house = pygame.transform.scale(pygame.image.load("images\house.png"), (65, 65))
meat = pygame.transform.scale(pygame.image.load("images\meat.png"), (41, 41))
key = pygame.transform.scale(pygame.image.load("images\key.png"), (20, 36))

#HEALTH BAR
health_counter = 5
h5 = pygame.transform.scale(pygame.image.load("images\health_bar\\5.png"), (280, 53))
h4 = pygame.transform.scale(pygame.image.load("images\health_bar\\4.png"), (280, 53))
h3 = pygame.transform.scale(pygame.image.load("images\health_bar\\3.png"), (280, 53))
h2 = pygame.transform.scale(pygame.image.load("images\health_bar\\2.png"), (280, 53))
h1 = pygame.transform.scale(pygame.image.load("images\health_bar\\1.png"), (280, 53))

#PROJECTILE_BAR
projectile_counter = 5
p5 = pygame.transform.scale(pygame.image.load("images\projectile_bar\\5.png"), (220, 23))
p4 = pygame.transform.scale(pygame.image.load("images\projectile_bar\\4.png"), (220, 23))
p3 = pygame.transform.scale(pygame.image.load("images\projectile_bar\\3.png"), (220, 23))
p2 = pygame.transform.scale(pygame.image.load("images\projectile_bar\\2.png"), (220, 23))
p1 = pygame.transform.scale(pygame.image.load("images\projectile_bar\\1.png"), (220, 23))
p0 = pygame.transform.scale(pygame.image.load("images\projectile_bar\\0.png"), (220, 23))

#PROJECTILE SETTINGS
radius = 10
projectile_color = 'darkolivegreen'

#SOUNDS 
key_sound = mixer.Sound("sounds\key.wav")
eat_sound = mixer.Sound("sounds\eating.wav")
jump_sound = mixer.Sound("sounds\jump.wav")
grass_sounds = [mixer.Sound("sounds\grass_0.wav"), mixer.Sound("sounds\grass_1.wav")]
coin_pickup_sound = mixer.Sound("sounds\coin.wav")
bg_music = mixer.music.load("sounds\\bgmusic.wav")
grass_sound_timer = 0
jump_sound.set_volume(0.6)
coin_pickup_sound.set_volume(0.5)
grass_sounds[0].set_volume(0.5)
grass_sounds[1].set_volume(0.5)


def import_folder(path):
    surface_list = []
    
    for _, __, img_files in walk(path):
        for img in img_files:
            full_path = path + '/' + img
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface) 
    
    return surface_list


def next_level():
    if key_collected and next_level_trigger:
        if current_level == 2:
            level_map = level_map_2
            new_level = Level(level_map, screen)
            new_level.run()

        if current_level == 3:
            level_map = level_map_3
            new_level = Level(level_map, screen)
            new_level.run()
        
            