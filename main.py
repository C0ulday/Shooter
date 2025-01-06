import math
import pygame
pygame.init()




WIDTH = 1080
HEIGHT = 720
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font("assets/font/BPdots.otf")

class Player:
    def __init__(self):
        self.max_health = 100
        self.health = 100
        self.score = 0


#### AFFICHAGE
pygame.display.set_caption("Z-Shooter")
screen = pygame.display.set_mode((WIDTH,HEIGHT))


# Background
background = pygame.image.load("assets/background.jpg")
running = True

# Projectiles

zombie1 = Projectile("assets/zomboe1.png")
while running :

    screen.blit(background, (0,0))
    pygame.display.flip()

    screen.blit(game.zombie1, game.zombie1.rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()