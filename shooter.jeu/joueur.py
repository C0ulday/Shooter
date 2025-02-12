import pygame

class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.health = 100
        self.max_health = 100
        self.points = 0

        