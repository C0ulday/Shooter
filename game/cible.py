import pygame

class Cible(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        
        self.image = image