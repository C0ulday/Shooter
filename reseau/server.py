import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import requests
import socket
import pygame
import struct
import threading
import pickle as pkl
from game import jeu  
from game import menu
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO
from flask_session import Session
from database.init_db import initialize_database
from database.db_config import get_db_connection
import bcrypt
from database.models.user import User
import json

# Initialisation du serveur Flask
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class Server:
    currentUser = -1 
    def __init__(self):
        self.Ip_adress = "localhost"  # À changer avec la vraie adresse IP
        self.Port = 4000
        self.clients = 0
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.Ip_adress, self.Port))
        self.serverSocket.listen(5)  # Connexions multiples (spectateurs)
        self.game = jeu.Jeu()  # Instance du jeu
        self.menu = menu.Menu()  # Instance du menu 
        self.running = True
        self.leaderboard = None

        print("Serveur en attente de connexion...")

    def start(self):
        try:
            # Démarrer le serveur Flask/Web dans un thread
            flaskThread = threading.Thread(target=self.runFlask, daemon=True)
            flaskThread.start()

            while True:
                # Accepte une connexion entrante
                connexion, adresse = self.serverSocket.accept()
                print(f"Connexion établie avec : {adresse}")
                self.clients += 1

                if self.clients == 1:
                    clientThread = threading.Thread(target=self.handleClient, args=(connexion,), daemon=True)
                    clientThread.start()
                # else:
                #     spectatorThread = threading.Thread(target=self.handleSpectator, args=(connexion,), daemon=True)
                #     spectatorThread.start()

        except socket.error as e:
            print(f"Erreur socket : {e}")

        finally:
            print("Fermeture des connexions...")
            self.serverSocket.close()

    def handleClient(self, conn):
        try:
            buffer = ""
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                # Accumule les données au cas où plusieurs messages sont reçus en une fois
                buffer += data.decode("utf-8")

                # Essaye de parser tous les messages JSON valides dans le buffer
                while buffer:
                    try:
                        message, index = json.JSONDecoder().raw_decode(buffer)
                        buffer = buffer[index:].lstrip()  # Nettoie le buffer de ce qui a été lu
                        if message.get("message") == "hit":
                            self.game.action = "hit"
                            print("Reçu : HIT")
        
                        elif message.get("message") == "miss":
                            print("Reçu : MISS")
                        else:
                            print("Message inconnu :", message)

                    except json.JSONDecodeError:
                        # Message incomplet : attendre plus de données
                        break

        except ConnectionResetError:
            print("Client déconnecté brutalement")

        except Exception as e:
            print("Erreur inattendue :", e)

        finally:
            print("Connexion fermée")
            conn.close()


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
                
        @socketio.on("quitGame")
        def handle_quitGame():
            print("Quitter le jeu !")
            self.running = False

        @socketio.on("startMode1")
        def handle_startMode1():
            print("Mode Chill lancé !")
            print(serveur.currentUser)
            if self.menu:
                self.menu.runMode1 = True
            else :
                print("Le menu n'est pas initialisé.")

        @socketio.on("returnToMenu")
        def handle_returnToMenu():
            print("Retour au menu principal !")
            if self.menu:
                self.menu.classementMenu = False
                self.menu.runLaunchMenu = True
            else :
                print("Le menu n'est pas initialisé.")

        @socketio.on("getleaderboard")
        def handle_getleaderboard():
            print("Classement !")

            self.leaderboard = sql_select(""" SELECT users.name, scores.score, profiles.bio, profiles.avatar_url
                FROM scores
                JOIN users ON users.id = scores.user_id
                JOIN profiles ON profiles.user_id = users.id
                ORDER BY scores.score DESC
                LIMIT 10
            """)

            print(self.leaderboard)
            self.menu.classementMenu = True


        socketio.run(app, host=self.Ip_adress, port=8000, debug=False, use_reloader=False)

    def runGame(self):
        print(serveur.currentUser)
        self.menu.showLoading()
        while self.running:
            if self.menu.runLaunchMenu:
                if self.menu.classementMenu:
                    self.menu.showClassement(self.leaderboard)
                else :
                    self.menu.launchMenu()

            else:
                self.menu.menuJouer()
                if self.menu.runMode1:
                    self.game.jouer()
                    self.menu.runMode1 = False
                    sql_execute(command=""" INSERT INTO scores (user_id, score)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE
                    score = IF(VALUES(score) > score, VALUES(score), score)
                    """, params=(serveur.currentUser, (self.game.joueur.score)))
                    socketio.emit("returnToMenuButton")
                    self.menu.runLaunchMenu = True

    def sendData(self, connexion, data):
        game = pkl.dumps(data)
        size_prefix = struct.pack("I", len(game)) 
        connexion.sendall(size_prefix + game)  
        print(f"Envoi du jeu au client...")
        
