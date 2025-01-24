import pygame
import math
import random


class Aigle(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.points = 50
        self.droite = 1
        self.gauche  = 2
        self.vivant = True
        self.direction = random.randint(1, 2)
        self.vol_droit = False
        self.animation_count = 0

        self.vol_de_droite = [pygame.image.load("assets/ennemis/aigle/fly1.png"),
                              pygame.image.load("assets/ennemis/aigle/fly2.png"),
                              pygame.image.load("assets/ennemis/aigle/fly3.png"),
                              pygame.image.load("assets/ennemis/aigle/fly4.png")]
        self.vol_mort =       [pygame.image.load("assets/ennemis/aigle/hurt1.png"),
                              pygame.image.load("assets/ennemis/aigle/hurt2.png"),
                              pygame.image.load("assets/ennemis/aigle/hurt3.png"),
                              pygame.image.load("assets/ennemis/aigle/hurt4.png")]
        

        # définition de l'image actuelle et du rectangle de position
        self.image = self.vol_de_droite[0]
        self.rect = self.image.get_rect(center=(random.randint(100, 500), random.randint(100, 300)))

    def updateAnimation(self):
        self.animation_count += 1

        if self.vivant:
            # Animation en vol normal
            index = (self.animation_count // 5) % len(self.vol_de_droite)
            self.image = self.vol_de_droite[index]
        else:
            # Animation en état "mort"
            index = (self.animation_count // 5) % len(self.vol_mort)
            self.image = self.vol_mort[index]

    def update(self):
        """Met à jour la position et l'animation."""
        self.updateAnimation()
        
        # Déplacement horizontal en fonction de la direction
        if self.direction == self.droite:
            self.rect.x += 5
            if self.rect.right > 800:
                self.direction = self.gauche
        else:
            self.rect.x -= 5
            if self.rect.left < 0:
                self.direction = self.droite

        

