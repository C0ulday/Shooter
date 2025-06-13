import socket
import pygame
import struct
import threading
import pickle as pkl
from game import jeu  
from game import menu
from flask import Flask, render_template
from flask_socketio import SocketIO

# Initialisation du serveur Flask
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class Server:
    def __init__(self):
        self.Ip_adress = "localhost"  # À changer avec la vraie adresse IP
        self.Port = 4000
        self.clients = 0
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.Ip_adress, self.Port))
        self.serverSocket.listen(5)  # Connexions multiples (spectateurs)
        self.game = jeu.Jeu()  # Instance du jeu
        self.menu = menu.Menu(self.game)  # Instance du menu  
        
        print("Serveur en attente de connexion...")

    def start(self):
        try:
            # Démarrer le serveur Flask/Web dans un thread
            flaskThread = threading.Thread(target=self.runFlask, daemon=True)
            flaskThread.start()

            # Démarrer le jeu dans thread principal
            #self.runGame()


            while True:
                # Accepte une connexion entrante
                connexion, adresse = self.serverSocket.accept()
                print(f"Connexion établie avec : {adresse}")
                self.clients += 1

                if self.clients == 1:
                    clientThread = threading.Thread(target=self.handleClient, args=(connexion,), daemon=True)
                    clientThread.start()
                else:
                    spectatorThread = threading.Thread(target=self.handleSpectator, args=(connexion,), daemon=True)
                    spectatorThread.start()

        except socket.error as e:
            print(f"Erreur socket : {e}")

        finally:
            print("Fermeture des connexions...")
            self.serverSocket.close()

    def handleClient(self, connexion):
        try:
            while True:
                data = connexion.recv(1024).decode("utf-8")
                if data == "Send game":
                    self.sendData(connexion, self.game)
                elif data == "miss":
                    print("Shot missed the target ...")
                elif data == "hit":
                    print("Shot hit the target ...")

        except socket.error as e:
            print(f"Erreur socket : {e}")

        finally:
            print("Fermeture de la connexion client...")
            connexion.close()

    def handleSpectator(self, connexion):
        try:
            print("Connexion d'un spectateur...")

        except socket.error as e:
            print(f"Erreur socket : {e}")

        finally:
            print("Fermeture de la connexion spectateur...")
            connexion.close()

    def runFlask(self):
        @socketio.on("startGame")
        def handle_startGame():
            print("Le jeu a été lancé !")
            if self.menu:
                self.menu.runLaunchMenu = False
            else :
                print("Le menu n'est pas initialisé.")
        @socketio.on("startMode1")
        def handle_startMode1():
            print("Mode Chill lancé !")
            if self.menu:
                self.menu.runMode1 = True
            else :
                print("Le menu n'est pas initialisé.")
        @socketio.on("returnToMenu")
        def handle_returnToMenu():
            print("Retour au menu principal !")
            if self.menu:
                self.menu.returnToMenu = True
            else :
                print("Le menu n'est pas initialisé.")
        @socketio.on("pauseGame")
        def handle_pauseGame():
            print("Jeu en pause !")
            if self.menu:
                self.menu.jeu.pause = True
            else :
                print("Le menu n'est pas initialisé.")
        
        @socketio.on("reprendreGame")
        def handle_reprendreGame():
            print("Jeu reprend !")
            if self.menu:
                self.menu.jeu.pause = False
            else :
                print("Le menu n'est pas initialisé.")

        socketio.run(app, host=self.Ip_adress, port=8000, debug=False, use_reloader=False)

    def runGame(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if self.menu.runLaunchMenu:
                self.menu.launchMenu()
            if self.menu.runMode1:
                print("coucou")
                self.menu.jeu.jouer()
            if self.menu.returnToMenu:
                self.menu.runLaunchMenu = True
                self.menu.runMode1 = False
                self.menu.returnToMenu = False
            else:
                self.menu.menuJouer()
            clock.tick(60)  # limite à 60 FPS


    def sendData(self, connexion, data):
        game = pkl.dumps(data)
        size_prefix = struct.pack("I", len(game)) 
        connexion.sendall(size_prefix + game)  
        print(f"Envoi du jeu au client...")

# Route Flask pour la page web
@app.route("/")
def home():
    return render_template("app.html")

# Lancer le serveur
if __name__ == "__main__":
    serveur = Server()

    # Lancer Flask dans un thread secondaire
    flaskThread = threading.Thread(target=serveur.runFlask, daemon=True)
    flaskThread.start()

    # Lancer la boucle réseau dans un thread secondaire
    def handle_connections():
        try:
            while True:
                connexion, adresse = serveur.serverSocket.accept()
                print(f"Connexion établie avec : {adresse}")
                serveur.clients += 1

                if serveur.clients == 1:
                    clientThread = threading.Thread(target=serveur.handleClient, args=(connexion,), daemon=True)
                    clientThread.start()
                else:
                    spectatorThread = threading.Thread(target=serveur.handleSpectator, args=(connexion,), daemon=True)
                    spectatorThread.start()
        except socket.error as e:
            print(f"Erreur socket : {e}")
        finally:
            print("Fermeture des connexions réseau...")
            serveur.serverSocket.close()

    connectionThread = threading.Thread(target=handle_connections, daemon=True)
    connectionThread.start()

    # Lancer le jeu dans le thread principal
    serveur.runGame()

