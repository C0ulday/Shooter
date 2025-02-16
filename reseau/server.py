import socket
<<<<<<< HEAD
import pickle
=======
import pygame
import struct
import threading
import pickle as pkl
>>>>>>> 21c25a0a24c2cc29bee30c41d641ce69a698ec1e
from game import jeu  


class server:
    def __init__(self):
        self.Ip_adress = 'localhost'
        self.Port = 4000
<<<<<<< HEAD
        self.server()
    
def server():
    # Création d'un socket
    serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Association du socket à l'adresse locale et au port 4000
    serveur_socket.bind(("", 4000))

    serveur_socket.listen(1)
    print("Serveur en attente de connexion...")

    try:
        # Accepte une connexion entrante
        connexion, adresse = serveur_socket.accept()
        print(f"Connexion établie avec : {adresse}")

        while True:
            try:
                data = connexion.recv(1024)
                if not data:
                    print("Aucune donnée reçue. Fermeture de la connexion.")
                    break  # Sort de la boucle si aucune donnée n'est reçue

                received_object = pickle.loads(data)  # Désérialisation
                
                # Vérification du type
                if isinstance(received_object, jeu.Jeu):
                    print(f"Objet reçu !")
                else:
                    print("Erreur : l'objet reçu n'est pas une instance de Jeu.")

            except pickle.UnpicklingError:
                print("Erreur lors de la désérialisation des données.")
            except socket.error as e:
                print(f"Erreur socket pendant la réception des données : {e}")
                break 

    except socket.error as e:
        print(f"Erreur socket : {e}")

    finally:
        print("Fermeture des connexions...")
        connexion.close()
        serveur_socket.close()

def sendObject(connexion, message):
    # Envoyer un message ou un object au client
    connexion.sendall(message.encode("utf-8"))
    print(f"Message envoyer au client : {message}\n")
    
def receiveObjct(connexion) :
    # Réception du message du client
    message_client = connexion.recv(1024).decode("utf-8")
    print(f"Message reçu du client : {message_client}")
    return message_client

if __name__ == "__main__":
    serveur = server()
=======
        self.clients = 0
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.Ip_adress, self.Port))
        self.serverSocket.listen(5)  # Connections multiples (spectateurs) 
        print("Serveur en attente de connexion...")
        
    
    def server(self):
        try:
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

    def runGame(self):
        pygame.init()
        self.game = jeu.Jeu()
        self.game.jouer()

    def sendData(self, connexion, data):
        game = pkl.dumps(data)
        # Send size + actual data
        size_prefix = struct.pack("I", len(game)) 
        connexion.sendall(size_prefix + game)  
        print(f"Envoi du jeu au client...")


if __name__ == "__main__":
    serveur = server()
    serveur.server()
>>>>>>> 21c25a0a24c2cc29bee30c41d641ce69a698ec1e
