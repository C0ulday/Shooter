import pygame
from game.jeu import Jeu
from game.bouton import Bouton

class Menu:
    def __init__(self, jeu):
        
        self.jeu = jeu
        self.back_color = (98, 53, 138)
        self.run_display = True
        self.gameScore = 0

        # Initialisation de l'écran principal
        self.screen = jeu.screen
        pygame.display.set_caption("Esi-SHOOT")

        # Surface optionnelle pour le menu (si vous souhaitez dessiner séparément)
        self.menu_surface = pygame.Surface((jeu.largeur, jeu.hauteur))

        # Chemin vers la musique et chargement des images
        self.musicPath = "game/assets/sounds/luv.wav"
        self.loadingImage = pygame.image.load("game/assets/gui/ecran_chargement.png")
        self.loadingImage = pygame.transform.scale(self.loadingImage, (jeu.largeur, jeu.hauteur))
        self.logos = pygame.image.load("game/assets/gui/logos.png")
        self.logos = pygame.transform.scale(self.logos, (jeu.largeur, jeu.hauteur))

        # Couleurs utilisées pour les boutons
        self.colorPressed = (255, 255, 255)
        self.color = (155, 139, 221)

        # Initialisation de la police pour les boutons
        self.fontBtn = "game/assets/font/Minecraft.ttf"
        self.fontSizeBtn = 30
        
        self.runLaunchMenu = True
        self.runMode1 = False
        self.runMode2 = False
        self.returnToMenu = False

    def playMusic(self, path):
        pygame.mixer.music.load(path)  # Charge le fichier musical
        pygame.mixer.music.set_volume(0.03)  # Définit le volume (entre 0.0 et 1.0)
        pygame.mixer.music.play(-1)  # Joue en boucle infinie (-1)

    def stopMusic(self):
        pygame.mixer.music.stop()

    def showLoading(self):
        self.screen.blit(self.loadingImage, (0, 0))
        pygame.display.flip()
        pygame.time.wait(1000)

    def launchMenu(self):
        # Création et positionnement des boutons du menu principal
        jouerBtn = Bouton(self.jeu.largeur // 2, self.jeu.hauteur // 2 - 60, "Jouer", self.fontBtn, self.fontSizeBtn, self.color)
        paramBtn = Bouton(self.jeu.largeur // 2, self.jeu.hauteur // 2, "Parametres", self.fontBtn, self.fontSizeBtn, self.color)
        creditsBtn = Bouton(self.jeu.largeur // 2, self.jeu.hauteur // 2 + 60, "Credits", self.fontBtn, self.fontSizeBtn, self.color)
        classBtn = Bouton(self.jeu.largeur // 2, self.jeu.hauteur // 2 + 120, "Classements", self.fontBtn, self.fontSizeBtn, self.color)
        buttons = [jouerBtn, paramBtn, creditsBtn, classBtn]

        self.showLoading()

        running = True
        while running:
            posSouris = pygame.mouse.get_pos()
            self.screen.fill(self.back_color)
            self.screen.blit(self.logos, (0, -30))
            for btn in buttons:
                btn.update(self.screen, posSouris, self.colorPressed, self.color)

            pygame.display.flip()

            if not self.runLaunchMenu:
                break  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0].boutonHover(posSouris):
                        self.menuJouer()     

    def menuJouer(self):
        
        reflexBtn = Bouton(self.jeu.largeur // 2, self.jeu.hauteur // 2, "Reflex Mode", self.fontBtn, self.fontSizeBtn, self.color)
        chillBtn = Bouton(self.jeu.largeur // 2, self.jeu.hauteur // 2 - 60, "Chill Mode", self.fontBtn, self.fontSizeBtn, self.color)
        retourBtn = Bouton(self.jeu.largeur // 2, self.jeu.hauteur // 2 + 60, "Retour", self.fontBtn, self.fontSizeBtn, self.color)
        
        buttons = [retourBtn, chillBtn, reflexBtn]
        
        running = True
        while running:
            posSouris = pygame.mouse.get_pos()
            self.screen.fill(self.back_color)
            self.screen.blit(self.logos, (0, -30))
            for btn in buttons:
                btn.update(self.screen, posSouris, self.colorPressed, self.color)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # Pour la télécommande
                if self.runMode1:
                    self.gameScore = 0
                    self.gameScore = self.jeu.jouer()
                    self.runMode1 = False
                    running = False

                ####
                elif self.returnToMenu:
                    running = False
                    self.runLaunchMenu = True
                    self.runMode1 = False
                    self.returnToMenu = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if chillBtn.boutonHover(posSouris) :
                        self.showLoading()
                        self.stopMusic()
                        self.jeu.jouer()
                    elif retourBtn.boutonHover(posSouris):
                        running = False
                        
