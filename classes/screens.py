import pygame
from pygame.surface import Surface
from classes.settings import Settings


class MainScreen(Surface):
    def __init__(self, size):
        super(MainScreen, self).__init__(size)
        self.surface = pygame.display.set_mode(size)
        self.rect = self.get_rect()


class Screen(Surface):
    def __init__(self, size, settings):
        super(Screen, self).__init__(size)
        self.size = size
        self.rect = self.get_rect()
        self.width = settings.width
        self.height = settings.height

