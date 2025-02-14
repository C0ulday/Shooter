import pygame
import math
import random
from jeu import *

class Aigle(pygame.sprite.Sprite):

    def __init__(self,x,y,speed):
        super().__init__()

        self.points = 100
        self.vivant = True
        self.animation_count = 0
        self.speed = speed
        self.direction = -1


        # Définition des images de l'aigle
        self.vol = []
        self.vol_mort = []

        for i in range(1,5):
            image = f"shooter.jeu/assets/mode1/sprites/aigle/fly{i}.png"
            self.vol.append(pygame.image.load(image))
        
        for i in range(1,7):
            image = f"shooter.jeu/assets/mode1/sprites/death/death{i}.png"
            self.vol_mort.append(pygame.image.load(image))

        # définition de l'image actuelle et du rectangle de position

        self.image = self.vol[0]
        self.rect = self.image.get_rect()

    
        self.rect.x = x
        self.rect.y = y

        self.height = self.image.get_height()

    def getAigleHeight(self):
        return self.height
    
    def updateAnimation(self):
        self.animation_count += 1
        

        if self.vivant:
            # Animation en vol normal
            index = (self.animation_count // 5) % len(self.vol)
            self.image = self.vol[index]
        else:
            # Animation en état "mort" qui se joue une seule fois
            index = (self.animation_count // 5) % len(self.vol_mort)
            if self.image == self.vol_mort[len(self.vol_mort) - 1]:
                self.kill()
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

class Frog(pygame.sprite.Sprite):
    def __init__(self,x,y,speed):
        super().__init__()

        self.points = 80
        self.vivant = True
        self.animation_count = 0
        self.speed = speed
        self.direction = 1


        # Définition des images de l'aigle
        self.walk = []
        self.walk_mort = []
        self.tentation = []

        for i in range(1,7):
            image = f"shooter.jeu/assets/mode1/sprites/frog/jump{i}.png"
            self.walk.append(pygame.image.load(image))
        
        for i in range(1,7):
            image = f"shooter.jeu/assets/mode1/sprites/death/death{i}.png"
            self.walk_mort.append(pygame.image.load(image))

        # définition de l'image actuelle et du rectangle de position

        self.image = self.walk[0]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.height = self.image.get_height()

    def updateAnimation(self):
        self.animation_count += 1

        if self.vivant:
            # Animation en vol normal
            index = (self.animation_count // 5) % len(self.walk)
            self.image = self.walk[index]
        else:
            # Animation en état "mort"
            index = (self.animation_count // 5) % len(self.walk_mort)
            self.image = self.walk_mort[index]
            self.rect.x += self.speed
            if (self.image == self.walk_mort[5]):
                self.kill()

    def update(self):
        # Met à jour la position et l'animation
        self.updateAnimation()
        
        # déplacement horizontal
        self.rect.x += self.direction*self.speed

        # détruit le sprite si sort de la fenêtre
        if (self.rect.x > 1920):
            self.kill()

    def getFrogHeight(self):
        return self.height