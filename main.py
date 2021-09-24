# Import the pygame module.
import pygame

# Import random for random numbers.
import random
import decimal

# Import pygame.locals for easier access to key coordinates.
# Updated to conform to flak8 standards.
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

# Define the constants for the screen width and height.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_SCREEN_WIDTH = 800
GAME_SCREEN_HEIGHT = 500

# Define a Player object by extending pygame.sprite.Sprite.
# The surface drawn on the screen is now an attribute of 'player'.
class Player(pygame.sprite.Sprite):
    def __init__(self, lives=3):
        super(Player, self).__init__()
        self.surf = pygame.image.load('jet.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.lives = lives

    # Move the player based on set of pressed keys.
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep the player on the screen.
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > GAME_SCREEN_WIDTH:
            self.rect.right = GAME_SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > GAME_SCREEN_HEIGHT:
            self.rect.bottom = GAME_SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, min=5, max=20):
        super(Enemy, self).__init__()
        #self.surf = pygame.Surface((20, 10))
        self.surf = pygame.image.load('missile.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(GAME_SCREEN_WIDTH + 20, GAME_SCREEN_WIDTH + 100),
                random.randint(0, GAME_SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(min, max)

    # Move the sprite based off its speed.
    # Remove the sprite when it passes the left edge of the screen.
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load('cloud.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(GAME_SCREEN_WIDTH + 20, GAME_SCREEN_WIDTH + 100),
                random.randint(0, GAME_SCREEN_HEIGHT)
            )
        )

    # Move the cloud based on a constant speed.
    # Remove the cloud when it leaves the edge of the screen.
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

class Screen(pygame.surface.Surface):
    def __init__(self, size):
        super(Screen, self).__init__(size)
        self.size = size
        self.rect = self.get_rect()

# Initialize pygame.
pygame.init()

# Create the screen object.
# The width and height are controlled by the SCREEN_WIDTH and SCREEN_HEIGHT constants.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
game_screen = Screen((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
ADDSCORE = pygame.USEREVENT + 3
pygame.time.set_timer(ADDSCORE, 1000)
SPEEDGAME = pygame.USEREVENT + 4
pygame.time.set_timer(SPEEDGAME, 5000)

# Instantiate the player, which right now is just a rectangle.
player = Player()

# Create groups to hold all sprites and enemy sprites.
#   enemies is used for collision detection and position updates.
#   all_sprites is used for rendering.
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main game loop running.
running = True
score = 0
speed = 30
min = 5
max = 20

# Setup a clock for a decent frame rate.
clock = pygame.time.Clock()

# Main game loop.
while running:
    # Look at every event in the queue:
    for event in pygame.event.get():
        # Check for a KEYDOWN event.
        if event.type == KEYDOWN:
            # If the scape key is pressed, exit the main loop.
            if event.key == K_ESCAPE:
                running = False

        # Check for a QUIT event, quit the main loop.
        elif event.type == QUIT:
            running = False

        # Add a new enemy.
        if event.type == ADDENEMY:
            # Create a new enemy and add it to the sprite groups.
            new_enemy = Enemy(min=min, max=max)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Add clouds.
        if event.type == ADDCLOUD:
            # Create a new cloud and add it to the sprite group.
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        if event.type == ADDSCORE:
            score += 1

        if event.type == SPEEDGAME:
            min += 5
            max += 5


    # Get the pressed keys and check for input.
    pressed_keys = pygame.key.get_pressed()

    # Update group positions.
    enemies.update()
    clouds.update()

    # Update the player sprite based on user key presses.
    player.update(pressed_keys)

    # Fill the screen with black.
    game_screen.fill((135, 206, 205))
    game_screen.rect.bottom = SCREEN_HEIGHT
    screen.fill((255, 255, 255))

    # Draw all sprites.
    for entity in all_sprites:
        game_screen.blit(entity.surf, entity.rect)

    # Initialize the font used in game.
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    # Create a scoring system.
    textscore = myfont.render('Score: ' + str(score), False, (0, 0, 0))
    # Create a lives label.
    textlives = myfont.render('Lives: ' + str(player.lives), False, (0, 0, 0))
    textlives_rect = textlives.get_rect()
    textlives_rect.right = screen_rect.right

    screen.blit(game_screen, game_screen.rect)
    screen.blit(textscore, ((SCREEN_WIDTH - textscore.get_width()) / 2, (SCREEN_HEIGHT - GAME_SCREEN_HEIGHT) / 2))
    screen.blit(textlives, (textlives_rect.left, (SCREEN_HEIGHT - GAME_SCREEN_HEIGHT) / 2))

    # Check if the enemies have collided with the player.
    if pygame.sprite.spritecollideany(player, enemies):
        # Check to see how many lives they have. If they have more lives, subtract one and reset the game.
        # Player has more lives, reset the game.
        if player.lives > 1:
            lives = player.lives
            player.kill()
            player = Player(lives=(lives - 1))
            all_sprites.add(player)
            for enemy in enemies:
                enemy.kill()
            score = 0
            min = 5
            max = 20
        # Player has no more lives, kill the player and end the game.
        else:
            player.kill()
            running = False

    # Update the display.
    pygame.display.flip()

    # Ensure the program maintains a rate of 30 frames per second.
    clock.tick(30)
