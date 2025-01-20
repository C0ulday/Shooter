import math
import pygame
import viseur
pygame.init()




WIDTH = 1080
HEIGHT = 720
fps = 60

#### AFFICHAGE
pygame.display.set_caption("Z-Shooter")

# Background
background = pygame.image.load("assets/images/background.jpg")
running = True

timer = pygame.time.Clock()
font = pygame.font.Font("assets/font/BPdots.otf")

class Player:
    def __init__(self):
        self.max_health = 100
        self.health = 100
        self.score = 0



# Ajout du viseur
jouer_viseur = viseur.Viseur()
viseur_sprites = pygame.sprite.Group()
viseur_sprites.add(jouer_viseur)

screen = pygame.display.set_mode((WIDTH,HEIGHT))


while running :

    timer.tick(fps)
    screen.blit(background, (0,0))

    viseur_sprites.update()
    viseur_sprites.draw(screen)
    pygame.display.flip()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()