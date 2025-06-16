import pygame, random
from game.monstre import *
from game.joueur import Joueur
from game.viseur import Viseur
from game.bouton import *

class Jeu:
    def __init__(self):
        
        # Création du groupe de sprites pour le viseur
        self.viseur = pygame.sprite.Group()
        self.ajouterViseur() # On ajoute un visuer par défaut

        # Groupes de sprites pour les cibles
        self.aigles = pygame.sprite.Group()
        self.frogs   = pygame.sprite.Group()
        self.gators = pygame.sprite.Group()
        self.monstres = pygame.sprite.Group() # Contient tout les cibles

        # Chargement des images de l'environnement
        self.back       = pygame.image.load("game/assets/mode1/env/back.png")
        self.clouds     = pygame.image.load("game/assets/mode1/env/clouds.png")
        self.decor      = pygame.image.load("game/assets/mode1/env/tiles.png")
        self.rock       = pygame.image.load("game/assets/mode1/env/rock.png")
        self.sol        = pygame.image.load("game/assets/mode1/env/front.png")

        self.exclamationSound = pygame.mixer.Sound("game/assets/sounds/exclamation.wav")
        
        # Le joueur
        self.joueur = Joueur("poulpy")
        self.pause = False

        # Matériels affichage
        info = pygame.display.Info()
        self.largeur = info.current_w
        self.hauteur = info.current_h - 10
        
        font_size = 16
        self.font = pygame.font.Font("game/assets/font/BPdots.otf", font_size)
        self.font.set_bold(True)
        
        # Création d'une surface dédiée pour le jeu
        self.gameSurface = pygame.Surface((self.largeur, self.hauteur))
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur), pygame.RESIZABLE)

        pygame.mixer.init()

    def updateEnvironement(self, environment):
        # Effacer la surface de jeu
        self.gameSurface.fill((0, 0, 0))

        # Affichage des éléments de l'environnement dans l'ordre souhaité sur gameSurface
        for env in environment:
            self.gameSurface.blit(env, (0, 0))

        self.monstres.draw(self.gameSurface)
        self.monstres.update(self.largeur,True)

        # Mise à jour et affichage du viseur
        self.viseur.update()
        self.viseur.draw(self.gameSurface)

        # Affichage du score dans le coin supérieur gauche
        score_text = self.font.render(f"Score: {self.joueur.score}", True, (255, 255, 255))
        self.gameSurface.blit(score_text, (10, 10))

    def ajouterViseur(self):
        # Ajoute le viseur au groupe de sprites
        viseur = Viseur()
        self.viseur.add(viseur)

    def spawnAigles(self, x, y, speed):
        aigle = Monstre("aigle", x, y, speed)
        h = aigle.getHeight()  # Récupération de la hauteur de l'image de l'aigle
        # Ajustement pour éviter qu'une moitié de l'aigle ne spawn
        aigle = Monstre("aigle", x, y - h, speed)
        self.aigles.add(aigle)
        self.monstres.add(*self.aigles)
    
    def spawnFrog(self, x, y, speed):
        frog = Monstre("frog", x, y, speed)
        self.frogs.add(frog)
        self.monstres.add(*self.frogs)
    
    def spawnGator(self, x, y, speed):
        gator = Monstre("gator", x, y, speed)
        self.gators.add(gator)
        self.monstres.add(*self.gators)

    def scoreMessage(self, monstre):
        if (monstre.monster_type == "aigle"):
            self.joueur.setScore(50)
            # Affichage des points dynamiquement
            pointsMessage = {
                "text": "+50",
                "start_time": pygame.time.get_ticks(),
                "x": monstre.rect.x,
                "y": monstre.rect.y
            }
        elif (monstre.monster_type == "gator"):
            self.joueur.setScore(100)
            pointsMessage = {
                "text": "+100",
                "start_time": pygame.time.get_ticks(),
                "x": monstre.rect.x,
                "y": monstre.rect.y
            }
        return pointsMessage
    
    def affichageTemps(self, temps, temps_passe):
        # Affichage du chronomètre dans le coin supérieur droit
        temps_sec = temps * 0.001
        if temps_sec <= 1:
            temps_text = self.font.render(f"Temps: {temps_sec:.1f} s", True, (255, 0, 0))
            if not temps_passe:
                self.exclamationSound.play()
                temps_passe = True
        else:
            temps_text = self.font.render(f"Temps: {temps_sec:.1f} s", True, (255, 255, 255))
            
        temps_rect = temps_text.get_rect(topright=(self.gameSurface.get_width() - 10, 10))
        self.gameSurface.blit(temps_text, temps_rect)

    def afficheMessage(self, pointsMessage):
        # Dessin des points si un message est actif
        if pointsMessage is not None:
            # Durée de vie en millisecondes (ici 2000 ms = 2 secondes)
            duree = 2000
            elapsed = pygame.time.get_ticks() - pointsMessage["start_time"]
            if elapsed < duree:
                # Calcul de l'alpha qui décroît linéairement de 255 à 0
                alpha = 255 - int(255 * elapsed / duree)

                # Création du texte et application de l'alpha
                points_surface = self.font.render(pointsMessage["text"], True, (255, 255, 255))
                points_surface.set_alpha(alpha)
                
                x = pointsMessage["x"]
                y = pointsMessage["y"] - (elapsed/100)
                self.gameSurface.blit(points_surface, (x, y))
            else:
                # Après 2 secondes, on n'affiche plus le message
                pointsMessage = None

    def spawnMonsters(self, temps):
        # Pour n'avoir qu'un seul sprite à la fois
        x = self.largeur
        if len(self.aigles) <=0:
            y = random.randint(0, self.hauteur - 120)
            self.spawnFrog(x, int(self.hauteur * 0.01), 5)
            # On spawn des aigles avec des vitesses différentes selon le temps restant
            if temps < 2500:
                self.spawnAigles(x, y, 20)
            elif temps < 1500:
                self.spawnAigles(x, y, 40)
            else:
                self.spawnAigles(x, y, 5)

        if len(self.gators) <=0:
            y = random.randint(0, self.hauteur - 120)
            self.spawnGator(x,y,5)
            
    def drawPause(self):
        # Création d'une surface semi-transparente
        pause_surface = pygame.Surface((self.largeur, self.hauteur), pygame.SRCALPHA)
        pause_surface.fill((0, 0, 0, 2))

        # Texte "PAUSE"
        pause_text = self.font.render("PAUSE", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.largeur // 2, self.hauteur // 2))

        # Affichage
        self.gameSurface.blit(pause_surface, (0, 0))  # Applique le fond transparent
        self.gameSurface.blit(pause_text, pause_rect)  # Affiche le texte au centre

        

############################################################################################
    def jouer(self):
        
        # Redimensionnement des images pour correspondre à la surface de jeu
        background = pygame.transform.scale(self.back, (self.largeur, self.hauteur))
        clouds     = pygame.transform.scale(self.clouds, (self.largeur, self.hauteur))
        sol        = pygame.transform.scale(self.sol, (self.largeur, self.hauteur))
        rock       = pygame.transform.scale(self.rock, (self.largeur, self.hauteur))
        decor      = pygame.transform.scale(self.decor, (self.largeur, self.hauteur))
        environment = [background, clouds, sol, rock, decor]

        # Définition d'un événement personnalisé pour le spawn des monstres (toutes les 1.5 secondes)
        SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_EVENT, 1500)

        clock = pygame.time.Clock()
        fps = 60 
        temps = 30000 # 30 secondes 
        self.joueur.score = 0
        temps_passe = False  # Pour gérer l'activation de l'exclamation
        running = True
        endingTime = temps + pygame.time.get_ticks()
        pointsMessage = None

        self.aigles = pygame.sprite.Group()
        self.frogs   = pygame.sprite.Group()
        self.gators = pygame.sprite.Group()
        self.monstres = pygame.sprite.Group()
        self.spawnMonsters(temps)
        
        while running:
            # Limite le nombre de frames par seconde
            clock.tick(fps)
            for event in pygame.event.get():
                
                # Gestion de la fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                # Gestion du clic de souris pour tirer
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    monstre = self.viseur.sprites()[0].detecteurTir(self.monstres)
                    if (monstre is not None):
                        pointsMessage = self.scoreMessage(monstre)
                        print(f"Score: {self.joueur.score}")
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if  not self.pause:
                        print("pause")
                        self.pause = True             
                    else:
                        self.pause = False

                # Gestion de l'événement de spawn des monstres
                if event.type == SPAWN_EVENT:
                    self.spawnMonsters(temps)

            if not self.pause:
                self.updateEnvironement(environment)
                self.afficheMessage(pointsMessage)
                self.affichageTemps(endingTime - pygame.time.get_ticks(), temps_passe)
                
                # Décrémentation du temps de jeu
                if pygame.time.get_ticks() >= endingTime:
                    running = False
                
            else:
                self.drawPause()    
            
            # Une fois le rendu terminé sur gameSurface, on le blitte sur la display surface
            self.screen.blit(self.gameSurface, (0, 0))
            pygame.display.flip()
            
            

