import pygame

class Joueur(pygame.sprite.Sprite):
    def __init__(self,pseudo):
        super().__init__()

        self.health = 100
        self.max_health = 100
        self.score = 0
        self.pseudo = pseudo

    def setScore(self,points):
        self.score = self.score + points
    
    def getScore(self):
        return self.score