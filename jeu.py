import pygame
from zombie import *
from joueur import Joueur
from viseur import Viseur


class Jeu:

    def __init__(self):

        # générer le joueur
        self.joueur = Joueur()

        # groupe de projectiles/zombies
        self.all_zombies_sprites = pygame.sprite.Group()
        self.lancer_zombie()

        # le viseur
        self.viseur_sprites = pygame.sprite.Group()
        self.ajouter_viseur()


    def ajouter_viseur(self):

        # Ajout du viseur
        le_viseur = Viseur()
        self.viseur_sprites.add(le_viseur)



    def lancer_zombie(self):

        self.all_zombies_sprites.add(Zombie_Facile(500,600))
        self.all_zombies_sprites.add(Zombie_Moyen(600,700))
        self.all_zombies_sprites.add(Zombie_Difficile(700,800))
        self.all_zombies_sprites.add(Zombie_Facile(900,100))
        self.all_zombies_sprites.add(Zombie_Extreme(400,600))
    