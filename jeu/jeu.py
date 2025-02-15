import pygame, random
from monstre import *
from joueur import Joueur
from viseur import Viseur
from bouton import *

class Jeu:
    def __init__(self):
        
        # Création du groupe de sprites pour le viseur
        self.viseur = pygame.sprite.Group()
        self.ajouterViseur() # On ajoute un visuer par défaut

        # Groupes de sprites pour les cibles
        self.aigles = pygame.sprite.Group()
        self.frogs   = pygame.sprite.Group()

        # Chargement des images de l'environnement
        self.back = pygame.image.load("jeu/assets/mode1/env/back.png")
        self.clouds     = pygame.image.load("jeu/assets/mode1/env/clouds.png")
        self.decor      = pygame.image.load("jeu/assets/mode1/env/tiles.png")
        self.rock       = pygame.image.load("jeu/assets/mode1/env/rock.png")
        self.sol        = pygame.image.load("jeu/assets/mode1/env/front.png")
        
        self.exclamationSound = pygame.mixer.Sound("jeu/assets/sounds/exclamation.wav")
        
        # Le joueur
        self.joueur = Joueur("poulpy")
        
        # Matériels affichage
        
        info = pygame.display.Info()
        self.largeur = info.current_w
        self.hauteur = info.current_h - 50
        
        font_size = 16
        self.font = pygame.font.Font("jeu/assets/font/BPdots.otf", font_size)
        self.font.set_bold(True)
        
        self.font_btn = "jeu/assets/font/Minecraft.ttf"
        self.font_size_btn = 30
        self.color_pressed = (255,255,255)
        self.color = (155,139,221)


############################################################################################


############################################################################################
    def jouer(self):
        
        screen = pygame.display.set_mode((self.largeur, self.hauteur),pygame.RESIZABLE)
        pygame.display.set_caption("Esi-SHOOT")

        
        screen = pygame.display.set_mode((self.largeur, self.hauteur),pygame.RESIZABLE)
        
        # Redimensionnement
        background = pygame.transform.scale(self.back, (self.largeur, self.hauteur))
        clouds     = pygame.transform.scale(self.clouds, (self.largeur, self.hauteur))
        sol =  pygame.transform.scale(self.sol, (self.largeur, self.hauteur))
        rock =  pygame.transform.scale(self.rock, (self.largeur, self.hauteur))
        decor =  pygame.transform.scale(self.decor, (self.largeur, self.hauteur))

        # Définition d'un événement personnalisé pour le spawn des monstres (toutes les 2 secondes)
        SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_EVENT, 1500)

        clock = pygame.time.Clock()
        fps = 120 
        temps = 3000
        score = 0
        temps_passe = False # Pour gérer l'activation de l'exclamation
        running = True
        

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                # Gestion du clic de souris pour tirer
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.viseur.sprites()[0].detecteurTir(self.aigles):
                        score = self.joueur.setScore(50)
                        print(f"Score: {score}")

                # Gestion de l'événement de spawn des monstres
                if event.type == SPAWN_EVENT:
                    x = self.largeur
                    y = random.randint(0, self.hauteur - 50)
                    self.spawnFrog(x, self.hauteur * 0.01,5)
                    # On spawn des aigles avec des vitesses différentes selon le temps restant
                    if temps < 2500:
                        self.spawnAigles(x, y, 20)
                    elif temps < 1500:
                        self.spawnAigles(x, y, 40)
                    else:
                        self.spawnAigles(x, y, 5)

            # Limite le nombre de frames par seconde
            clock.tick(fps)
            # Affichage des éléments de l'environnement dans l'ordre souhaité
            screen.blit(background, (0, 0))
            screen.blit(clouds, (0, 0))
            screen.blit(rock, (0, 0))
            screen.blit(decor, (0, 0))
            screen.blit(sol, (0, 0))

            # Affichage et mise à jour des sprites des aigles
            self.aigles.draw(screen)
            self.aigles.update(True)

            # Affichage et mise à jour des sprites des grenouilles
            self.frogs.draw(screen)
            self.frogs.update()

            # Mise à jour et affichage du viseur
            self.viseur.update()
            self.viseur.draw(screen)

            # Affichage du score dans le coin supérieur gauche
            score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            temps_sec = temps * 0.001
            
            # Affichage du chronomètre dans le coin supérieur droit
            temps_text = self.font.render(f"Temps: {temps_sec:.3f} s", True, (255, 255, 255))
            if (temps_sec <= 1):
                temps_text = self.font.render(f"Temps: {temps_sec:.3f} s", True, (255, 0, 0))
                
                if(temps_passe == False):
                    self.exclamationSound.play()
                    temps_passe = True
                
                
            temps_rect = temps_text.get_rect(topright=(screen.get_width() - 10, 10))
            screen.blit(temps_text, temps_rect)

            # Mise à jour de l'affichage
            pygame.display.flip()

            # Décrémentation du temps de jeu
            if temps <= 0:
                running = False
            temps -= 1
            
