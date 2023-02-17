import pygame
import math

# Initialize pygame window
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Initialize the state variables
x, y = 100, 100
vx, vy = 50, 50
dt = 0.01

# Run the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Implement RK4 method
    k1_x = vx * dt
    k1_y = vy * dt
    k2_x = (vx + k1_x / 2) * dt
    k2_y = (vy + k1_y / 2) * dt
    k3_x = (vx + k2_x / 2) * dt
    k3_y = (vy + k2_y / 2) * dt
    k4_x = (vx + k3_x) * dt
    k4_y = (vy + k3_y) * dt

    x += (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
    y += (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6

    # Draw the state
    pygame.draw.circle(screen, (0, 0, 255), (int(x), int(y)), 10)

    # Update the screen
    pygame.display.update()
    clock.tick(60)

# Quit pygame
pygame.quit()
