import pygame
import math
import random

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, point, velocity, image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.velocity = velocity
        self.point = point
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)  # Positionnement initial

    def move(self, type):
        pass  

class Zombie_Facile(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, point=10, velocity=3, image_path="assets/images/zombie1.png")

class Zombie_Moyen(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, point=20, velocity=6, image_path="assets/images/zombie2.png")

class Zombie_Difficile(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, point=30, velocity=8, image_path="assets/images/zombie1.png")

class Zombie_Extreme(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, point=40, velocity=11, image_path="assets/images/zombie2.png")

class Zombie_Perte(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, point=-100, velocity=11, image_path="assets/images/zombie3.png")
