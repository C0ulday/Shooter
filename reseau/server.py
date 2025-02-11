import socket
import pickle
from ..Jeu import jeu 

class server:
    def __init__(self):
        self.Ip_adress = 'localhost'
        self.Port = 4000
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
                if isinstance(received_object, Jeu):
                    print(f"Objet reçu : Nom = {received_object.name}, Âge = {received_object.age}")
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