#----------------------------------

# Page d'accueil
@app.route("/", methods=["GET"])
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            users.id, users.name, users.role, profiles.avatar_url, profiles.bio
        FROM users
        LEFT JOIN profiles ON users.id = profiles.user_id
    """)
    profiles = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("home.html", profiles=profiles)

@app.route("/bouton", methods=["POST"])
def clientHandler():
    if request.method == "POST":
        data = request.get_json()
        if (data['message'] == 'hit'):
            print("Received Hit from client !!!!!!")
            
        elif (data['message'] == 'miss'):
            print("Received Miss from client !!!!!!")

# Inscription (Signup)
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        bio = request.form.get("bio", "Aucune description")
        avatar_url = request.form.get("avatar_url", "static/images/default-avatar.png")
        
        if not verif_url(url= avatar_url):
            flash("L'image n'est pas correct !", "danger")
            return redirect(url_for("signup"))


        if not User.register(name, email, password, bio, avatar_url):
            flash("Cet email est déjà utilisé !", "danger")
            return redirect(url_for("signup"))

        flash("Inscription réussie ! Connectez-vous.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

# Connexion (Login)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("dashboard"))
            else:
                serveur.currentUser = user["id"]
                return redirect(url_for("jeuView"))
        else:
            flash("Email ou mot de passe incorrect.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

# Dashboard : affichage des profils (admin uniquement)
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        flash("Accès réservé aux administrateurs.", "danger")
        return redirect(url_for("home"))

    profile = sql_select(command= "SELECT bio, avatar_url FROM profiles WHERE user_id = %s", params=(session["user_id"],))
    
    profiles = sql_select(command= """ SELECT users.id, users.name, profiles.bio, profiles.avatar_url 
        FROM users 
        JOIN profiles ON users.id = profiles.user_id
    """)
    profile = profile[0] if profile else None

    return render_template(
        "dashboard.html",
        user_name=session["name"],
        bio=profile["bio"] if profile else "Aucune description ajoutée",
        avatar_url=profile["avatar_url"] if profile else "static/images/default-avatar.png",
        profiles=profiles
    )

# Vue "Jeu" (exemple de vue accessible à tous les utilisateurs connectés)
@app.route("/jeu")
def jeuView():
    if "user_id" not in session:
        return redirect(url_for("login"))

    profile = sql_select("SELECT bio, avatar_url FROM profiles WHERE user_id = %s", params=(session["user_id"],))
    print(profile)
    profiles = sql_select("""SELECT users.id, users.name, profiles.bio, profiles.avatar_url 
        FROM users 
        JOIN profiles ON users.id = profiles.user_id
    """)
    profile = profile[0] if profile else None

    return render_template(
        "app.html",
        user_name=session["name"],
        bio=profile["bio"] if profile else "Aucune description ajoutée",
        avatar_url=profile["avatar_url"] if profile else "static/images/default-avatar.png",
        profiles=profiles
    )

# Suppression d’un utilisateur (admin uniquement)
@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if "user_id" not in session:
        flash("Vous devez être connecté pour supprimer un utilisateur.", "danger")
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        flash("Accès refusé : seuls les administrateurs peuvent supprimer des utilisateurs.", "danger")
        return redirect(url_for("dashboard"))

    User.delete_user(user_id)
    flash("Utilisateur supprimé avec succès.", "success")
    return redirect(url_for("dashboard"))

# Déconnexion
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

def sql_execute(command, params = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(command, params)
        else:
            cursor.execute(command)
        
        conn.commit()
       
    finally:
        cursor.close()
        conn.close()

def sql_select(command, params=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if params:
        cursor.execute(command, params)
    else:
        cursor.execute(command)

    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def verif_url(url):

    try:
        if url == "": return True
        response = requests.head(url, allow_redirects=True, timeout=5)
        content_type = response.headers.get("Content-Type", "")

        formats_acceptes = [
            "image/png",
            "image/jpeg",
            "image/webp",
            "image/gif"
        ]

        if content_type in formats_acceptes:
            print(f"Image acceptée : {url} ({content_type})")
            return True
        else:
            print(f" Type non accepté : {content_type}")
            return False

    except requests.RequestException as e:
        print(f"Erreur réseau : {e}")
        return False

# Lancer le serveur
if __name__ == "__main__":
    serveur = Server()

    # Configuration de la session
    app.secret_key = "supersecretkey"
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Initialisation automatique de la base de données
    initialize_database()
    
    #serveur.start()
    #Lancer Flask dans un thread secondaire
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

    #Lancer le jeu dans le thread principal
    serveur.runGame()

