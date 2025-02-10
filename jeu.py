import pygame
from monstre import *
from joueur import Joueur
from viseur import Viseur


class Jeu:

    def __init__(self,xlimit=None,ylimit=None):
        self.WIDTH = 1000
        self.HEIGHT = 472
        self.fps = 60
        self.xlimit = xlimit
        self.ylimit = ylimit
        
        # Le monstre 
        self.aigles = pygame.sprite.Group()
        self.spawnAigle()

        # le viseur
        self.viseur = pygame.sprite.Group()
        self.ajouter_viseur()

        # groupe de projectiles/zombies
        #self.all_zombies_sprites = pygame.sprite.Group()
        #self.lancer_zombie()

    def spawnAigle(self):
        aigle = Aigle(self,self.xlimit,self.ylimit)
        self.aigles.add(aigle)

    def ajouter_viseur(self):
        viseur = Viseur()
        self.viseur.add(viseur)
    
    #def lancer_zombie(self):

        #self.all_zombies_sprites.add(Zombie_Facile(500,600))
        #self.all_zombies_sprites.add(Zombie_Moyen(600,700))
        #self.all_zombies_sprites.add(Zombie_Difficile(700,800))
        #self.all_zombies_sprites.add(Zombie_Extreme(900,100))
        #self.all_zombies_sprites.add(Zombie_Perte(400,600))
    
