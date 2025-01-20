import pygame
from zombie import Zombie
from joueur import Joueur

class Jeu:

    def __init__(self):

        # générer le joueur
        self.joueur = Joueur(self)
        # groupe de projectiles/zombies

        self.all_zombies = pygame.sprite.Group()
    
    def lancer_projectile(self,type):

        match type:
            case 1:
                le_zombie = Zombie()
                self.add_zombies.add(le_zombie)
            case 2:
                le_zombie = Zombie()
                self.add_zombies.add(le_zombie)
            case 3:
                le_zombie = Zombie()
                self.add_zombies.add(le_zombie)