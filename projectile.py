import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self,x,y,velocity,image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.velocity = velocity
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
    
def launch_projectile(image_path):
