import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self,image_path):
        super().__init__()
        self.velocity = 5
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
    
def launch_projectile(image_path):

    projectile = Projectile(image_path) 