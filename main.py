# Import the pygame module.
import sys

import pygame

from classes.sprites import Player
from classes.screens import MainScreen, Screen
from classes.settings import Settings
import game_functions as gf


# Create settings for the game.
settings = Settings()

# Initialize pygame.
pygame.init()

# Create the screen object.
# The width and height are controlled by the SCREEN_WIDTH and SCREEN_HEIGHT constants.
screen = MainScreen((settings.width, settings.height))
game_screen = Screen((settings.width, settings.height - 100), settings)

# Create groups to hold all sprites and enemy sprites.
#   enemies is used for collision detection and position updates.
#   all_sprites is used for rendering.
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


# Main game loop.
def main_game():
    # Instantiate the player, which right now is just a rectangle.
    player = Player(settings)
    all_sprites.add(player)

    # Variable to keep the main game loop running.
    running = True

    # Setup a clock for a decent frame rate.
    clock = pygame.time.Clock()

    while running:
        # Look at every event in the queue:
        for event in pygame.event.get():
            gf.event_handler(event, settings, game_screen, all_sprites, enemies, clouds)

        # Get the pressed keys and check for input.
        pressed_keys = pygame.key.get_pressed()

        # Update group positions.
        enemies.update()
        clouds.update()

        # Update the player sprite based on user key presses.
        player.update(pressed_keys)

        # Fill the screen with black.
        game_screen.fill((135, 206, 205))
        game_screen.rect.bottom = settings.height
        screen.surface.fill((255, 255, 255))

        # Draw all sprites.
        for entity in all_sprites:
            game_screen.blit(entity.surf, entity.rect)

        gf.update_screen(settings, screen, game_screen, player)

        # Check if the enemies have collided with the player.
        if pygame.sprite.spritecollideany(player, enemies):
            # Check to see how many lives they have. If they have more lives, subtract one and reset the game.
            # Player has more lives, reset the game.
            if player.lives > 1:
                lives = player.lives
                player.kill()
                player = Player(settings , lives=(lives - 1))
                all_sprites.add(player)
                for enemy in enemies:
                    enemy.kill()
                if settings.score > settings.high_score:
                    settings.high_score = settings.score
                settings.score = 0
                settings.speed_multiplier = 1
            # Player has no more lives, kill the player and end the game.
            else:
                player.kill()
                running = False

        # Update the display.
        pygame.display.flip()

        # Ensure the program maintains a rate of 30 frames per second.
        clock.tick(30)


def end_game():
    end_screen = Screen((settings.width, settings.height), settings)
    end_screen.fill((255, 255, 255))
    screen.surface.blit(end_screen, end_screen.get_rect())

    for entity in all_sprites:
        entity.kill()

    # Insert High Score
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    high_score_text = myfont.render('High Score: ' + str(settings.high_score), False, (0, 0, 0))

    screen.surface.blit(high_score_text, (
    (settings.width - high_score_text.get_width()) / 2, (settings.height - high_score_text.get_height()) / 2))

    settings.score = 0
    settings.high_score = 0
    settings.speed_multiplier = 1

    end = True
    while end:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    end = False

        pygame.display.flip()


while True:
    main_game()
    end_game()