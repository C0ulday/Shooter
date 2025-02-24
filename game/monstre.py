import pygame
import random

class Monstre(pygame.sprite.Sprite):
    def __init__(self, monster_type, x, y, speed):
        super().__init__()
        
        self.monster_type = monster_type
        self.vivant = True
        self.animation_count = 0
        self.speed = speed
        self.images = []
        self.death_images = []
        self.has_died = False  # Nouveau drapeau pour suivre l'état de la mort
        
        if monster_type == "aigle":
            self.direction = -1
            for i in range(1, 5):
                image_path = f"game/assets/mode1/sprites/aigle/fly{i}.png"
                self.images.append(pygame.image.load(image_path))
        elif monster_type == "frog":
            self.direction = 1
            for i in range(1, 7):
                image_path = f"game/assets/mode1/sprites/frog/jump{i}.png"
                self.images.append(pygame.image.load(image_path))
        elif monster_type == "gator":
            self.tir = 0
            self.direction = -1
            for i in range(1, 5):
                image_path = f"game/assets/mode1/sprites/gator/gator{i}.png"
                self.images.append(pygame.image.load(image_path))

        for i in range(1, 7):
            image_path = f"game/assets/mode1/sprites/death/death{i}.png"
            self.death_images.append(pygame.image.load(image_path))
            
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = self.image.get_height()
        
    def updateAnimation(self):
        self.animation_count += 1

        if self.vivant:
            index = (self.animation_count // 5) % len(self.images)
            self.image = self.images[index]
        else:
            if not self.has_died:
                self.has_died = True
                self.animation_count = 0  # Réinitialiser pour commencer l'animation de mort
            index = self.animation_count // 5
            if index < len(self.death_images):
                self.image = self.death_images[index]
            else:
                self.image = self.death_images[-1]
                self.kill()

    def getHeight(self):
        return self.height

    def update(self, largeur, *args):
        if self.monster_type == "aigle" or self.monster_type == "gator":
            isVolDroit = args[0] if args else True
            self.updateAnimation()
            if self.vivant:  # Se déplacer uniquement si vivant
                if isVolDroit:
                    self.rect.x += self.direction * self.speed
                else:
                    self.rect.x -= self.speed
                    self.rect.y += random.randint(10, 20)
                if self.rect.right <= 0 or self.rect.left >= largeur:
                    self.kill()
        elif self.monster_type == "frog":
            self.updateAnimation()
            if self.vivant:  # Se déplacer uniquement si vivant
                self.rect.x += self.direction * self.speed
                if self.rect.x > largeur:
                    self.kill()