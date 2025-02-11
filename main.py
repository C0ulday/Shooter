import math
import pygame
import random
from jeu import Jeu
pygame.init()

#### AFFICHAGE
pygame.display.set_caption("M-Shooter")

# Initialisation fenêtre de jeu classique
background = pygame.image.load("assets/environnement/back.png")
sol = pygame.image.load("assets/environnement/tiles.png")
font = pygame.font.Font("assets/font/BPdots.otf",16)
font.set_bold(True)

# Le jeu
jeu = Jeu()
score = 0  # Initialisation du score

######## Boucle de jeu
screen = pygame.display.set_mode((jeu.WIDTH,jeu.HEIGHT))

# Définition d'un événement pour le spawn de monstres
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 2000)  # un monstre toutes les 2 secondes


# Timer

clock = pygame.time.Clock()
temps = 3000 # 3s
fps = 60

running = True
while running :

    clock.tick(fps)
    screen.blit(background, (0,0))
    screen.blit(sol, (0,0))

    # Affichagfe des aigles
    jeu.aigles.draw(screen)
    jeu.aigles.update(True)

    # Affichage du viseur
    jeu.viseur.update()
    jeu.viseur.draw(screen)

    # Affichage du score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Affichage du chronomètre
    temps_text = font.render(f"temps: {temps} ms", True, (255, 255, 255))
    temps_rect = temps_text.get_rect(topright=(screen.get_width() - 10, 10))
    screen.blit(temps_text, temps_rect)
   
    pygame.display.flip()

    # Gestion du temps de jeu
    if temps <=0 :
        running = False

    temps -=1
    # Gestion des évènements du jeu
    for event in pygame.event.get():
        # Vérification du tir avec clic de la souris
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            if jeu.viseur.sprites()[0].detecteurTir(jeu.aigles):
                score += 50
                print(f"Score: {score}")

        # Affichage des aigles à différentes positions
        if event.type == SPAWN_EVENT:
            x = jeu.getWidth()
            y = random.randint(0, jeu.getHeight())
            if temps < 2500:
                jeu.spawnAigles(x,y,10)
            if temps < 1500:
                jeu.spawnAigles(x,y,10)
            else:
                jeu.spawnAigles(x,y,5)

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        print(temps)
    clock.tick(fps)
    
   
