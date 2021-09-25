import sys

import pygame
pygame.init()

from classes.sprites import Player, Enemy, Cloud

# Import pygame.locals for easier access to key coordinates.
# Updated to conform to flak8 standards.
from pygame.locals import (
	K_ESCAPE,
	KEYDOWN,
	QUIT
)

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
ADDSCORE = pygame.USEREVENT + 3
pygame.time.set_timer(ADDSCORE, 1000)
SPEEDGAME = pygame.USEREVENT + 4
pygame.time.set_timer(SPEEDGAME, 5000)


def update_screen(settings, screen, game_screen, player):
	# Initialize the font used in game.
	myfont = pygame.font.SysFont('Comic Sans MS', 30)
	# Create a scoring system.
	textscore = myfont.render('Score: ' + str(settings.score), False, (0, 0, 0))
	textscore_rect = textscore.get_rect()
	# Create a high score label.
	text_high_score = myfont.render('High Score: ' + str(settings.high_score), False, (0, 0, 0))
	# Create a lives label.
	textlives = myfont.render('Lives: ' + str(player.lives), False, (0, 0, 0))
	textlives_rect = textlives.get_rect()
	textlives_rect.right = screen.rect.right

	screen.surface.blit(game_screen, game_screen.rect)
	screen.surface.blit(textscore, (
		(screen.rect.width - textscore.get_width()) / 2, (screen.rect.height - game_screen.height) / 2))
	screen.surface.blit(textlives, (textlives_rect.left, (screen.rect.height - game_screen.height) / 2))
	screen.surface.blit(text_high_score, ((screen.rect.width - text_high_score.get_width()) / 2, textscore_rect.bottom - 1))


def event_handler(event, settings, game_screen, all_sprites, enemies, clouds):
	# Check for a KEYDOWN event.
	if event.type == KEYDOWN:
		# If the scape key is pressed, exit the main loop.
		if event.key == K_ESCAPE:
			sys.exit()

	# Check for a QUIT event, quit the main loop.
	elif event.type == QUIT:
		sys.exit()

	# Add a new enemy.
	if event.type == ADDENEMY:
		# Create a new enemy and add it to the sprite groups.
		new_enemy = Enemy(settings)
		enemies.add(new_enemy)
		all_sprites.add(new_enemy)

	# Add clouds.
	if event.type == ADDCLOUD:
		# Create a new cloud and add it to the sprite group.
		new_cloud = Cloud(game_screen)
		clouds.add(new_cloud)
		all_sprites.add(new_cloud)

	if event.type == ADDSCORE:
		settings.score += 1

	if event.type == SPEEDGAME:
		settings.speed_multiplier += 1
