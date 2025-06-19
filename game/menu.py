import pygame
from game.jeu import Jeu
from game.bouton import Bouton

class Menu:
    def __init__(self):
    
        self.back_color = (98, 53, 138)
        self.run_display = True
        
        # Matériels affichage
        info = pygame.display.Info()
        self.largeur = info.current_w
        self.hauteur = info.current_h - 10
        
        # Initialisation de l'écran principal
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur), pygame.RESIZABLE)
        pygame.display.set_caption("Esi-SHOOT")

        # Surface optionnelle pour le menu (si vous souhaitez dessiner séparément)
        self.menu_surface = pygame.Surface((self.largeur, self.hauteur))

        # Chemin vers la musique et chargement des images
        self.musicPath = "game/assets/sounds/luv.wav"
        self.loadingImage = pygame.image.load("game/assets/gui/ecran_chargement.png")
        self.loadingImage = pygame.transform.scale(self.loadingImage, (self.largeur, self.hauteur))
        self.logos = pygame.image.load("game/assets/gui/logos.png")
        self.logos = pygame.transform.scale(self.logos, (self.largeur, self.hauteur))

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
        self.classementMenu = False


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
        jouerBtn = Bouton(self.largeur // 2, self.hauteur // 2 - 60, "Jouer", self.fontBtn, self.fontSizeBtn, self.color)
        paramBtn = Bouton(self.largeur // 2, self.hauteur // 2, "Parametres", self.fontBtn, self.fontSizeBtn, self.color)
        creditsBtn = Bouton(self.largeur // 2, self.hauteur // 2 + 60, "Credits", self.fontBtn, self.fontSizeBtn, self.color)
        classBtn = Bouton(self.largeur // 2, self.hauteur // 2 + 120, "Classements", self.fontBtn, self.fontSizeBtn, self.color)
        buttons = [jouerBtn, paramBtn, creditsBtn, classBtn]

        posSouris = pygame.mouse.get_pos()
        self.screen.fill(self.back_color)
        self.screen.blit(self.logos, (0, -30))
        for btn in buttons:
            btn.update(self.screen, posSouris, self.colorPressed, self.color)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].boutonHover(posSouris):
                    self.menuJouer() 

    def showClassement(self, classement):

        self.screen.fill(self.back_color)
        self.screen.blit(self.logos, (0, -30))
        
        title_font = pygame.font.SysFont("Arial", 36)
        font = pygame.font.SysFont("Arial", 24)

        # Titre
        titre = title_font.render("Classement Top 10", True, (255, 255, 0))
        self.screen.blit(titre, (self.largeur // 2 - titre.get_width() // 2, 40))
        x = self.largeur // 2
        
        # En-têtes
        headers = ["Nom", "Score", "Bio"]
        x_positions = [x - 500, x-300 , x + 100]
        
        for i, head in enumerate(headers):
            header_text = font.render(head, True, (0, 200, 255))
            self.screen.blit(header_text, (x_positions[i], 100))

        # Données du classement
        y = 140
        for joueur in classement:
            name = font.render(joueur['name'], True, (255, 255, 255))
            score = font.render(str(joueur['score']), True, (255, 255, 255))
            bio = font.render(joueur['bio'] or "-", True, (200, 200, 200))

            self.screen.blit(name, (x_positions[0], y))
            self.screen.blit(score, (x_positions[1], y))
            self.screen.blit(bio, (x_positions[2], y))

            y += 40
        # Bouton retour
        retourBtn = Bouton(self.largeur // 2, y + 60, "Retour", self.fontBtn, self.fontSizeBtn, self.color)
        
        posSouris = pygame.mouse.get_pos()
        retourBtn.update(self.screen, posSouris, self.colorPressed, self.color)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def menuJouer(self):
        
        reflexBtn = Bouton(self.largeur // 2, self.hauteur // 2, "Reflex Mode", self.fontBtn, self.fontSizeBtn, self.color)
        chillBtn = Bouton(self.largeur // 2, self.hauteur // 2 - 60, "Chill Mode", self.fontBtn, self.fontSizeBtn, self.color)
        retourBtn = Bouton(self.largeur // 2, self.hauteur // 2 + 60, "Retour", self.fontBtn, self.fontSizeBtn, self.color)
        
        buttons = [retourBtn, chillBtn, reflexBtn]
        
        self.screen.fill(self.back_color)
        self.screen.blit(self.logos, (0, -30))
        posSouris = pygame.mouse.get_pos()
        self.playMusic(self.musicPath)
        
        for btn in buttons:
            btn.update(self.screen, posSouris, self.colorPressed, self.color)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if chillBtn.boutonHover(posSouris) :
                    self.showLoading()
                    self.stopMusic()
                    Jeu.jouer()
                    self.runLaunchMenu = True
                elif retourBtn.boutonHover(posSouris):
                    self.returnToMenu = False
                    self.runLaunchMenu = True 
                        
