from random import randint

import pygame
from pygame.sprite import Sprite
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)


class Player(Sprite):
    def __init__(self, settings, lives=3):
        super(Player, self).__init__()
        self.surf = pygame.image.load('jet.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.settings = settings
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
        if self.rect.right > self.settings.width:
            self.rect.right = self.settings.width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > self.settings.height:
            self.rect.bottom = self.settings.height


class Enemy(Sprite):
    def __init__(self, settings,  min=5, max=20):
        super(Enemy, self).__init__()
        self.settings = settings
        self.surf = pygame.image.load('missile.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                randint(self.settings.width + 20, self.settings.width + 100),
                randint(0, self.settings.height)
            )
        )
        if self.settings.speed_multiplier == 1:
            self.speed = randint(min, max) * self.settings.speed_multiplier
        else:
            self.speed = randint(min, max) * randint(1, self.settings.speed_multiplier)

    # Move the sprite based off its speed.
    # Remove the sprite when it passes the left edge of the screen.
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def increase_speeds(self, amount):
        self.speed += amount


class Cloud(Sprite):
    def __init__(self, settings):
        super(Cloud, self).__init__()
        self.settings = settings
        self.surf = pygame.image.load('cloud.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                randint(self.settings.width + 20, self.settings.width + 100),
                randint(0, self.settings.height)
            )
        )

    # Move the cloud based on a constant speed.
    # Remove the cloud when it leaves the edge of the screen.
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()