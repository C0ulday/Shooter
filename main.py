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
jeu = Jeu()
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
   
    # Vérification du tir avec clic de la souris
    if pygame.mouse.get_pressed()[0]:  # Vérifie si le bouton gauche de la souris est cliqué
        if jeu.viseur.sprites()[0].detecteur_tir(jeu.aigles):
            score += 50  # Ajoute 50 points par tir réussi
            print(f"Score: {score}")

    # Affichage du score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
   
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
