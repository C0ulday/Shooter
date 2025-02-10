import math
import pygame
from jeu import Jeu
pygame.init()




WIDTH = 1000
HEIGHT = 472
fps = 60

#### AFFICHAGE
pygame.display.set_caption("M-Shooter")

# Background
background = pygame.image.load("assets/environnement/back.png")
sol = pygame.image.load("assets/environnement/tiles.png")

running = True

timer = pygame.time.Clock()
font = pygame.font.Font("assets/font/BPdots.otf")

class Player:
    def __init__(self):
        self.max_health = 100
        self.health = 100
        self.score = 0

# Le jeu

jeu = Jeu()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

while running :

    timer.tick(fps)
    screen.blit(background, (0,0))
    screen.blit(sol, (0,0))
   
    #jeu.all_zombies_sprites.draw(screen)
    #jeu.all_zombies_sprites.update(WIDTH,HEIGHT)

    jeu.viseur.update()
    jeu.viseur.draw(screen)

    jeu.aigles.draw(screen)
    jeu.aigles.update()
   
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()