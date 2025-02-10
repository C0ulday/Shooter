import pygame
import math
import random


class Aigle(pygame.sprite.Sprite):

    def __init__(self, jeu, xlimit=None, ylimit=None):
        super().__init__()
        self.jeu = jeu
        self.points = 50
        self.vivant = True
        self.vol_droit = True
        self.animation_count = 0
        self.speed = 5
        self.direction = -1
        self.xlimit = xlimit
        self.ylimit = ylimit
        if (not xlimit):
            self.xlimit = jeu.WIDTH
        if (not ylimit):
            self.ylimit = jeu.HEIGHT

        self.vol = [pygame.image.load("assets/ennemis/aigle/fly1.png"),
                              pygame.image.load("assets/ennemis/aigle/fly2.png"),
                              pygame.image.load("assets/ennemis/aigle/fly3.png"),
                              pygame.image.load("assets/ennemis/aigle/fly4.png")] # il faut enlever fly3.png pour bien détecter l'image
        

        self.vol_mort =       [pygame.image.load("assets/ennemis/aigle/hurt1.png"),
                              pygame.image.load("assets/ennemis/aigle/hurt2.png"),
                              pygame.image.load("assets/ennemis/aigle/hurt3.png"),
                              pygame.image.load("assets/ennemis/aigle/hurt4.png")]
        
        # définition de l'image actuelle et du rectangle de position
        self.image = self.vol[0]
        self.rect = self.image.get_rect(center=(500, 236))
        print(self.rect.x)
        

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

    def update(self):
        # Met à jour la position et l'animation
        self.updateAnimation()
        #print(self.rect.x)
        # déplacement horizontal
        if self.vol_droit:
            self.rect.x += self.direction*self.speed
        elif not self.vol_droit:
            self.rect.x -= self.speed
            self.rect.y += random.randint(10,20)
             
        # détruit le sprite si sort de la fenêtre
        if self.vivant :
            if (self.rect.centerx < 1000-self.xlimit) or (self.rect.centerx > self.xlimit): 
                self.changeDirection() 

        if (self.rect.centery > self.ylimit):
            self.kill()

    def setSpeed(self,speed):
        self.speed = speed

    def setVolAleatoire(self):
        self.vol_droit = False

class Dog(pygame.sprite.Sprite):
     ""