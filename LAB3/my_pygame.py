# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
window_size = (500, 500)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Simple Pygame Program")

# Run until the user asks to quit
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the game logic (if any)

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    circle_center = (250, 250)
    circle_radius = 75
    pygame.draw.circle(screen, (0, 0, 255), circle_center, circle_radius)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
