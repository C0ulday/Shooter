import math
import pygame
import random
from game.jeu import Jeu
from game.menu import *

pygame.init()

def menu():
    pygame.display.set_caption("Menu - M-Shooter")
    #background = pygame.image.load("game/assets/environnement/back.png")

# Exemple d'exécution du jeu
if __name__ == "__main__":
    pygame.init()
    jeu = Jeu()
    menu = Menu(jeu)
    menu.launchMenu()
    pygame.quit()
