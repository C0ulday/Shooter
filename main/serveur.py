# Serveur
import socket

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

    # Met le socket à l'état d'écoute
    serveur_socket.listen(1)
    print("Serveur en attente de connexion...")

    # Accepte une connexion entrante
    connexion, adresse = serveur_socket.accept()
    print(f"Connexion établie avec : {adresse}")

    # Fermeture des connexions
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
