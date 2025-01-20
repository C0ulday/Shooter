import pygame
import math
import random

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, point, velocity, image_path):
        super().__init__()


        self.x = x
        self.y = y
        self.velocity = velocity
        self.point = point
        self.image = pygame.image.load(image_path)
        
        self.image = pygame.transform.smoothscale(self.image, (90, 90))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)  # positionnement initial

        # vitesse initiale aléatoire
        self.velocity_x = random.uniform(-10, 10)
        self.velocity_y = random.uniform(-15, -5)

        # gravité et amortissement (perte d'énergie)
        self.gravity = 0.5
        self.bounce_factor = 0.8
        self.rotation_angle = 0  # angle de rotation actuel
        self.rotation_speed = random.uniform(5, 10)


    def update(self,WIDTH,HEIGHT):
        # Appliquer la gravité sur l'axe Y
        self.velocity_y += self.gravity

        # Mettre à jour la position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Gestion des rebonds sur les bords de la fenêtre
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.velocity_x = -self.velocity_x * self.bounce_factor
            self.rotation_speed = -self.rotation_speed  # Inverser la rotation

        if self.rect.bottom >= HEIGHT:
            self.velocity_y = -self.velocity_y * self.bounce_factor  # Rebond
            self.rect.bottom = HEIGHT  # Éviter qu'il sorte de l'écran

            # Appliquer un amortissement pour réduire l'énergie du rebond
            #if abs(self.velocity_y) < 1:
                #self.velocity_y = 0  # Arrêter le rebond s'il est trop faible
                #self.velocity_x *= 0.95  # Réduire la vitesse horizontale

        # faire tourner l'image en fonction de la vitesse
        self.rotation_angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, type):
        pass  

class Zombie_Facile(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, point=10, velocity=3, image_path="assets/images/zombie1.png")

class Zombie_Moyen(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, point=20, velocity=6, image_path="assets/images/zombie2.png")

class Zombie_Difficile(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, point=30, velocity=8, image_path="assets/images/zombie1.png")

class Zombie_Extreme(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, point=40, velocity=11, image_path="assets/images/zombie2.png")

class Zombie_Perte(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y, point=-100, velocity=11, image_path="assets/images/zombie3.png")
