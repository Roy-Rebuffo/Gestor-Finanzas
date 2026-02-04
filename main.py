import os
from src.persistencia import (
    cargar_datos, guardar_datos, exportar_a_csv,obtener_ruta_usuario,
    FICHERO_USUARIOS, FOLDER_OUTPUT
)
from src.modelos import (
    crear_usuario, crear_transaccion, 
    CATEGORIAS_GASTO, CATEGORIAS_INGRESO
)
from src.logica import obtener_balance_general, calcular_total
from utils.validators import validar_usuario, hash_password

# --- FUNCIONES DE LA APLICACIÓN ---

def menu_app(usuario):
    # Definimos las rutas exclusivas para este usuario al entrar
    ruta_g = obtener_ruta_usuario(usuario['username'], "gastos")
    ruta_n = obtener_ruta_usuario(usuario['username'], "nominas")

    while True:
        print(f"\n--- PANEL DE CONTROL - {usuario['username'].upper()} ---")
        print("1. Añadir Ingreso (Nomina)")
        print("2. Añadir Gasto")
        print("3. Ver Balance y Resumen")
        print("4. Exportar Informe (CSV)")
        print("5. Eliminar Gasto/Ingreso")
        print("6. Cerrar Sesión")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            gestionar_registro(ruta_n, CATEGORIAS_INGRESO, "INGRESO")
        elif opcion == "2":
            gestionar_registro(ruta_g, CATEGORIAS_GASTO, "GASTO")
        elif opcion == "3":
            mostrar_resumen(ruta_g, ruta_n)
        elif opcion == "4":
            print("\n--- EXPORTAR DATOS A EXCEL (CSV) ---")
            print("1. Exportar mis Gastos")
            print("2. Exportar mis Nóminas")
            sub_op = input("Selecciona qué exportar: ")

            if sub_op == "1":
                datos = cargar_datos(ruta_g)
                tipo = "gastos"
            elif sub_op == "2":
                datos = cargar_datos(ruta_n)
                tipo = "nominas"
            else:
                print("Opción no válida.")
                continue

            if not datos:
                print("No hay datos para exportar.")
            else:
                # Creamos un nombre de archivo chulo: informe_gastos_pepito.csv
                nombre_csv = f"informe_{tipo}_{usuario['username']}.csv"
                ruta_export = os.path.join(FOLDER_OUTPUT, nombre_csv)
                
                if exportar_a_csv(ruta_export, datos):
                    print(f"¡Éxito! Archivo generado en: {ruta_export}")
                    print("Ya puedes abrirlo con Excel o Google Sheets.")
        elif opcion == "5":
            print("1. Borrar un Gasto")
            print("2. Borrar un Ingreso")
            sub_op = input("Selecciona: ")
            if sub_op == "1": eliminar_registro(ruta_g)
            elif sub_op == "2": eliminar_registro(ruta_n)
        elif opcion == "6":
            break

def gestionar_registro(ruta_fichero, categorias, tipo):
    """Ahora recibe ruta_fichero en lugar de usar una fija"""
    print(f"\n--- NUEVO {tipo} ---")
    try:
        concepto = input("Concepto: ")
        cantidad = float(input("Cantidad: "))
        
        for i, cat in enumerate(categorias, 1):
            print(f"{i}. {cat}")
        
        sel = int(input("Seleccione categoría (nº): "))
        cat_elegida = categorias[sel-1] if 1 <= sel <= len(categorias) else "Otros"

        datos = cargar_datos(ruta_fichero)
        datos.append(crear_transaccion(concepto, cantidad, cat_elegida))
        
        if guardar_datos(ruta_fichero, datos):
            print(f"Guardado en tu archivo personal.")
    except (ValueError, IndexError):
        print("Entrada no válida.")

def mostrar_resumen(ruta_g, ruta_n):
    """Recibe las dos rutas del usuario actual"""
    gastos = cargar_datos(ruta_g)
    nominas = cargar_datos(ruta_n)
    
    total_g = calcular_total(gastos)
    total_n = calcular_total(nominas)
    balance = obtener_balance_general(gastos, nominas)
    
    print(f"\n--- RESUMEN PARA TU USUARIO ---")
    print(f"Ingresos: {total_n}€ | Gastos: {total_g}€")
    color = "🟢" if balance >= 0 else "🔴"
    print(f"ESTADO ACTUAL: {balance}€ {color}")

def eliminar_registro(ruta_fichero):
    datos = cargar_datos(ruta_fichero)
    if not datos:
        print("No hay registros para borrar.")
        return

    print("\n--- ELIMINAR REGISTRO ---")
    for d in datos:
        print(f"ID: {d['id']} | {d['fecha']} | {d['concepto']} | {d['cantidad']}€")
    
    id_a_borrar = input("\nIntroduce el ID del registro que quieres borrar (o 'q' para cancelar): ")
    
    if id_a_borrar.lower() == 'q': return

    # Filtramos la lista: nos quedamos con todo MENOS con el ID que queremos borrar
    nuevos_datos = [d for d in datos if d['id'] != id_a_borrar]

    if len(nuevos_datos) < len(datos):
        if guardar_datos(ruta_fichero, nuevos_datos):
            print("Registro eliminado correctamente.")
    else:
        print("No se encontró ningún registro con ese ID.")

# --- FLUJO DE INICIO Y LOGIN ---

def flujo_registro():
    print("\n--- REGISTRO DE USUARIO ---")
    username = input("Introduce nombre de usuario: ")
    usuarios = cargar_datos(FICHERO_USUARIOS)
    
    if any(u['username'] == username for u in usuarios):
        print("Error: El usuario ya existe.")
        return

    password = input("Introduce contraseña: ")
    email = input("Introduce email: ")
    
    pw_hash = hash_password(password)
    nuevo_usuario = crear_usuario(username, pw_hash, email)
    
    usuarios.append(nuevo_usuario)
    if guardar_datos(FICHERO_USUARIOS, usuarios):
        print("Registro completado con éxito.")

def flujo_login():
    print("\n--- LOGIN ---")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    
    usuario_logueado = validar_usuario(username, password)
    
    if usuario_logueado:
        print(f"\n¡Bienvenido de nuevo, {username}!")
        menu_app(usuario_logueado)
    else:
        print("Usuario o contraseña incorrectos.")

def main():
    while True:
        print("\n--- 💰 GESTOR DE FINANZAS DAM 💰 ---")
        print("1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            flujo_login()
        elif opcion == "2":
            flujo_registro()
        elif opcion == "3":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()