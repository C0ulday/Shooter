from database.db_config import get_db_connection
from models.user import User 
import bcrypt

class Admin(User):
    """Classe représentant un administrateur, héritant de User."""
    
    def __init__(self, id, name, email, password_hash, role="admin"):
        super().__init__(id, name, email, password_hash, role)


    def update_user_role(self, user_id, new_role):
        """Met à jour le rôle d'un utilisateur."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
            conn.commit()
            print(f" Rôle de l'utilisateur {user_id} mis à jour en {new_role}.")
        except Exception as e:
            print(f" Erreur lors de la mise à jour du rôle : {e}")
        finally:
            cursor.close()
            conn.close()

    def get_all_users_with_roles(self):
        """Récupère tous les utilisateurs avec leur rôle."""
        conn = get_db_connection()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id, name, email, role FROM users")
            users = cursor.fetchall()
        conn.close()
        return users

    def reset_user_password(self, user_id, new_password_hash):
        """Réinitialise le mot de passe d'un utilisateur."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (new_password_hash, user_id))
            conn.commit()
            print(f" Mot de passe de l'utilisateur {user_id} réinitialisé avec succès.")
        except Exception as e:
            print(f" Erreur lors de la réinitialisation du mot de passe : {e}")
        finally:
            cursor.close()
            conn.close()
