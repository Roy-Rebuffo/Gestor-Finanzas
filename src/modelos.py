import uuid
from datetime import datetime

CATEGORIAS_GASTO = ["Comida", "Transporte", "Ocio", "Salud", "Suscripciones"]
CATEGORIAS_INGRESO = ["Nomina", "Venta", "Regalo", "Otros"]

def crear_transaccion(concepto, cantidad, categoria, fecha=None):
    "Función para crear una transacción."
    "Retorna un diccionario con la estructura"

    return {
        "id": str(uuid.uuid4())[:8],
        "concepto": concepto,
        "cantidad": float(cantidad),
        "categoria": categoria,
        "fecha": fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
def crear_usuario(username, password_hash, email, moneda = "EUR"):
    "Crea el diccionario para el login"
    return{
        "username":username,
        "password": password_hash,
        "email": email,
        "config":{
            "moneda": moneda,
            "presupuesto_limite": 0.0
        }
    }
