import socket
import RPi.GPIO as GPIO
import time
import struct

class Client:
    def __init__(self, ip_adress="localhost", port=4000, pin=13): # pin et ip adress à changer
        self.ip_adress = ip_adress
        self.port = port
        self.pin = pin

        # Configuration du GPIO
        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  

    def client(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.ip_adress, self.port))
            while True:
                """Surveille le bouton et envoie un message lorsqu'il est pressé"""
                print("En attente d'un appui sur le bouton...")
                if GPIO.input(self.pin) == GPIO.HIGH:
                    print("Bouton pressé ! Envoi du message...")
                    message = "Send game"
                    self.sendMessage()
                    x_cible,y_cible = self.receiveData()
                    # TODO : traitement d'image
                    if True:
                        message = "hit"
                    else:
                        message = "miss"

                    self.send_message(message)
                    time.sleep(0.5)  # éviter les répétitions involontaires
                    break

        except socket.error as e:
            print(f"Erreur socket : {e}")

        finally:
            self.client_socket.close()

    def sendMessage(self, message):
        self.client_socket.sendall(message.encode("utf-8"))
        response = self.client_socket.recv(1024).decode("utf-8")
        print(f"Réponse du serveur : {response}")

    def receiveMessage(self):
        response = self.client_socket.recv(1024).decode("utf-8")
        print(f"Réponse du serveur : {response}")
        return response

    def receiveData(self):
        data = self.client_socket.recv(1024)
        print(f"Réponse du serveur : {data}")
        x, y = struct.unpack("ii", data)
        print(f"Decoded coordinates: x={x}, y={y}")
        return x,y

if __name__ == "__main__":
    client = Client(ip_adress="")  
    client.run()
