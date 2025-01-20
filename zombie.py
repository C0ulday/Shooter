import pygame


class Zombie(pygame.sprite.Sprite):

    def __init__(self,x,y,point,velocity,image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.velocity = velocity
        self.point = point
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
    
