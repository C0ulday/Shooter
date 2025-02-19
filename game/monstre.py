import pygame
import random

class Monstre(pygame.sprite.Sprite):
    def __init__(self, monster_type, x, y, speed):
        """
        monster_type: chaîne de caractères indiquant le type de monstre ("aigle" ou "frog")
        x, y: position initiale
        speed: vitesse du monstre
        """
        super().__init__()
        
        self.monster_type = monster_type
        self.vivant = True
        self.animation_count = 0
        self.speed = speed
        self.images = []
        self.death_images = []
        
        # Définition de la direction et des points selon le type
        if monster_type == "aigle":
            self.direction = -1
            # Chargement des images en fonction du type de monstre
            # Images d'animation de vol
            for i in range(1, 5):
                image_path = f"game/assets/mode1/sprites/aigle/fly{i}.png"
                self.images.append(pygame.image.load(image_path))
                
        elif monster_type == "frog":
            self.direction = 1
            # Images d'animation de saut (pour la grenouille)
            for i in range(1, 7):
                image_path = f"game/assets/mode1/sprites/frog/jump{i}.png"
                self.images.append(pygame.image.load(image_path))
        # Gator
        elif monster_type == "gator":
            self.tir =0
            self.direction = -1
            for i in range(1, 5):
                image_path = f"game/assets/mode1/sprites/gator/gator{i}.png"
                self.images.append(pygame.image.load(image_path))

        # Images d'animation de mort (utilisation des mêmes images de mort)
        for i in range(1, 7):
            image_path = f"game/assets/mode1/sprites/death/death{i}.png"
            self.death_images.append(pygame.image.load(image_path))
            
        # Initialisation de l'image et du rectangle de position
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = self.image.get_height()
        
    def updateAnimation(self):
        
        self.animation_count += 1

        if self.vivant:
            # Animation normale (bouclée)
            index = (self.animation_count // 5) % len(self.images)
            self.image = self.images[index]
        else:
            # Animation de mort (non bouclée)
            index = self.animation_count // 5
            if index < len(self.death_images):
                self.image = self.death_images[index]
            else:
                self.image = self.death_images[-1]
                self.kill()

            # Mouvements (appliqués dans tous les cas)
            if self.monster_type == "aigle":
                self.rect.y += self.speed
            elif self.monster_type == "frog":
                self.rect.x += self.speed
            elif self.monster_type == "gator":
                self.rect.x += self.speed

    def getHeight(self):
        return self.height

    def update(self, largeur,*args):
        """
        La méthode update adapte le comportement suivant le type de monstre.
        Pour l'aigle, un paramètre booléen (par exemple isVolDroit) peut être passé.
        Pour la grenouille, aucun paramètre supplémentaire n'est nécessaire.
        """
        if self.monster_type == "aigle" or self.monster_type == "gator":
            # Pour l'aigle, on attend éventuellement un booléen indiquant la direction du vol
            isVolDroit = args[0] if args else True
            self.updateAnimation()
            if isVolDroit:
                self.rect.x += self.direction * self.speed
            else:
                self.rect.x -= self.speed
                self.rect.y += random.randint(10, 20)
            # Suppression si le monstre sort de l'écran (par exemple vers le haut)
            if self.rect.right <= 0 or self.rect.left >= largeur:
                self.kill()
                
        elif self.monster_type == "frog":
            self.updateAnimation()
            self.rect.x += self.direction * self.speed
            # Suppression si le monstre sort de l'écran (par exemple vers la droite)
            if self.rect.x > largeur:
                self.kill()
                
  
    