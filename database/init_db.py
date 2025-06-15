import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import bcrypt
from database.models.user import User

from database.db_config import get_db_connection
import mysql.connector


def create_database():
    """Crée la base de données si elle n'existe pas."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "")
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS PX")
        print("Base de données vérifiée et créée si manquante.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f" Erreur MySQL : {err}")

def create_tables():
    """Vérifie et crée les tables si elles n'existent pas."""
    conn = get_db_connection()
    if conn is None:
        print(" Impossible de se connecter à la base de données")
        return

    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL UNIQUE,
                bio TEXT,
                avatar_url VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL UNIQUE,
                score INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

    conn.commit()
    conn.close()
    print("Tables vérifiées et créées.")

def initialize_database():
    """Initialise la base de données et crée les tables."""
    create_database()
    create_tables()
    # time.sleep(1)
    name = "Admin"
    email = "admin@example.com"
    password = "admin123"
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    existing_admin = cursor.fetchone()

    if existing_admin:
        print("Admin déjà existant, aucune action nécessaire.")
    else:
        User.add_user(name, email, password_hash, role="admin")
        print("Admin créé avec succès.")

  

if __name__ == "__main__":
    initialize_database()
