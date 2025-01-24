import pygame
import math
import random


class Aigle(pygame.sprite.Sprite):

    def __init__(self):

        self.points = 50
        self.droite = 1
        self.gauche  = 2
        self.vivant = True
        self.direction = random.randint(1, 2)
        self.vol_droit = False
        self.animation_count = 0

        self.vol_de_droite = [pygame.image.load("assets/ennemis/aigle/fy1.png"),
                              pygame.image.load("assets/ennemis/aigle/fy2.png"),
                              pygame.image.load("assets/ennemis/aigle/fy3.png"),
                              pygame.image.load("assets/ennemis/aigle/fy4.png")]
        self.vol_mort =       [pygame.image.load("assets/ennemis/aigle/hurt1.png"),
                              pygame.image.load("assets/ennemis/aigle/hurt2.png"),
                              pygame.image.load("assets/ennemis/aigle/hurt3.png"),
                              pygame.image.load("assets/ennemis/aigle/hurt4.png")]
        
    
    def updateAnimation(self):

        

