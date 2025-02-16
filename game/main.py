import math
import pygame
import random
from jeu import Jeu
from menu import *
pygame.init()



def menu():
    pygame.display.set_caption("Menu - M-Shooter")
    background = pygame.image.load("game/assets/environnement/back.png")



# Exemple d'exécution du jeu
if __name__ == "__main__":
    pygame.init()
    jeu = Jeu()
    jeu.jouer()
    #men = mainMenu(jeu)
    #men.blitMainMenu()
    pygame.quit()
