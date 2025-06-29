
# ESI-SHOOT : Stand de tir connecté

> Projet multidisciplinaire – PX457  
> Auteurs : Ismail El Youssefi, Mahmoud Bouchelaghem, Dario Gomez Baquerizo, Kagnon Coulibaly

---

## Présentation

ESI-SHOOT est un stand de tir connecté qui combine **jeu interactif**, **traitement d’image en temps réel**, et **architecture client-serveur**. L’objectif : viser des cibles animées affichées à l’écran à l’aide d’un pistolet connecté équipé d’une caméra, et déterminer si un tir est réussi ou non par analyse d’image.

---

## Architecture du projet

### 1. Jeu (Pygame)
- Affichage des cibles (aigle, gator, pato, grenouille)
- Deux modes : Chill Mode (facile) et Reflex Mode (plus rapide)
- Gestion des scores, animations, viseur et temps

Fichier principal : `jeu.py`

### 2. Interface (Menu)
- Menu de navigation avec options : Jouer, Paramètres, Crédits, Classement
- Lancement des modes de jeu
- Intégration graphique et sonore

Fichier principal : `menu.py`

### 3. Client (Raspberry Pi)
- Gère un bouton physique et la caméra
- Analyse d'image avec OpenCV via `matching.py`
- Envoie les résultats (`hit` ou `miss`) au serveur via TCP

Fichier principal : `client.py`

### 4. Traitement d’image
- Détection de la cible à partir d’une image de référence
- Masquage couleur + comparaison de formes avec `cv2.matchShapes`
- Vérifie également le centrage de la cible dans l’image

Fichier : `matching.py`

### 5. Serveur Web & Jeu
- Serveur Flask avec SocketIO
- Affichage du jeu (Pygame)
- Gestion des utilisateurs, scores et sessions
- Communication avec le client Raspberry via TCP

Fichier principal : `server.py`

---

## Organisation des fichiers

```
game/
 ├── assets/         # Ressources graphiques et sonores
 ├── jeu.py          # Moteur de jeu Pygame
 ├── monstre.py      # Classe des monstres animés
 ├── menu.py         # Menu principal
 └── ...
database/
 ├── models/         # Modèles utilisateurs (User)
 ├── db_config.py    # Connexion DB MySQL
 └── init_db.py      # Initialisation
server.py          # Serveur Flask + Pygame
client.py          # Client Raspberry Pi (caméra + bouton)
matching.py        # Analyse d'image via OpenCV
```

---

## Lancement du projet

### Prérequis
- Python 3.8+
- MySQL Server
- Raspberry Pi avec caméra et bouton physique
- Bibliothèques Python : `pygame`, `opencv-python`, `flask`, `flask-socketio`, `RPi.GPIO`, etc.

### Lancer le jeu
```bash
python -m game.server
```

### Côté Raspberry Pi
```bash
python client.py
```

---

## Fonctionnalités clés

- Analyse d’image en temps réel
- Viseur contrôlé à la souris
- Communication client-serveur (TCP + WebSocket)
- Système de classement des joueurs
- Authentification et avatars
- Détection de contour + centrage de cible

---

## Limitations et améliorations possibles

- Spectateurs non encore implémentés
- Aucun système de calibration automatisée
- IA de reconnaissance non intégrée (trop complexe pour le besoin)

---

## Documentation

Un rapport détaillé est disponible dans le fichier :  
`Rapport PX457.pdf`

---

## Aperçus

| Menu principal | Gameplay | Classement |
| -------------- | -------- | ---------- |
| ![menu](game/assets/gui/logos.png) | ![pato](game/assets/mode1/sprites/pato.png) | _Capture dynamique depuis le jeu_ |

---
