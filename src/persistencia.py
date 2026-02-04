import json
import os
import csv

# Rutas
RUTA_SCRIPT = os.path.dirname(__file__)
FOLDER_OUTPUT = os.path.join(RUTA_SCRIPT, "..", "output")

# Definimos una por una para no liarla
FICHERO_USUARIOS = os.path.join(FOLDER_OUTPUT, "usuarios.json")

def guardar_datos(ruta, datos):
    """Guarda datos en la ruta absoluta especificada."""
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error al guardar en {ruta}: {e}")
        return False

def cargar_datos(ruta):
    """Carga datos desde la ruta absoluta."""
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

#Crea una ruta JSON para cada usuario
def obtener_ruta_usuario(username, tipo_fichero):
    """
    Genera una ruta tipo: output/gastos_pepito.json
    tipo_fichero puede ser 'gastos' o 'nominas'
    """
    user_clean = username.lower().strip()
    nombre_archivo = f"{tipo_fichero}_{user_clean}.json"
    return os.path.join(FOLDER_OUTPUT, nombre_archivo)
    
def exportar_a_csv(nombre_archivo_csv, lista_diccionarios):
    """Convierte la lista de diccionarios en un archivo CSV."""
    if not lista_diccionarios:
        return False
    
    try:
        # Obtenemos las cabeceras de las llaves del primer diccionario
        columnas = lista_diccionarios[0].keys()
        
        with open(nombre_archivo_csv, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(lista_diccionarios)
        return True
    except Exception as e:
        print(f"Error al exportar: {e}")
        return False