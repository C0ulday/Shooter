import pygame
from monstre import *
from joueur import Joueur
from viseur import Viseur


class Jeu:

    def __init__(self):

        # le viseur
        self.viseur = pygame.sprite.Group()
        self.ajouterViseur()

        # L'ensemble des monstres aigles
        self.aigles = pygame.sprite.Group()
        self.frog = pygame.sprite.Group()

    def jouer(self):

        #### AFFICHAGE
        pygame.display.set_caption("M-Shooter")

        # Initialisation fenêtre de jeu classique
        background = pygame.image.load("shooter.jeu/assets/mode1/env/back.png")
        clouds = pygame.image.load("shooter.jeu/assets/mode1/env/clouds.png")
        decor = pygame.image.load("shooter.jeu/assets/mode1/env/tiles.png")
        rock = pygame.image.load("shooter.jeu/assets/mode1/env/rock.png")
        sol = pygame.image.load("shooter.jeu/assets/mode1/env/front.png")
        
        font = pygame.font.Font("shooter.jeu/assets/font/BPdots.otf",16)
        font.set_bold(True)

        score = 0  # Initialisation du score

        ######## Boucle de jeu

        info = pygame.display.Info()
        largeur = info.current_w
        hauteur = info.current_h

        screen = pygame.display.set_mode((largeur,hauteur),pygame.FULLSCREEN)

        # Définition d'un événement pour le spawn de monstres
        SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_EVENT, 2000)  # un monstre toutes les 2 secondes


        # Timer

        clock = pygame.time.Clock()
        temps = 3000 # 3s
        fps = 60

        running = True
        while running :

            #environnement
            clock.tick(fps)
            screen.blit(background, (0,0))
            screen.blit(clouds, (0,0))
            screen.blit(rock, (930,840))
            screen.blit(decor, (0,827))
            screen.blit(sol, (0,1020))


            # Affichagfe des aigles
            self.aigles.draw(screen)
            self.aigles.update(True)

            # Ajout des grenouilles
            self.frog.draw(screen)
            self.frog.update()

            # Affichage du viseur
            self.viseur.update()
            self.viseur.draw(screen)

            # Affichage du score
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            # Affichage du chronomètre
            temps_text = font.render(f"temps: {temps} ms", True, (255, 255, 255))
            temps_rect = temps_text.get_rect(topright=(screen.get_width() - 10, 10))
            screen.blit(temps_text, temps_rect)
        
            # Mis à jour de la fenetre
            pygame.display.flip()

            # Gestion du temps de jeu
            if temps <=0 :
                running = False

            temps -=1
            # Gestion des évènements du jeu
            for event in pygame.event.get():

                # Vérification du tir avec clic de la souris
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                    if self.viseur.sprites()[0].detecteurTir(self.aigles):
                        score += 50
                        print(f"Score: {score}")
                # Affichae de la grneouille
                if (len(self.frog) <= 0):
                    self.spawnFrog(5)
                # Affichage des aigles à différentes positions
                if event.type == SPAWN_EVENT:
                    x = largeur
                    y = random.randint(0, hauteur - sol.get_height())
                    if temps < 2500:
                        self.spawnAigles(x,y,10)
                    if temps < 1500:
                        self.spawnAigles(x,y,10)
                    else:
                        self.spawnAigles(x,y,5)

                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
             
                    

                #print(temps)
            clock.tick(fps)
            
    
    def ajouterViseur(self):
        viseur = Viseur()
        self.viseur.add(viseur)

    # Lancer les monstres

    def spawnAigles(self,x,y,speed):
        aigle = Aigle(x,y,speed)
        h = aigle.getAigleHeight() # utilisé pour obtenir la hauteur de l'image de l'aigle
        aigle = Aigle(x,y - h,speed) # la soustraction permet de faire spawn l'aigle en entier sur l'écran 
        # à chaque fois et non une seule partie
        self.aigles.add(aigle)
    
    def spawnFrog(self,speed):
        frog = Frog(speed)
        frog = Frog(speed) # la soustraction permet de faire spawn l'aigle en entier sur l'écran 
        # à chaque fois et non une seule partie
        self.frog.add(frog)



