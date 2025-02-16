import math
import pygame
import random
<<<<<<< HEAD
from jeu import Jeu
from menu import *
=======
from game.jeu import Jeu
>>>>>>> 21c25a0a24c2cc29bee30c41d641ce69a698ec1e
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
