import math
import pygame
import random
from jeu import Jeu
pygame.init()



def menu():
    pygame.display.set_caption("Menu - M-Shooter")
    background = pygame.image.load("shooter.jeu/assets/environnement/back.png")



# Exemple d'exécution du jeu
if __name__ == "__main__":
    pygame.init()
    jeu = Jeu()
    #jeu.jouer()
    jeu.menu()
    pygame.quit()
