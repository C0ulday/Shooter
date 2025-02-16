import socket
import time
import struct
import RPi.GPIO as GPIO 
import pickle as pkl
from game import jeu

class Client:
    def __init__(self, ip_adress="localhost", port=4000, pin=13, mode=1): # pin, ip adress et mode à changer
        self.ip_adress = ip_adress
        self.port = port
        self.pin = pin
        self.mode = mode

        # Configuration du GPIO
        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  

    def client(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.ip_adress, self.port))
            while True:
                print("En attente d'un appui sur le bouton...")

                if GPIO.input(self.pin) == GPIO.HIGH:
                    print("Bouton pressé ! Envoi du message...")
                    message = "Send game"
                    self.sendMessage(message)
                    message =  self.receiveData()
                    if (message == "error"):
                        print("Erreur dans Désérialisation...")
                        break

                    # dire au serveur si c'est un hit ou miss
                    self.sendMessage(message) 
                    time.sleep(0.5)  # éviter les répétitions involontaires
                    break

        except socket.error as e:
            print(f"Erreur socket : {e}")

        finally:
            self.client_socket.close()
            GPIO.cleanup() 

    def sendMessage(self, message):
        self.client_socket.sendall(message.encode("utf-8"))
        print(f"Message envoyé: {message}")

    def receiveData(self):
        # receive the size of the object that we should receive (4 bytes)
        size_data = self.client_socket.recv(4)
        if not size_data:
            return "error"

        expected_size = struct.unpack("I", size_data)[0]  # "I" format means unsigned integer
        data = b""
        
        # loop to receive all data
        while len(data) < expected_size:
            packet = self.client_socket.recv(4096)
            if not packet:
                break
            data += packet

        try:
            game = pkl.loads(data)  # Désérialisation
            hit = False
            if isinstance(game, jeu.Jeu):
                print("Using method 2 to determine if it's a hit or not...")
                # TODO : traitement d'image mode 2, changement de valeur de hit
            else:
                print("Using method 1 to determine if it's a hit or not...")
                # TODO : traitement d'image mode 1, changement de valeur de hit
            return "hit" if hit else "miss"
        
        except Exception as e:
            print(f"Erreur de désérialisation : {e}")
            return "error"  # Default return
        
        
if __name__ == "__main__":
    client = Client()  
    client.client()
