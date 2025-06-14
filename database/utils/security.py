import bcrypt

def hash_password(password):
    """Hash un mot de passe avec bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
