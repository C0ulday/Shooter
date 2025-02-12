import math
import pygame
import random
from jeu import Jeu
pygame.init()



def menu():
    pygame.display.set_caption("Menu - M-Shooter")
    background = pygame.image.load("shooter.jeu/assets/environnement/back.png")



if __name__ == "__main__":
    game = Jeu()
    game.jouer()