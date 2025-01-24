import pygame
from zombie import *
from monstre import *
from joueur import Joueur
from viseur import Viseur


class Jeu:

    def __init__(self):

        # Ajout du premier monstre

        # générer le joueur
        #self.joueur = Joueur()
        self.aigles_sprites = pygame.sprite.Group()

        # le viseur
        #self.viseur_sprites = pygame.sprite.Group()
        #self.ajouter_viseur()

         # groupe de projectiles/zombies
        #self.all_zombies_sprites = pygame.sprite.Group()
        #self.lancer_zombie()

    def spawnAigle(self):
        aigle = Aigle()
        self.aigles_sprites.add(aigle)
    #def ajouter_viseur(self):

        # Ajout du viseur
        #le_viseur = Viseur()
        #self.viseur_sprites.add(le_viseur)



    #def lancer_zombie(self):

        #self.all_zombies_sprites.add(Zombie_Facile(500,600))
        #self.all_zombies_sprites.add(Zombie_Moyen(600,700))
        #self.all_zombies_sprites.add(Zombie_Difficile(700,800))
        #self.all_zombies_sprites.add(Zombie_Extreme(900,100))
        #self.all_zombies_sprites.add(Zombie_Perte(400,600))
    