############################################################################################

    def menu(self):
        
        pygame.display.set_caption("Esi-SHOOT")
        screen = pygame.display.set_mode((self.largeur, self.hauteur), pygame.RESIZABLE)
        # Chargement et redimensionnement de l'image d'arrière-plan
        ecran_img = pygame.image.load("jeu/assets/gui/ecran_chargement.png")
        ecran_img= pygame.transform.scale(ecran_img, (self.largeur, self.hauteur))

        # Chargement et redimensionnement de toutes les images de boutons et du logo
        jouer_btn    = Bouton(self.largeur//2,self.hauteur//2 - 60 ,"Jouer",self.font_btn,self.font_size_btn,self.color)
        param_btn    = Bouton(self.largeur//2,self.hauteur//2,"Parametres",self.font_btn,self.font_size_btn,self.color)
        credits_btn  = Bouton(self.largeur//2,self.hauteur//2 + 60,"Credits",self.font_btn,self.font_size_btn,self.color)
        class_btn    = Bouton(self.largeur//2,self.hauteur//2 + 120,"Classements",self.font_btn,self.font_size_btn,self.color)

        #logos        = pygame.image.load("jeu/assets/gui/logos.png")
        #logos        = pygame.transform.scale(logos, (self.largeur, hauteur))
        
        back = (98, 53, 138)
        music = pygame.mixer.Sound("jeu/assets/sounds/luv.wav")
        
        running = True
        while running:
            
            pos_souris = pygame.mouse.get_pos()
            #count_temps +=1
            music.play()
            #screen.blit(ecran_img,(0,0))
            
            screen.fill(back)
            #screen.blit(logos,(0,0))
            
            jouer_btn.update(screen,pos_souris,self.color_pressed,self.color)
            class_btn.update(screen,pos_souris,self.color_pressed,self.color)
            param_btn.update(screen,pos_souris,self.color_pressed,self.color)
            credits_btn.update(screen,pos_souris,self.color_pressed,self.color)
            
            pygame.display.flip()
            
            # Affichage des modes de jeu
            
            if (jouer_btn.boutonHover(pos_souris) and pygame.mouse.get_pressed()[0]):
                self.menu_jouer(screen,back)
                
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                
        pygame.quit()
        
    def menu_jouer(self,screen,back):
        
        retour_btn =  Bouton(self.largeur//2,self.hauteur//2,"Retour",self.font_btn,self.font_size_btn,self.color)
        running = True
        while running:

            pos_souris = pygame.mouse.get_pos()
            screen.fill(back)
            retour_btn.update(screen,pos_souris,self.color_pressed,self.color)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
        pygame.quit()
############################################################################################
    def ajouterViseur(self):
        # Ajoute le viseur au groupe de sprites
        viseur = Viseur()
        self.viseur.add(viseur)

    def spawnAigles(self, x, y, speed):
        aigle = Monstre("aigle",x, y, speed)
        h = aigle.getHeight()  # Récupération de la hauteur de l'image de l'aigle
        aigle = Monstre("aigle",x, y - h, speed) # Pour éviter qu'une moitié de l'aigle ne spawn
        self.aigles.add(aigle)
    
    def spawnFrog(self,x,y,speed):
        frog = Monstre("frog",x,y,speed)
        self.frogs.add(frog)
