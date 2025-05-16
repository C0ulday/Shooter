import pygame
from const import *
from cible import Cible
import random

# Création de la classe de jeu

class Jeu:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.cibles = [] # Tableau des cibles que contient le jeu
        self.score = 0 # Score du joueur
        
        self.temps_restant = 180  # Temps de jeu en secondes
        
        self.fenetre = pygame.display.set_mode((largeur, hauteur))
        pygame.display.set_caption("Jeu de tir - ver0")
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.jeu_en_cours = True

    def addCible(self,cible):
        self.cibles.append(cible)
    
    def removeCible(self, cible):
        self.cibles.remove(cible)
    
    def updateEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jeu_en_cours = False
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for cible in self.cibles:
                    if cible.collision(x, y):
                        self.score += 1
                        self.cibles.remove(cible)
                        x = random.randint(0, self.largeur)
                        y = random.randint(0, self.hauteur)
                        #Attendre un moment avant de créer une nouvelle cible
                        pygame.time.delay(200)
                        self.addCible(Cible(x,y,50)) #  Ajout d'une nouvelle cible
                        break
        return True
    
    def updateMove(self):
        for cible in self.cibles:
            cible.move()
            
    def draw(self):
        self.fenetre.fill(BLANC)
        for cible in self.cibles:
            cible.draw(self.fenetre)
        # Affichage du score
        score_text = self.font.render("Score: " + str(self.score), True, NOIR)
        self.fenetre.blit(score_text, (10, 10))
        pygame.display.flip()
        
    def run(self): 
        pygame.init()
        

        cible = Cible(2,2,50)
        self.cibles.append(cible)
        
        while self.jeu_en_cours:
            self.temps_restant -= 1 / FPS
            if self.temps_restant <= 0:
                self.jeu_en_cours = False
                break
            
            self.updateEvents()
            self.updateMove()
            self.draw()
            
            # Limiter le nombre d'images par seconde
            self.clock.tick(FPS)
        
        pygame.quit()
        
