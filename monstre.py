import pygame
import math
import random


class Aigle(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.points = 50
        self.vivant = True
        self.vol_droit = True
        self.animation_count = 0
        self.speed = 5

        self.vol = [pygame.image.load("assets/ennemis/aigle/fly1.png"),
                              pygame.image.load("assets/ennemis/aigle/fly2.png"),
                              pygame.image.load("assets/ennemis/aigle/fly3.png"),
                              pygame.image.load("assets/ennemis/aigle/fly4.png")]
        

        self.vol_mort =       [pygame.image.load("assets/ennemis/aigle/hurt1.png"),
                              pygame.image.load("assets/ennemis/aigle/hurt2.png"),
                              pygame.image.load("assets/ennemis/aigle/hurt3.png"),
                              pygame.image.load("assets/ennemis/aigle/hurt4.png")]
        
        # définition de l'image actuelle et du rectangle de position
        self.image = self.vol[0]
        self.rect = self.image.get_rect(center=(800, random.randint(100, 200)))

    def updateAnimation(self):
        self.animation_count += 1

        if self.vivant:
            # Animation en vol normal
            index = (self.animation_count // 5) % len(self.vol)
            self.image = self.vol[index]
        else:
            # Animation en état "mort"
            index = (self.animation_count // 5) % len(self.vol_mort)
            self.image = self.vol_mort[index]

    def update(self):

        """Met à jour la position et l'animation."""
        self.updateAnimation()
        if self.vol_droit:
            # déplacement horizontal
            self.rect.x -= self.speed
        elif not self.vol_droit:
            self.rect.x -= self.speed
            self.rect.y += random.randint(10,20)
             
        # détruit le sprite si sort de la fenêtre
        if self.rect.x < -20*self.speed: #facteur -20 pour que ce soit un peu plus fluide
            self.kill() 

    def setSpeed(self,speed):
        self.speed = speed

    def setVolAleatoire(self):
        self.vol_droit = False

class Dog(pygame.sprite.Sprite):
     ""