import pygame
from zombie import Zombie
from joueur import Joueur
from viseur import Viseur


class Jeu:

    def __init__(self):

        # générer le joueur
        self.joueur = Joueur()

        # groupe de projectiles/zombies
        self.all_zombies_sprites = pygame.sprite.Group()
        self.lancer_zombie(1)

        # le viseur
        self.viseur_sprites = pygame.sprite.Group()
        self.ajouter_viseur()


    def ajouter_viseur(self):

        # Ajout du viseur
        le_viseur = Viseur()
        self.viseur_sprites.add(le_viseur)



    def lancer_zombie(self,type):

        match type:
            case 1:
                
                x = 0
                y = 0
                point = 10
                velocity = 4
                image_path = "assets/images/zombie1.png"

                le_zombie = Zombie(x,y,point,velocity,image_path)
                self.all_zombies_sprites.add(le_zombie)
            case 2:
                x = 0
                y = 0
                point = 10
                velocity = 4
                image_path = "assets/images/zombie2.png"
                
                le_zombie = Zombie(x,y,point,velocity,image_path)
                self.all_zombies_sprites.add(le_zombie)
            case 3:
                x = 0
                y = 0
                point = 10
                velocity = 4
                image_path = "assets/images/zombie3.png"
                
                le_zombie = Zombie(x,y,point,velocity,image_path)
                self.all_zombies_sprites.add(le_zombie)
                le_zombie = Zombie()
                self.all_zombies_sprites.add(le_zombie)