import pygame, random
from monstre import *
from joueur import Joueur
from viseur import Viseur
from bouton import *

class Jeu:
    def __init__(self):
        # Création du groupe de sprites pour le viseur
        self.viseur = pygame.sprite.Group()
        self.ajouterViseur()  # On ajoute un viseur par défaut

        # Groupes de sprites pour les cibles
        self.aigles = pygame.sprite.Group()
        self.frogs  = pygame.sprite.Group()

        # Chargement des images de l'environnement
        self.back   = pygame.image.load("game/assets/mode1/env/back.png")
        self.clouds = pygame.image.load("game/assets/mode1/env/clouds.png")
        self.decor  = pygame.image.load("game/assets/mode1/env/tiles.png")
        self.rock   = pygame.image.load("game/assets/mode1/env/rock.png")
        self.sol    = pygame.image.load("game/assets/mode1/env/front.png")
        
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
        
        self.font_btn = "game/assets/font/Minecraft.ttf"
        self.font_size_btn = 30
        self.color_pressed = (255, 255, 255)
        self.color = (155, 139, 221)

        # La surface principale d'affichage (display surface)
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur), pygame.RESIZABLE)
        pygame.display.set_caption("Esi-SHOOT")
        
        # Création d'une surface dédiée pour le jeu
        self.game_surface = pygame.Surface((self.largeur, self.hauteur))
        
    ############################################################################################
    def jouer(self):
        # Redimensionnement des images pour correspondre à la surface de jeu
        background = pygame.transform.scale(self.back, (self.largeur, self.hauteur))
        clouds     = pygame.transform.scale(self.clouds, (self.largeur, self.hauteur))
        sol        = pygame.transform.scale(self.sol, (self.largeur, self.hauteur))
        rock       = pygame.transform.scale(self.rock, (self.largeur, self.hauteur))
        decor      = pygame.transform.scale(self.decor, (self.largeur, self.hauteur))

        # Définition d'un événement personnalisé pour le spawn des monstres (toutes les 1.5 secondes)
        SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_EVENT, 1500)

        clock = pygame.time.Clock()
        fps = 120 
        temps = 3000
        score = 0
        temps_passe = False  # Pour gérer l'activation de l'exclamation
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
                    self.spawnFrog(x, int(self.hauteur * 0.01), 5)
                    # On spawn des aigles avec des vitesses différentes selon le temps restant
                    if temps < 2500:
                        self.spawnAigles(x, y, 20)
                    elif temps < 1500:
                        self.spawnAigles(x, y, 40)
                    else:
                        self.spawnAigles(x, y, 5)

            # Limite le nombre de frames par seconde
            clock.tick(fps)

            # Effacer la surface de jeu
            self.game_surface.fill((0, 0, 0))

            # Affichage des éléments de l'environnement dans l'ordre souhaité sur game_surface
            self.game_surface.blit(background, (0, 0))
            self.game_surface.blit(clouds, (0, 0))
            self.game_surface.blit(rock, (0, 0))
            self.game_surface.blit(decor, (0, 0))
            self.game_surface.blit(sol, (0, 0))

            # Affichage et mise à jour des sprites des aigles
            self.aigles.draw(self.game_surface)
            self.aigles.update(True)

            # Affichage et mise à jour des sprites des grenouilles
            self.frogs.draw(self.game_surface)
            self.frogs.update()

            # Mise à jour et affichage du viseur
            self.viseur.update()
            self.viseur.draw(self.game_surface)

            # Affichage du score dans le coin supérieur gauche
            score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
            self.game_surface.blit(score_text, (10, 10))

            # Affichage du chronomètre dans le coin supérieur droit
            temps_sec = temps * 0.001
            if temps_sec <= 1:
                temps_text = self.font.render(f"Temps: {temps_sec:.3f} s", True, (255, 0, 0))
                if not temps_passe:
                    self.exclamationSound.play()
                    temps_passe = True
            else:
                temps_text = self.font.render(f"Temps: {temps_sec:.3f} s", True, (255, 255, 255))
                
            temps_rect = temps_text.get_rect(topright=(self.game_surface.get_width() - 10, 10))
            self.game_surface.blit(temps_text, temps_rect)

            # Une fois le rendu terminé sur game_surface, on le blitte sur la display surface
            self.screen.blit(self.game_surface, (0, 0))
            pygame.display.flip()

            # Décrémentation du temps de jeu
            if temps <= 0:
                running = False
            temps -= 1
            
    ############################################################################################
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
    
    def spawnFrog(self, x, y, speed):
        frog = Monstre("frog", x, y, speed)
        self.frogs.add(frog)
