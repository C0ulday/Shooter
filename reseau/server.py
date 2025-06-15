import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
        self.menu = menu.Menu(self.game)  # Instance du menu  
        self.running = True
        self.gameScore = 0
        self.leaderboard = None
        print("Serveur en attente de connexion...")

    def start(self):
        try:
            # Démarrer le serveur Flask/Web dans un thread
            flaskThread = threading.Thread(target=self.runFlask, daemon=True)
            flaskThread.start()

            # Démarrer le jeu dans thread principal
            #self.runGame()

            while True:
                # Accepte une connexion entrante
                connexion, adresse = self.serverSocket.accept()
                print(f"Connexion établie avec : {adresse}")
                self.clients += 1

                if self.clients == 1:
                    clientThread = threading.Thread(target=self.handleClient, args=(connexion,), daemon=True)
                    clientThread.start()
                else:
                    spectatorThread = threading.Thread(target=self.handleSpectator, args=(connexion,), daemon=True)
                    spectatorThread.start()

        except socket.error as e:
            print(f"Erreur socket : {e}")

        finally:
            print("Fermeture des connexions...")
            self.serverSocket.close()

    def handleClient(self, connexion):
        try:
            while True:
                data = connexion.recv(1024).decode("utf-8")
                if data == "Send game":
                    self.sendData(connexion, self.game)
                elif data == "miss":
                    print("Shot missed the target ...")
                elif data == "hit":
                    print("Shot hit the target ...")

        except socket.error as e:
            print(f"Erreur socket : {e}")

        finally:
            print("Fermeture de la connexion client...")
            connexion.close()

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
                self.menu.runLaunchMenu = True
            else :
                print("Le menu n'est pas initialisé.")


        @socketio.on("getleaderboard")
        def handle_getleaderboard():
            print("Classement !")
   
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT users.name, scores.score, profiles.bio, profiles.avatar_url
                FROM scores
                JOIN users ON users.id = scores.user_id
                JOIN profiles ON profiles.user_id = users.id
                ORDER BY scores.score DESC
                LIMIT 10
            """)
            self.leaderboard = cursor.fetchall()
            print(self.leaderboard)
            cursor.close()
            conn.close()

            self.menu.classementMenu = True

        @socketio.on("returnFromClassement")
        def handle_returnFromClassement():
            print("Retour au menu principal !")
            if self.menu:
                self.menu.classementMenu = False
            else :
                print("Le menu n'est pas initialisé.")


        socketio.run(app, host=self.Ip_adress, port=8000, debug=False, use_reloader=False)

    def runGame(self):
        print(serveur.currentUser)
        self.menu.showLoading()
        while self.running:
            if self.menu.runLaunchMenu:
                if self.menu.classementMenu:
                    self.menu.shwoClassement(self.leaderboard)
                else :
                    self.menu.launchMenu()

            else:
                self.menu.menuJouer()
                if self.menu.runMode1:
                    self.gameScore = self.menu.jeu.jouer()
                    self.menu.runMode1 = False
                    self.gameScore = 0
                    self.addScore_database(self.gameScore)
                    socketio.emit("returnToMenuButton")
                    self.menu.runLaunchMenu = True

    def addScore_database(self, score):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        INSERT INTO scores (user_id, score)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
        score = IF(VALUES(score) > score, VALUES(score), score)
        """, (serveur.currentUser, score))
        conn.commit()
        cursor.close()
        conn.close()
        
    def sendData(self, connexion, data):
        game = pkl.dumps(data)
        size_prefix = struct.pack("I", len(game)) 
        connexion.sendall(size_prefix + game)  
        print(f"Envoi du jeu au client...")

# Route Flask pour la page web
# @app.route("/")
# def home():
#     return render_template("app.html")


#----------------------------------


# Page d'accueil
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# Inscription (Signup)
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        bio = request.form.get("bio", "Aucune description")
        avatar_url = request.form.get("avatar_url", "static/images/default-avatar.png")

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
            flash("Connexion réussie.", "success")
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

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT bio, avatar_url FROM profiles WHERE user_id = %s", (session["user_id"],))
    profile = cursor.fetchone()

    cursor.execute("""
        SELECT users.id, users.name, profiles.bio, profiles.avatar_url 
        FROM users 
        JOIN profiles ON users.id = profiles.user_id
    """)
    profiles = cursor.fetchall()

    cursor.close()
    conn.close()

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

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT bio, avatar_url FROM profiles WHERE user_id = %s", (session["user_id"],))
    profile = cursor.fetchone()

    cursor.execute("""
        SELECT users.id, users.name, profiles.bio, profiles.avatar_url 
        FROM users 
        JOIN profiles ON users.id = profiles.user_id
    """)
    profiles = cursor.fetchall()

    cursor.close()
    conn.close()

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


# Lancer le serveur
if __name__ == "__main__":
    serveur = Server()

    # Lancer Flask dans un thread secondaire
    flaskThread = threading.Thread(target=serveur.runFlask, daemon=True)
    flaskThread.start()

    
    # Configuration de la session
    app.secret_key = "supersecretkey"
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Initialisation automatique de la base de données
    initialize_database()

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

    # Lancer le jeu dans le thread principal
    serveur.runGame()

