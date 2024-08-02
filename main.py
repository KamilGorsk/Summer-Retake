# Importing pygame, personal pycharm has it installed but when exporting the script,
# other machines might not.
import pygame
from os.path import join
from random import randint
import time

# default pygame setup
pygame.init()
# screen variables created early on making it easier to call later down the line and makes our code more robust
# as we are no longer working with hard-coded numbers.
screenx, screeny = 1280, 720
screen = pygame.display.set_mode((screenx, screeny))
# changes the name of the window to the games title
pygame.display.set_caption('Element Z')
Clock = pygame.time.Clock()
running = True

# image loading - loads all images used for the game, using the join method we can find the desired image
# making the code more robust overall.
# if an image has no transparent pixels we want to call .convert otherwise .convert_alpha, increases fps, runs smoother

player_ship = pygame.image.load(join('images', 'player.png')).convert_alpha()
player_rect = player_ship.get_rect(center=(screenx / 2, screeny / 2))
# using vector math for movement as vectors are incredibly powerful
player_dir = pygame.math.Vector2(0, 0)
# pixels/frame
player_speed = 300

game_background = pygame.image.load(join('images', 'background.png')).convert()

star_background = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_loc = [(randint(0, screenx), randint(0, screeny)) for i in range(20)]

asteroid_main = pygame.image.load(join('images', 'asteroid.png')).convert_alpha()
asteroid_rect = asteroid_main.get_rect(center=(screenx / 2, screeny / 2))

projectile_main = pygame.image.load(join('images', 'projectile.png')).convert_alpha()
projectile_rect = projectile_main.get_rect(bottomleft=(20, screeny - 20))

# classes

# ensures that code stays running forever unless the user closes out of the window

while running:
    dt = Clock.tick(240) / 1000  # framerate independence using delta time method formula is direction * speed * dt
    # poll for events
    # pygame.QUIT event means the user clicked x to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # pygame.key / pygame.mouse are better for input than event loop as they make it easier to integrate with classes
    # also can check for continuous presses
    # input - storing return value inside a var for arrow keys + WASD movement using a boolean value
    keys = pygame.key.get_pressed()
    player_dir.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
    player_dir.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
    # normalizing movement, so it's consistent and stays at 300 whichever direction the player is going
    player_dir = player_dir.normalize() if player_dir else player_dir
    player_rect.center += player_dir * player_speed * dt

    # projectile firing
    recent_keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print('fire')
    # fill the screen with colour to wipe away anything from last frame
    screen.fill("Gray")

    # render game here
    screen.blit(game_background, (0, 0))
    for loc in star_loc:
        screen.blit(star_background, loc)
    screen.blit(projectile_main, projectile_rect)

    screen.blit(player_ship, player_rect)

    screen.blit(asteroid_main, asteroid_rect)
    # update() the display to put game on screen .flip works here as well
    pygame.display.update()

pygame.quit()
