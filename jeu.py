import pygame
from monstre import *
from joueur import Joueur
from viseur import Viseur


class Jeu:

    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 472
        
        # le viseur
        self.viseur = pygame.sprite.Group()
        self.ajouterViseur()

        # L'ensemble des monstres aigles
        self.aigles = pygame.sprite.Group()

    #getters pour jeu

    def getHeight(self):
        return self.HEIGHT
    
    def getWidth(self):
        return self.WIDTH

    def ajouterViseur(self):
        viseur = Viseur()
        self.viseur.add(viseur)

    # Lancer les monstres

    def spawnAigles(self,x,y,speed):
        aigle = Aigle(x,y,speed)
        h = aigle.getAigleHeight() # utilisé pour obtenir la hauteur de l'image de l'aigle
        aigle = Aigle(x,y - h,speed) # la soustraction permet de faire spawn l'aigle en entier sur l'écran 
        # à chaque fois et non une seule partie
        self.aigles.add(aigle)

