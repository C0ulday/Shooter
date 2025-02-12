import pygame
import math
import random
from jeu import *

class Aigle(pygame.sprite.Sprite):

    def __init__(self,x,y,speed):
        super().__init__()

        self.points = 50
        self.vivant = True
        self.animation_count = 0
        self.speed = speed
        self.direction = -1

        self.vol = [pygame.image.load("shooter.jeu/assets/mode1/sprites/aigle/fly1.png"),
                              pygame.image.load("shooter.jeu/assets/mode1/sprites/aigle/fly2.png"),
                              pygame.image.load("shooter.jeu/assets/mode1/sprites/aigle/fly3.png"),
                              pygame.image.load("shooter.jeu/assets/mode1/sprites/aigle/fly4.png")] # il faut enlever fly3.png pour bien détecter l'image
        

        self.vol_mort =       [pygame.image.load("shooter.jeu/assets/mode1/sprites/aigle/hurt1.png"),
                              pygame.image.load("shooter.jeu/assets/mode1/sprites/aigle/hurt2.png"),
                              pygame.image.load("shooter.jeu/assets/mode1/sprites/aigle/hurt3.png"),
                              pygame.image.load("shooter.jeu/assets/mode1/sprites/aigle/hurt4.png")]
        
        # définition de l'image actuelle et du rectangle de position

        self.image = self.vol[0]
        self.rect = self.image.get_rect()

    
        self.rect.x = x
        self.rect.y = y

        self.height = self.image.get_height()

       
        

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
            self.rect.y += self.speed

    def changeDirection(self):
        if (self.direction == -1) :
            self.direction = 1 
        else : 
            self.direction = -1

    def update(self,isVolDroit):
        # Met à jour la position et l'animation
        self.updateAnimation()

        # déplacement horizontal
        if isVolDroit:
            self.rect.x += self.direction*self.speed
        elif not isVolDroit:
            self.rect.x -= self.speed
            self.rect.y += random.randint(10,20)

        # détruit le sprite si sort de la fenêtre
        if (self.rect.y < 0):
            self.kill()

    def getAigleHeight(self):
        return self.height
    
    def getPoints(self):
        return self.points


class Dog(pygame.sprite.Sprite):
     ""