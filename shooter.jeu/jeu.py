import pygame, random
from monstre import *  # Importation des classes liées aux monstres (Aigle, Frog, etc.)
from joueur import Joueur
from viseur import Viseur

class Jeu:
    def __init__(self):
        
        # Création du groupe de sprites pour le viseur
        self.viseur = pygame.sprite.Group()
        self.ajouterViseur() # On ajoute un visuer par défaut

        # Groupes de sprites pour les cibles
        self.aigles = pygame.sprite.Group()
        self.frogs   = pygame.sprite.Group()

        # Chargement des images de l'environnement
        self.back = pygame.image.load("shooter.jeu/assets/mode1/env/back.png")
        self.clouds     = pygame.image.load("shooter.jeu/assets/mode1/env/clouds.png")
        self.decor      = pygame.image.load("shooter.jeu/assets/mode1/env/tiles.png")
        self.rock       = pygame.image.load("shooter.jeu/assets/mode1/env/rock.png")
        self.sol        = pygame.image.load("shooter.jeu/assets/mode1/env/front.png")
        
        self.exclamationSound = pygame.mixer.Sound("shooter.jeu/assets/sounds/exclamation.wav")
        
        # Le joueur
        self.joueur = Joueur("poulpy")

############################################################################################


############################################################################################
    def jouer(self):
        
        pygame.display.set_caption("Esi-SHOOT")
        font_size = 16
        font = pygame.font.Font("shooter.jeu/assets/font/BPdots.otf", font_size)
        font.set_bold(True)

        # Récupération des dimensions de l'écran
        info = pygame.display.Info()
        # On démarre avec une fenêtre à la moitié des dimensions de l'écran
        largeur = info.current_w // 2  
        hauteur = info.current_h // 2

        screen = pygame.display.set_mode((largeur, hauteur), pygame.RESIZABLE)
        
        # Redimensionnement
        background = pygame.transform.scale(self.back, (largeur, hauteur))
        clouds     = pygame.transform.scale(self.clouds, (largeur, hauteur))
        sol =  pygame.transform.scale(self.sol, (largeur, hauteur))
        rock =  pygame.transform.scale(self.rock, (largeur, hauteur))
        decor =  pygame.transform.scale(self.decor, (largeur, hauteur))

        # Définition d'un événement personnalisé pour le spawn des monstres (toutes les 2 secondes)
        SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_EVENT, 2000)

        clock = pygame.time.Clock()
        fps = 60 
        temps = 3000
        score = 0
        temps_passe = False # Pour gérer l'activation de l'exclamation
        running = True
        

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                
                # Gestion de l'événement de redimensionnement de la fenêtre
                if event.type == pygame.VIDEORESIZE:
                    largeur, hauteur = event.size
                    screen = pygame.display.set_mode((largeur, hauteur), pygame.RESIZABLE)
                    # Redimensionnement dynamique des images en fonction des dimensions actuelles de la fenêtre
                    background = pygame.transform.scale(self.back, (largeur, hauteur))
                    clouds     = pygame.transform.scale(self.clouds, (largeur, hauteur))
                    sol =  pygame.transform.scale(self.sol, (largeur, hauteur))
                    rock =  pygame.transform.scale(self.rock, (largeur, hauteur))
                    decor =  pygame.transform.scale(self.decor, (largeur, hauteur))

                # Gestion du clic de souris pour tirer
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.viseur.sprites()[0].detecteurTir(self.aigles):
                        score = self.joueur.setScore(50)
                        print(f"Score: {score}")

                # Gestion de l'événement de spawn des monstres
                if event.type == SPAWN_EVENT:
                    x = largeur
                    y = random.randint(0, hauteur - 50)
                    self.spawnFrog(x,hauteur * 0.01,5)
                    # On spawn des aigles avec des vitesses différentes selon le temps restant
                    if temps < 2500:
                        self.spawnAigles(x, y, 20)
                    elif temps < 1500:
                        self.spawnAigles(x, y, 30)
                    else:
                        self.spawnAigles(x, y, 10)

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
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            temps_sec = temps * 0.001
            
            # Affichage du chronomètre dans le coin supérieur droit
            temps_text = font.render(f"Temps: {temps_sec:.3f} s", True, (255, 255, 255))
            if (temps_sec <= 1):
                temps_text = font.render(f"Temps: {temps_sec:.3f} s", True, (255, 0, 0))
                
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

