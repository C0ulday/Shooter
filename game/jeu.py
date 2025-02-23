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
        
        # Matériels affichage
        info = pygame.display.Info()
        self.largeur = info.current_w
        self.hauteur = info.current_h - 50
        
        font_size = 16
        self.font = pygame.font.Font("game/assets/font/BPdots.otf", font_size)
        self.font.set_bold(True)
        
        self.fontBtn = "game/assets/font/Minecraft.ttf"
        self.fontSizeBtn = 30
        self.colorPressed = (255, 255, 255)
        self.color = (155, 139, 221)

        # La surface principale d'affichage (display surface)
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur), pygame.RESIZABLE)
        pygame.display.set_caption("Esi-SHOOT")
        
        # Création d'une surface dédiée pour le jeu
        self.gameSurface = pygame.Surface((self.largeur, self.hauteur))

        pygame.mixer.init()

    def updateEnvirnement(self, environment, score):
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
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
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

    def scoreMessage(self, monstre, score):
        if (monstre.monster_type == "aigle"):
            score = self.joueur.setScore(50)
            # Affichage des points dynamiquement
            pointsMessage = {
                "text": "+50",
                "start_time": pygame.time.get_ticks(),
                "x": monstre.rect.x,
                "y": monstre.rect.y
            }
        elif (monstre.monster_type == "gator"):
            score = self.joueur.setScore(100)
            pointsMessage = {
                "text": "+100",
                "start_time": pygame.time.get_ticks(),
                "x": monstre.rect.x,
                "y": monstre.rect.y
            }
        return pointsMessage, score
    
    def affichageTemps(self, temps, temps_passe):
        # Affichage du chronomètre dans le coin supérieur droit
            temps_sec = temps * 0.001
            if temps_sec <= 1:
                temps_text = self.font.render(f"Temps: {temps_sec:.3f} s", True, (255, 0, 0))
                if not temps_passe:
                    #self.exclamationSound.play()
                    temps_passe = True
            else:
                temps_text = self.font.render(f"Temps: {temps_sec:.3f} s", True, (255, 255, 255))
                
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
            y = random.randint(0, self.hauteur - 60)
            self.spawnFrog(x, int(self.hauteur * 0.01), 5)
            # On spawn des aigles avec des vitesses différentes selon le temps restant
            if temps < 2500:
                self.spawnAigles(x, y, 20)
            elif temps < 1500:
                self.spawnAigles(x, y, 40)
            else:
                self.spawnAigles(x, y, 5)

        if len(self.gators) <=0:
            y = random.randint(0, self.hauteur - 60)
            self.spawnGator(x,y,5)

    def playMusic(self,path):
        pygame.mixer.music.load(path)  # Load the music file
        pygame.mixer.music.set_volume(0.03)  # Set volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Play in a loop (-1 means infinite)

    def stopMusic(self):
        pygame.mixer.music.stop()

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
        temps = 1020
        score = 0
        temps_passe = False  # Pour gérer l'activation de l'exclamation
        running = True

        pointsMessage = None

        while running:
            # Limite le nombre de frames par seconde
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                # Gestion du clic de souris pour tirer
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    monstre = self.viseur.sprites()[0].detecteurTir(self.monstres)
                    if (monstre is not None):
                        pointsMessage,score = self.scoreMessage(monstre, score)
                        print(f"Score: {score}")

                # Gestion de l'événement de spawn des monstres
                if event.type == SPAWN_EVENT:
                    self.spawnMonsters(temps)

            self.updateEnvirnement(environment, score)
            self.afficheMessage(pointsMessage)
            self.affichageTemps(temps, temps_passe)

            # Une fois le rendu terminé sur gameSurface, on le blitte sur la display surface
            self.screen.blit(self.gameSurface, (0, 0))
            pygame.display.flip()

            # Décrémentation du temps de jeu
            if temps <= 0:
                running = False
            temps -= 1
            
############################################################################################

    def menu(self):
        # Chargement et redimensionnement de l'image d'arrière-plan
        ecran_img = pygame.image.load("game/assets/gui/ecran_chargement.png")
        ecran_img = pygame.transform.scale(ecran_img, (self.largeur, self.hauteur))
        logos     = pygame.image.load("game/assets/gui/logos.png")
        logos     = pygame.transform.scale(logos, (self.largeur, self.hauteur))

        # Chargement et redimensionnement de toutes les images de boutons et du logo
        jouerBttn    = Bouton(self.largeur//2,self.hauteur//2 - 60 ,"Jouer",self.fontBtn,self.fontSizeBtn,self.color)
        paramBtn    = Bouton(self.largeur//2,self.hauteur//2,"Parametres",self.fontBtn,self.fontSizeBtn,self.color)
        creditsBtn  = Bouton(self.largeur//2,self.hauteur//2 + 60,"Credits",self.fontBtn,self.fontSizeBtn,self.color)
        classBtn    = Bouton(self.largeur//2,self.hauteur//2 + 120,"Classements",self.fontBtn,self.fontSizeBtn,self.color)
        btns = [jouerBttn, paramBtn, creditsBtn, classBtn]
        
        back = (98, 53, 138)
        musicPath = "game/assets/sounds/luv.wav"
        running = True
        self.screen.blit(ecran_img, (0, 0))  # Affiche l'écran de chargement en plein écran
        pygame.display.flip()  # Rafraîchit l'affichage
        pygame.time.wait(3000)  # Pause de 3 secondes avant le menu
        self.playMusic(musicPath)
        while running:
            
            posSouris = pygame.mouse.get_pos()
            #count_temps +=1
            
            self.screen.fill(back)
            self.screen.blit(logos, (self.largeur // 2 - logos.get_width() // 2, 50))  
            for btn in btns :
                btn.update(self.screen,posSouris,self.colorPressed,self.color)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btns[0].boutonHover(posSouris):
                        self.menuJouer(back) 


        pygame.quit()
        
    def menuJouer(self,back):
        retourBtn =  Bouton(self.largeur//2,self.hauteur//2 + 60,"Retour",self.fontBtn,self.fontSizeBtn,self.color)
        nextLevelBtn =  Bouton(self.largeur//2,self.hauteur//2,"Next level",self.fontBtn,self.fontSizeBtn,self.color)
        btns = [retourBtn, nextLevelBtn]
        running = True
        while running:
            posSouris = pygame.mouse.get_pos()
            self.screen.fill(back)
            for btn in btns :
                btn.update(self.screen,posSouris,self.colorPressed,self.color)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if nextLevelBtn.boutonHover(posSouris):
                        self.stopMusic()
                        self.jouer()
                    if retourBtn.boutonHover(posSouris):
                        running = False
