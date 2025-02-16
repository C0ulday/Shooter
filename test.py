import math
import pygame
from jeu import Jeu
pygame.init()

#### AFFICHAGE
pygame.display.set_caption("M-Shooter")

# Background
background = pygame.image.load("assets/environnement/back.png")
sol = pygame.image.load("assets/environnement/tiles.png")

running = True

timer = pygame.time.Clock()
font = pygame.font.Font("assets/font/BPdots.otf")

# Le jeu
jeu = Jeu(160+500)
score = 0  # Initialisation du score

screen = pygame.display.set_mode((jeu.WIDTH,jeu.HEIGHT))

while running :

    timer.tick(jeu.fps)
    screen.blit(background, (0,0))
    screen.blit(sol, (0,0))
   
    jeu.viseur.update()
    jeu.viseur.draw(screen)

    jeu.aigles.draw(screen)
    jeu.aigles.update()
   

    # Affichage du score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
   
    pygame.display.flip()

    if (len(jeu.aigles) == 0):
        jeu.spawnAigle()

    for event in pygame.event.get():
        # Vérification du tir avec clic de la souris
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            if jeu.viseur.sprites()[0].detecteur_tir(jeu.aigles):
                score += 1  # Ajoute 50 points par tir réussi
                print(f"Score: {score}")

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()


# pygame.display.set_caption("Esi-SHOOT")
#         screen = pygame.display.set_mode((self.largeur, self.hauteur), pygame.RESIZABLE)
#         # Chargement et redimensionnement de l'image d'arrière-plan
#         ecran_img = pygame.image.load("game/assets/gui/ecran_chargement.png")
#         ecran_img= pygame.transform.scale(ecran_img, (self.largeur, self.hauteur))

#         # Chargement et redimensionnement de toutes les images de boutons et du logo
#         jouer_btn    = Bouton(self.largeur//2,self.hauteur//2 - 60 ,"Jouer",self.font_btn,self.font_size_btn,self.color)
#         param_btn    = Bouton(self.largeur//2,self.hauteur//2,"Parametres",self.font_btn,self.font_size_btn,self.color)
#         credits_btn  = Bouton(self.largeur//2,self.hauteur//2 + 60,"Credits",self.font_btn,self.font_size_btn,self.color)
#         class_btn    = Bouton(self.largeur//2,self.hauteur//2 + 120,"Classements",self.font_btn,self.font_size_btn,self.color)

#         #logos        = pygame.image.load("game/assets/gui/logos.png")
#         #logos        = pygame.transform.scale(logos, (self.largeur, hauteur))
        
#         back = (98, 53, 138)
#         music = pygame.mixer.Sound("game/assets/sounds/luv.wav")
        
#         running = True
#         while running:
            
#             pos_souris = pygame.mouse.get_pos()
#             #count_temps +=1
#             music.play()
#             #screen.blit(ecran_img,(0,0))
            
#             screen.fill(back)
#             #screen.blit(logos,(0,0))
            
#             jouer_btn.update(screen,pos_souris,self.color_pressed,self.color)
#             class_btn.update(screen,pos_souris,self.color_pressed,self.color)
#             param_btn.update(screen,pos_souris,self.color_pressed,self.color)
#             credits_btn.update(screen,pos_souris,self.color_pressed,self.color)
            
#             pygame.display.flip()
            
#             # Affichage des modes de jeu
            
#             if (jouer_btn.boutonHover(pos_souris) and pygame.mouse.get_pressed()[0]):
#                 self.menu_jouer(screen,back)
                
            
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
                
                
#         pygame.quit()
        
#     def menu_jouer(self,screen,back):
        
#         retour_btn =  Bouton(self.largeur//2,self.hauteur//2,"Retour",self.font_btn,self.font_size_btn,self.color)
#         running = True
#         while running:

#             pos_souris = pygame.mouse.get_pos()
#             screen.fill(back)
#             retour_btn.update(screen,pos_souris,self.color_pressed,self.color)
#             pygame.display.flip()
            
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
                
#         pygame.quit()