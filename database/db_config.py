import mysql.connector
import os

def get_db_connection():
    """Établit une connexion à la base de données MySQL."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "")
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return None
