import hashlib
from src.persistencia import cargar_datos, FICHERO_USUARIOS

def hash_password(password):
    """Convierte la contraseña en un hash SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def validar_usuario(username, password):
    """
    Comprueba si el usuario existe y si la contraseña coincide.
    Retorna el diccionario del usuario si es correcto, o None si falla.
    """
    usuarios = cargar_datos(FICHERO_USUARIOS)
    
    # Hasheamos la contraseña que introduce el usuario
    password_encrip = hash_password(password)
    
    for u in usuarios:
        if u['username'] == username and u['password'] == password_encrip:
            return u  # Login exitosos
            
    return None # Login fallido

