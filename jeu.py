import pygame
import projectile
from joueur import Joueur

class Jeu:

    def __init__(self):

        # générer le joueur
        self.joueur = Joueur(self)
    
    def lancer_projectile(self,):
        zomb