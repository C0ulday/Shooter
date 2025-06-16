from database.db_config import get_db_connection
import bcrypt

class User:
    """Classe représentant un utilisateur."""
    
    def __init__(self, id, name, email, password_hash, role="user"):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role

    @staticmethod
    def get_all_users():
        """Récupère tous les utilisateurs."""
        conn = get_db_connection()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id, name, email, role FROM users")
            users = cursor.fetchall()
        conn.close()
        return users

    @staticmethod
    def add_user(name, email, password_hash, role="user"):
        """Ajoute un nouvel utilisateur."""
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                           (name, email, password_hash, role))
            conn.commit()
        conn.close()

    @staticmethod
    def register(name, email, password, bio="Aucune description", avatar_url="static/images/default-avatar.png", role="user"):
        """Crée un utilisateur avec son profil."""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Vérifie si l'utilisateur existe déjà
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False  # Inscription échouée (email déjà utilisé)

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")

        # Création utilisateur
        cursor.execute("INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                    (name, email, password_hash, role))
        conn.commit()
        user_id = cursor.lastrowid

        # Création du profil
        cursor.execute("INSERT INTO profiles (user_id, bio, avatar_url) VALUES (%s, %s, %s)",
                    (user_id, bio, avatar_url))
        conn.commit()

        cursor.close()
        conn.close()
        return True  # Inscription réussie

    @staticmethod
    def delete_user(user_id):
        """Supprimer un utilisateur"""
        conn = get_db_connection()
        cursor = conn.cursor()

        try: 
            cursor.execute("DELETE FROM profiles WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            print(f"Utilisateur {user_id} supprimé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la suppression de l'utilisateur {user_id}: {e}")
        finally:
            cursor.close()
            conn.close()

    
            
