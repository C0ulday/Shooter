import pygame
pygame.init()

import pygame

class Viseur(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load("game/assets/viseur/cross2.png")
        
        # Définir la taille de l'image du sprite
        self.rect = self.image.get_rect()
        
        # Position initiale du curseur
        self.rect.center = pygame.mouse.get_pos()
        
        # Variables pour le son et le comptage des tirs
        self.clicSouris = False
        self.total_shots = 0
        self.gunShotSound = pygame.mixer.Sound("game/assets/sounds/shot.wav")

    def update(self):
        # Obtenir la position actuelle de la souris
        self.rect.center = pygame.mouse.get_pos()
        
        # Vérifier si la souris a été cliquée (bouton gauche de la souris)
        if pygame.mouse.get_pressed()[0] and not self.clicSouris:
            self.gunShotSound.play()
            self.total_shots += 1
            self.clicSouris = True

        # Éviter les clics répétés (on réinitialise le clic après un certain temps)
        if self.clicSouris:
            if not pygame.mouse.get_pressed()[0]:  # Quand la souris n'est plus cliquée
                self.clicSouris = False  # Réinitialiser le clic

    def detecteurTir(self, monstres):
        
        for monstre in monstres:
            if monstre.monster_type == "gator":
                if self.rect.colliderect(monstre.rect) and monstre.vivant :
                    monstre.tir +=1
                    if monstre.tir >=3:  # Vérifie la collision entre le viseur et du monstre
                        monstre.vivant = False  
                        return monstre
            else:
                if self.rect.colliderect(monstre.rect) and monstre.vivant:  # Vérifie la collision entre le viseur et du monstre
                    monstre.vivant = False  
                    return monstre
        return None