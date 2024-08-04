# Importing pygame, personal pycharm has it installed but when exporting the script,
# other machines might not.
from os.path import join
from random import randint, uniform

import pygame


# sprites and classes from session 9 - look at slides for help
# player class, already re-sized the asset in a separate program, I will not be needing a transform.scale for that
# using vector math for movement as vectors are incredibly powerful. -dir short for direction.
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_rect(center=(screenx / 2, screeny / 2))
        self.speed = 300  # speed value, default = 300
        self.dir = pygame.math.Vector2()

        # anti-spam system
        self.can_shoot = True
        self.projectile_shoot_time = 0
        # how fast player can shoot default = 500ms
        self.cooldown_duration = 500

    def projectile_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.projectile_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

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
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Projectile(projectile_main, self.rect.midtop, (all_sprites, projectile_sprites))
            self.can_shoot = False
            self.projectile_shoot_time = pygame.time.get_ticks()
            projectile_sound.play()
        self.projectile_timer()


class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=(randint(0, screenx), randint(0, screeny)))


class Projectile(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.dir = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(420, 520)
        self.rotation_speed = randint(52, 88)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.dir * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_rect(center=self.rect.center)


# use session 10 slides for animation cycle
class AsteroidAnimation(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()


def collisions():
    # making running a global variable, so I am able to call it here to shut down the game on collision without creating
    # a new variable. Not the best way to go around making a loss state however for a small pygame project like this
    # it seems good enough.
    # session 9 mask creation for pixel perfect collision
    global running

    collision_sprites = pygame.sprite.spritecollide(player, asteroid_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        running = False

    for projectile in projectile_sprites:
        collided_sprites = pygame.sprite.spritecollide(projectile, asteroid_sprites, True)
        if collided_sprites:
            projectile.kill()
            AsteroidAnimation(explosion_animation, projectile.rect.midtop, all_sprites)
            explosion_sound.play()


# function to display score called later down in code, boxes it in a rectangle
def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_score = font.render(str(current_time), True, 'white')
    text_rect = text_score.get_rect(midbottom=(screenx / 2, screeny - 50))
    screen.blit(text_score, text_rect)
    pygame.draw.rect(screen, (240, 240, 240), text_rect.inflate(30, 20), 5, 10)


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

# file/image loading - loads all images used for the game, using the join method we can find the desired image
# making the code more robust overall.
game_background = pygame.image.load(join('images', 'background.png')).convert()
asteroid_main = pygame.image.load(join('images', 'asteroid.png')).convert_alpha()
projectile_main = pygame.image.load(join('images', 'projectile.png')).convert_alpha()
star_image = pygame.image.load(join('images', 'star.png')).convert_alpha()
font = pygame.font.Font(join('images', 'blank space.otf'), 32)
explosion_animation = [pygame.image.load(join('images', 'asteroid_anim', f'{i}.png')).convert_alpha() for i in range(8)]

# sound imports
projectile_sound = pygame.mixer.Sound(join('sound', 'projectile.wav'))
projectile_sound.set_volume(0.08)
explosion_sound = pygame.mixer.Sound(join('sound', 'explosion.wav'))
explosion_sound.set_volume(0.22)
background_sound = pygame.mixer.Sound(join('sound', 'breakcore.wav'))
background_sound.set_volume(0.26)
background_sound.play(loops=-1)
# if an image has no transparent pixels we want to use .convert otherwise .convert_alpha, increases fps, runs smoother
# creating a group for all sprites for better optimization
# changed code to use a single import 20 times rather than creating 20 at once for better efficiency
all_sprites = pygame.sprite.Group()
asteroid_sprites = pygame.sprite.Group()
projectile_sprites = pygame.sprite.Group()

# amount of stars that get placed at random
for i in range(22):
    Star(all_sprites, star_image)
player = Player(all_sprites)

# custom events from session 9, interval timer
asteroid_event = pygame.event.custom_type()
pygame.time.set_timer(asteroid_event, 500)

# ensures that code stays running forever unless the user closes out of the window
while running:
    dt = Clock.tick(240) / 1000  # framerate independence using delta time method formula is direction * speed * dt
    # poll for events
    # pygame.QUIT event means the user clicked x to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == asteroid_event:
            x, y = randint(0, screenx), randint(-200, -100)
            Asteroid(asteroid_main, (x, y), (all_sprites, asteroid_sprites))
    # calls an update method on all the sprites inside the group, passing delta time through it
    all_sprites.update(dt)
    # collision setup
    collisions()

    # fill the screen with colour to wipe away anything from last frame
    screen.fill("Gray")

    # render game here
    screen.blit(game_background, (0, 0))

    # displays the score before every sprite therefore making it so that the player and asteroids will cover it
    display_score()
    # draws every image in the group
    all_sprites.draw(screen)

    # update() the display to put game on screen .flip works here as well
    pygame.display.update()

pygame.quit()
