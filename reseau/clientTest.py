import socket
import json
import keyboard

class Client:
    def __init__(self, ip_adress="172.20.10.3", port=4000, pin=13): 
        self.ip_adress = ip_adress
        self.port = port
        self.pin = pin
        self.client_socket = None

        self.connect_to_server()

        try:
            while True:
                self.button_pressed()

        except KeyboardInterrupt:
            print("Fermeture du client.")
            
        finally:
            if self.client_socket:
                self.client_socket.close()

    def button_pressed(self): 
        if keyboard.is_pressed('a'):
            print("hit")
            self.sendMessage("hit")
            while keyboard.is_pressed('a'):
                pass 
        elif keyboard.is_pressed('z'):
            print("miss")
            self.sendMessage("miss")
            while keyboard.is_pressed('z'):
                pass

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.ip_adress, self.port))
            print("Connecté au serveur. En attente d un appui clavier...")
        except socket.error as e:
            print(f"Erreur socket : {e}")
            self.client_socket = None 

    def sendMessage(self, message):
        if self.client_socket:
            payload = {"message": message}
            try:
                self.client_socket.sendall(json.dumps(payload).encode("utf-8"))
            except socket.error as e:
                print(f"Erreur d envoi : {e}")
        else:
            print("Socket non connectée.")

# Lancer le client
if __name__ == "__main__":
    client = Client()
