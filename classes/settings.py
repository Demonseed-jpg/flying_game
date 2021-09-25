import pygame.display


class Settings:
	def __init__(self, width=1920, height=1080):
		self.width = width
		self.height = height

		# Game Settings
		self.score = 0
		self.high_score = 0

		# Enemy Settings
		self.speed_multiplier = 1
