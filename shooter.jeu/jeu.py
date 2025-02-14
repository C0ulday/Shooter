import pygame, random
from monstre import *  # Importation des classes liées aux monstres (Aigle, Frog, etc.)
from joueur import Joueur
from viseur import Viseur

class Jeu:
    def __init__(self):
        # Création du groupe de sprites pour le viseur
        self.viseur = pygame.sprite.Group()
        self.ajouterViseur()

        # Groupes de sprites pour les aigles et les grenouilles
        self.aigles = pygame.sprite.Group()
        self.frog   = pygame.sprite.Group()

        # Chargement des images de l'environnement une seule fois
        self.back = pygame.image.load("shooter.jeu/assets/mode1/env/back.png")
        self.clouds     = pygame.image.load("shooter.jeu/assets/mode1/env/clouds.png")
        self.decor      = pygame.image.load("shooter.jeu/assets/mode1/env/tiles.png")
        self.rock       = pygame.image.load("shooter.jeu/assets/mode1/env/rock.png")
        self.sol        = pygame.image.load("shooter.jeu/assets/mode1/env/front.png")

    def jouer(self):
        # Définition du titre de la fenêtre
        pygame.display.set_caption("M-Shooter")

        # Chargement et configuration de la police d'affichage
        font = pygame.font.Font("shooter.jeu/assets/font/BPdots.otf", 16)
        font.set_bold(True)
        score = 0  # Score initial

        # Récupération des dimensions de l'écran (pour la première création de la fenêtre)
        info = pygame.display.Info()
        # On démarre avec une fenêtre à la moitié des dimensions de l'écran
        largeur = info.current_w // 2  
        hauteur = info.current_h // 2

        # Création d'une fenêtre redimensionnable
        screen = pygame.display.set_mode((largeur, hauteur), pygame.RESIZABLE)

        # Définition d'un événement personnalisé pour le spawn des monstres (toutes les 2 secondes)
        SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_EVENT, 2000)

        clock = pygame.time.Clock()
        fps = 60      # Limite à 60 images par seconde
        temps = 3000  # Temps de jeu en "ticks"

        running = True
        while running:
            # Parcours de tous les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Si l'utilisateur ferme la fenêtre, on arrête le jeu
                    running = False
                    pygame.quit()
                
                # Gestion de l'événement de redimensionnement de la fenêtre
                if event.type == pygame.VIDEORESIZE:
                    largeur, hauteur = event.size  # Mise à jour des dimensions
                    # Recréation de la fenêtre avec les nouvelles dimensions
                    screen = pygame.display.set_mode((largeur, hauteur), pygame.RESIZABLE)
                    # Vous pouvez ajouter ici des actions supplémentaires (par exemple, recalculer des positions)

                # Gestion du clic de souris pour tirer
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Si le viseur détecte un tir sur un aigle, on augmente le score
                    if self.viseur.sprites()[0].detecteurTir(self.aigles):
                        score += 50
                        print(f"Score: {score}")

                # Gestion de l'événement de spawn des monstres
                if event.type == SPAWN_EVENT:
                    x = largeur  # Position x à droite de l'écran
                    # On s'assure que 'sol' ne déborde pas en utilisant la hauteur de l'image
                    y = random.randint(0, hauteur - self.sol.get_height())
                    # On spawn des aigles avec des vitesses différentes selon le temps restant
                    if temps < 2500:
                        self.spawnAigles(x, y, 10)
                    elif temps < 1500:
                        self.spawnAigles(x, y, 10)
                    else:
                        self.spawnAigles(x, y, 5)
            
            # Redimensionnement dynamique des images en fonction des dimensions actuelles de la fenêtre
            background = pygame.transform.scale(self.back, (largeur, hauteur))
            clouds     = pygame.transform.scale(self.clouds, (largeur, hauteur))
            decor = self.decor
            
            # Calcul d'un ratio de redimensionnement basé sur la largeur par rapport à la référence 1920
            ratio = largeur / 1920
            # Redimensionnement de l'image rock et sol en fonction du ratio calculé
            rock = pygame.transform.scale(self.rock, (int(self.rock.get_width() * ratio), int(self.rock.get_height() * ratio)))
            sol  = pygame.transform.scale(self.sol,  (int(self.sol.get_width() * ratio),  int(self.sol.get_height() * ratio)))

            # Calcul des positions en pourcentages sur une référence de 1920 x 1080
            pos_rock  = (int(0.4844 * largeur), int(0.7778 * hauteur))
            pos_decor = (int(0.0 * largeur), int(0.7657 * hauteur))
            pos_sol   = (int(0.0 * largeur), int(0.9444 * hauteur))

            # Contrôle du nombre de ticks par seconde
            clock.tick(fps)

            # Affichage des éléments de l'environnement dans l'ordre souhaité
            screen.blit(background, (0, 0))
            screen.blit(clouds, (0, 0))
            screen.blit(rock, pos_rock)
            screen.blit(decor, pos_decor)
            screen.blit(sol, pos_sol)

            # Affichage et mise à jour des sprites des aigles
            self.aigles.draw(screen)
            self.aigles.update(True)

            # Affichage et mise à jour des sprites des grenouilles
            self.frog.draw(screen)
            self.frog.update()

            # Mise à jour et affichage du viseur
            self.viseur.update()
            self.viseur.draw(screen)

            # Affichage du score dans le coin supérieur gauche
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            # Affichage du chronomètre dans le coin supérieur droit
            temps_text = font.render(f"Temps: {temps} ms", True, (255, 255, 255))
            temps_rect = temps_text.get_rect(topright=(screen.get_width() - 10, 10))
            screen.blit(temps_text, temps_rect)

            # Mise à jour de l'affichage
            pygame.display.flip()

            # Décrémentation du temps de jeu
            if temps <= 0:
                running = False
            temps -= 1

            # Tick supplémentaire pour s'assurer du respect du fps (facultatif)
            clock.tick(fps)

    def ajouterViseur(self):
        # Ajoute le viseur au groupe de sprites
        viseur = Viseur()
        self.viseur.add(viseur)

    def spawnAigles(self, x, y, speed):
        # Crée un aigle et ajuste sa position pour qu'il soit entièrement visible
        aigle = Aigle(x, y, speed)
        h = aigle.getAigleHeight()  # Récupération de la hauteur de l'image de l'aigle
        aigle = Aigle(x, y - h, speed)
        self.aigles.add(aigle)
    
    def spawnFrog(self, speed):
        # Crée une grenouille et l'ajoute au groupe de sprites
        frog = Frog(speed)
        self.frog.add(frog)

