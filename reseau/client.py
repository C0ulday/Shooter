import socket
import os
import sys
import RPi.GPIO as GPIO 
import time
from matching import Matching

class Client:
    def __init__(self, ip_adress="localhost", port=4000, pin=13): 
        self.cam = Matching()
        self.ip_adress = ip_adress
        self.port = port
        self.pin = pin

        # Configuration du GPIO
        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  

        # Ajout d'un événement sur le bouton
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.button_pressed, bouncetime=300)

        try:
            while True:
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("Arrêt du client")

        finally:
            GPIO.cleanup()

    def button_pressed(self, channel): 
        print("Bouton pressed !")
        self.cam.matching_check()
        print(f'Resultat de l analyse est {self.cam.resultat}')

    def client(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.ip_adress, self.port))
            print("En attente d'un appui sur le bouton...")
            while True:
                pass

        except socket.error as e:
            print(f"Erreur socket : {e}")

        finally:
            self.client_socket.close()
            GPIO.cleanup() 
            print("Nettoyage terminé.")

    def sendMessage(self, message):
        self.client_socket.sendall(message.encode("utf-8"))
        print(f"Message envoyé: {message}")


if __name__ == "__main__":
    client = Client()  
