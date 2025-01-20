import socket;

def client():
    # Création d'un socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connexion au serveur local sur le port 4000
    client_socket.connect(("localhost", 4000))

    # Envoi d'un message au serveur
    message = "Serveur es-tu là ?"
    client_socket.sendall(message.encode("utf-8"))

    # Réception de la réponse du serveur
    reponse = client_socket.recv(1024).decode("utf-8")
    print(f"Réponse du serveur : {reponse}")

    # Fermeture de la connexion
    client_socket.close()
    
if __name__ == "__main__":
    client()