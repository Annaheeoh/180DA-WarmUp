import pygame
import random
from pygame.locals import (
    K_0, K_1, K_2, K_3,
    K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE,
    KEYDOWN, QUIT,
)

pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True
while running:
    com_val = random.randrange(0, 5)
    change = 0

    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key in [K_0, K_1, K_2, K_3]:
                user_in = int(event.unicode)
                change = 1
            elif event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    if change == 1:
        screen.fill((255, 255, 255))

        numFont = pygame.font.SysFont("Times New Roman", 90)
        textFont = pygame.font.SysFont("Times New Roman", 30)

        red = (255, 0, 0)
        green = (0, 255, 0)

        usertext = textFont.render("you inputted:", 1, red)
        comtext = textFont.render("the computer inputted:", 1, green)

        if user_in > com_val:
            resulttext = textFont.render("YOU WIN!!!:", 1, (122, 0, 122))
        else:
            resulttext = textFont.render("YOU LOSE!!!:", 1, (0, 122, 122))

        usernum = numFont.render(str(user_in), 1, red)
        comnum = numFont.render(str(com_val), 1, green)

        screen.blit(usertext, (50, 100))
        screen.blit(usernum, (50, 150))
        screen.blit(comtext, (400, 100))
        screen.blit(comnum, (400, 150))
        screen.blit(resulttext, (250, 300))

        pygame.display.flip()

# Done! Time to quit.
pygame.quit()
