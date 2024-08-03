# Importing pygame, personal pycharm has it installed but when exporting the script,
# other machines might not.
from os.path import join
from random import randint

import pygame


# sprites and classes
# player class, already re-sized the asset in a separate program, I will not be needing a transform.scale
# using vector math for movement as vectors are incredibly powerful, dir short for direction.
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_rect(center=(screenx / 2, screeny / 2))
        self.speed = 300
        self.dir = pygame.math.Vector2()

    # pygame.key / pygame.mouse are better for input than event loop as they make it easier to integrate with classes
    # also can check for continuous presses
    # input - storing return value inside a var for arrow keys + WASD movement using a boolean value
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.dir.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.dir.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        # normalizing movement, so it's consistent and stays at 300 whichever direction the player is going
        self.dir = self.dir.normalize() if self.dir else self.dir
        self.rect.center += self.dir * self.speed * dt

        # projectile firing
        recent_keys = pygame.key.get_pressed()
        if recent_keys[pygame.K_SPACE]:
            print('fire')

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
# if an image has no transparent pixels we want to use .convert otherwise .convert_alpha, increases fps, runs smoother
# creating a group for all sprites for better optimization
all_sprites = pygame.sprite.Group()
player = Player(all_sprites)

game_background = pygame.image.load(join('images', 'background.png')).convert()

star_background = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_loc = [(randint(0, screenx), randint(0, screeny)) for i in range(20)]

asteroid_main = pygame.image.load(join('images', 'asteroid.png')).convert_alpha()
asteroid_rect = asteroid_main.get_rect(center=(screenx / 2, screeny / 2))

projectile_main = pygame.image.load(join('images', 'projectile.png')).convert_alpha()
projectile_rect = projectile_main.get_rect(bottomleft=(20, screeny - 20))

# ensures that code stays running forever unless the user closes out of the window

while running:
    dt = Clock.tick(240) / 1000  # framerate independence using delta time method formula is direction * speed * dt
    # poll for events
    # pygame.QUIT event means the user clicked x to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # calls an update method on all the sprites inside the group, passing delta time through it
    all_sprites.update(dt)

    # fill the screen with colour to wipe away anything from last frame
    screen.fill("Gray")

    # render game here
    screen.blit(game_background, (0, 0))
    for loc in star_loc:
        screen.blit(star_background, loc)

    screen.blit(projectile_main, projectile_rect)
    screen.blit(asteroid_main, asteroid_rect)
    # draws every image in the group
    all_sprites.draw(screen)

    # update() the display to put game on screen .flip works here as well
    pygame.display.update()

pygame.quit()
