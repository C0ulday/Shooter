import socket
import pygame
import struct
import threading
import pickle as pkl
from game import jeu  
from flask import Flask, render_template
from flask_socketio import SocketIO

# Initialisation du serveur Flask
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class server:
    def __init__(self):
        self.Ip_adress = "localhost"   # iL faut le changer avec la vrai adresse ip
        self.Port = 4000
        self.clients = 0
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.Ip_adress, self.Port))
        self.serverSocket.listen(5)  # Connections multiples (spectateurs) 
        print("Serveur en attente de connexion...")
        
    def server(self):

        try:
            # Démarrer le serveur Flask/Web dans un thread
            flaskThread = threading.Thread(target=self.runFlask, daemon=True)
            flaskThread.start()

            # Start game in a separate thread
            gameThread = threading.Thread(target=self.runGame, daemon=True)
            gameThread.start()

            while True:
                # Accepte une connexion entrante
                connexion, adresse = self.serverSocket.accept()
                print(f"Connexion établie avec : {adresse}")
                self.clients += 1

                # Handle client
                if (self.clients == 0):
                    clientThread = threading.Thread(target=self.handleClient, args=(connexion, adresse), daemon=True)
                    clientThread.start()

                # Handle spectators
                elif (self.clients > 0):
                    spectatorThread = threading.Thread(target=self.handleSpectator, args=(connexion, adresse), daemon=True)
                    spectatorThread.start()

        except socket.error as e:
            print(f"Erreur socket : {e}")

        finally:
            print("Fermeture des connexions...")
            connexion.close()
            self.serverSocket.close() 

    def handleClient(self,connexion,adresse):
        try:
            while True:
                data = connexion.recv(1024).decode("utf-8")
                if (data == "Send game"):
                    self.sendData(connexion, self.game)

                elif (data == "miss"):
                    print("Shot missed the target ...")
                    #TODO

                elif (data == "hit"):
                    print("Shot hit the target ...")
                    #TODO

        except socket.error as e:
            print(f"Erreur socket : {e}")

        finally:
            print("Fermeture de la connexion...")
            connexion.close()

    def handleSpectator(self,connexion,adresse):
        try:
            #TODO
            print("")

        except socket.error as e:
            print(f"Erreur socket : {e}")

        finally:
            print("Fermeture des connexions...")
            connexion.close()

    def runFlask(self):
        """ Lance le serveur Flask avec WebSockets. """
        socketio.run(app, host=self.Ip_adress, port=5000, debug=False, use_reloader=False)

    def runGame(self):
        pygame.init()
        self.game = jeu.Jeu()
        self.game.menu()

    def sendData(self, connexion, data):
        game = pkl.dumps(data)
        # Send size + actual data
        size_prefix = struct.pack("I", len(game)) 
        connexion.sendall(size_prefix + game)  
        print(f"Envoi du jeu au client...")

    @app.route("/")
    def home():
        return render_template("app.html")
    
if __name__ == "__main__":
    serveur = server()
    serveur.server()
