# Importing pygame, personal pycharm has it installed but when exporting the script,
# other machines might not.
import pygame

# default pygame setup
pygame.init()
# screen variables created early on making it easier to call later down the line and makes our code more malleable
# as we are no longer working with hard-coded numbers.
screenx, screeny = 1280, 720
screen = pygame.display.set_mode((screenx, screeny))
# changes the name of the window to the games title
pygame.display.set_caption('Element Z')
clock = pygame.time.Clock()
running = True

# testing surface
surf = pygame.Surface((100, 200))

# ensures that code stays running forever unless the user closes out of the window
while running:
    # poll for events
    # pygame.QUIT event means the user clicked x to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with colour to wipe away anything from last frame
    screen.fill("Gray")

    # render game here
    screen.blit(surf, (100, 150))
    # update() the display to put game on screen .flip works here as well
    pygame.display.update()

    clock.tick(60)  # limits fps to 60 makes a lot of stuff run smoother and simplifies some math

pygame.quit()
