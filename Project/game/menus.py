import pygame
from button import Button
import sys
from main import run
import settings

#INITIAL SETTINGS
font = pygame.font.Font("images\PressStart2P-Regular.ttf", 64)

def main_menu(): #MAIN MENU FUNCTION
    menu = True
    while menu:
        menu_mouse_pos = pygame.mouse.get_pos() #Store current mouse position into a menu_mouse_pos variable
        settings.screen.blit(settings.day_bg, (0, 0))

        MENU_TEXT = font.render("FOREST RUNNER", True, "white")
        MENU_RECT = MENU_TEXT.get_rect(center = (640, 100))

        #Using Button.py module to implment buttons
        PLAY_BUTTON = Button(None, pos = (640, 300), text_input = "PLAY", font = font, base_color = "White", hovering_color = "black")
        LEVELS_BUTTON = Button(None ,pos = (640, 500), text_input = "LEVELS", font = font, base_color = "White", hovering_color = "black")

        buttons = [PLAY_BUTTON, LEVELS_BUTTON]  #Store all previously created buttons in one it list

        for button in buttons:
            button.change_color(menu_mouse_pos)
            button.update(settings.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(menu_mouse_pos):
                    settings.health_counter = 5
                    settings.current_level = 1
                    settings.projectile_counter = 5
                    run()
                if LEVELS_BUTTON.check_for_input(menu_mouse_pos):
                    levels_menu()

        settings.screen.blit(MENU_TEXT, MENU_RECT)
        pygame.display.update()



def levels_menu():
    lvl_Menu = True
    while lvl_Menu:

        menu_mouse_pos = pygame.mouse.get_pos() #Store current mouse position into a menu_mouse_pos variable
        settings.screen.blit(settings.day_bg, (0, 0))
        BACK_BUTTON = Button(None, pos = (100, 100), text_input = "<", font = font, base_color = "White", hovering_color = "black")
        LEVEL1 = Button(None, pos = (640, 100), text_input = "LEVEL 1", font = font, base_color = "White", hovering_color = "black")
        LEVEL2 = Button(None ,pos = (640, 250), text_input = "LEVEL 2", font = font, base_color = "White", hovering_color = "black")
        LEVEL3 = Button(None ,pos = (640, 400), text_input = "LEVEL 3", font = font, base_color = "White", hovering_color = "black")
        buttons = [LEVEL1, LEVEL2, LEVEL3, BACK_BUTTON]  #Store all previously created buttons in one it list

        for button in buttons:
            button.change_color(menu_mouse_pos)
            button.update(settings.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL1.check_for_input(menu_mouse_pos):
                    settings.health_counter = 5
                    settings.current_level = 1
                    settings.projectile_counter = 5
                    run()
                if LEVEL2.check_for_input(menu_mouse_pos):
                    settings.health_counter = 5
                    settings.current_level = 2
                    settings.projectile_counter = 5
                    run()
                if LEVEL3.check_for_input(menu_mouse_pos):
                    settings.health_counter = 5
                    settings.current_level = 3
                    settings.projectile_counter = 5
                    run()
                if BACK_BUTTON.check_for_input(menu_mouse_pos):
                    main_menu()

        pygame.display.update()

