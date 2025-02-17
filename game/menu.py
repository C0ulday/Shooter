import pygame
from game.jeu import Jeu
from game.bouton import Bouton


class menu():
    def __init__(self,jeu):
        
        self.jeu = jeu
        self.back_color = (98, 53, 138)
        self.run_display = True
        self.menu_surface = pygame.Surface(jeu.largeur,jeu.hauteur)
        self.menu_screen = pygame.display.set_mode((jeu.largeur, jeu.hauteur), pygame.RESIZABLE)
    
    def blitMenu(self):
        self.jeu.screen.blit(self.menu_screen, (0,0))
        pygame.display.update()
    
class mainMenu(menu):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.jouer_btn    = Bouton(jeu.largeur//2,jeu.hauteur//2 - 60 ,"Jouer",self.font_btn,self.font_size_btn,self.color)
        self.param_btn    = Bouton(jeu.largeur//2,jeu.hauteur//2,"Parametres",self.font_btn,self.font_size_btn,self.color)
        self.credits_btn  = Bouton(jeu.largeur//2,jeu.hauteur//2 + 60,"Credits",self.font_btn,self.font_size_btn,self.color)
        self.class_btn    = Bouton(jeu.largeur//2,jeu.hauteur//2 + 120,"Classements",self.font_btn,self.font_size_btn,self.color)

    def blitMainMenu(self):

        self.run_display = True
        while self.run_display:
            self.jeu.game_surface.fill(self.back_color)
            