import pygame
from const import *


#
# Création de la cible
# Ici elle sera ronde et rouge


class Cible:
    def __init__(self, x, y, rayon):
        self.x = x
        self.y = y
        self.rayon = rayon
        self.vx = 5 # Vitesse sur l'axe x
        self.vy = 5 # Vitesse sur l'axe y

    # Pour dessiner la cible
    def draw(self, screen):
        pygame.draw.circle(screen, ROUGE, (self.x, self.y), self.rayon)
        
    
    def move(self):
        # On déplace la cible
        self.x += self.vx
        self.y += self.vy

        # On vérifie si la cible sort de l'écran
        if self.x < 0 or self.x > LARGEUR:
            self.vx = -self.vx
        if self.y < 0 or self.y > HAUTEUR:
            self.vy = -self.vy
    
    def collision(self, x, y):
        # On vérifie si la cible est touchée
        if (x - self.x) ** 2 + (y - self.y) ** 2 <= self.rayon ** 2:
            return True
        return False