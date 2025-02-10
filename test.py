import math
import pygame
from jeu import Jeu
pygame.init()

#### AFFICHAGE
pygame.display.set_caption("M-Shooter")

# Background
background = pygame.image.load("assets/environnement/back.png")
sol = pygame.image.load("assets/environnement/tiles.png")

running = True

timer = pygame.time.Clock()
font = pygame.font.Font("assets/font/BPdots.otf")

# Le jeu
jeu = Jeu(160+500)
score = 0  # Initialisation du score

screen = pygame.display.set_mode((jeu.WIDTH,jeu.HEIGHT))

while running :

    timer.tick(jeu.fps)
    screen.blit(background, (0,0))
    screen.blit(sol, (0,0))
   
    jeu.viseur.update()
    jeu.viseur.draw(screen)

    jeu.aigles.draw(screen)
    jeu.aigles.update()
   

    # Affichage du score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
   
    pygame.display.flip()

    if (len(jeu.aigles) == 0):
        jeu.spawnAigle()

    for event in pygame.event.get():
        # Vérification du tir avec clic de la souris
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            if jeu.viseur.sprites()[0].detecteur_tir(jeu.aigles):
                score += 1  # Ajoute 50 points par tir réussi
                print(f"Score: {score}")

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
