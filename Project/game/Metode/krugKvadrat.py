import pygame

def circle_rect_collision(circle_x, circle_y, circle_r, rect_x, rect_y, rect_w, rect_h):
    closest_x = max(rect_x, min(circle_x, rect_x + rect_w))
    closest_y = max(rect_y, min(circle_y, rect_y + rect_h))
    dx = circle_x - closest_x
    dy = circle_y - closest_y
    if dx * dx + dy * dy < circle_r * circle_r:
        return True
    else:
        return False

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

circle_x = 180
circle_y = 180
circle_r = 50
rect_x = 200
rect_y = 200
rect_w = 200
rect_h = 200

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (255, 0, 0), (circle_x, circle_y), circle_r)
    pygame.draw.rect(screen, (0, 255, 0), (rect_x, rect_y, rect_w, rect_h))

    if circle_rect_collision(circle_x, circle_y, circle_r, rect_x, rect_y, rect_w, rect_h):

        #pygame.draw.circle(screen, (255, 0, 0), (circle_x, circle_y), circle_r, 2)
        #pygame.draw.rect(screen, (0, 255, 0), (rect_x, rect_y, rect_w, rect_h), 2)
        print("Collision")
    else:
        print("No collision")
    pygame.display.update()

pygame.quit()
