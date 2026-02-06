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
    ruta_g = obtener_ruta_usuario(usuario['username'], "gastos")
    ruta_n = obtener_ruta_usuario(usuario['username'], "ingresos")

    while True:
        # Cabecera personalizada con el nombre del usuario
        mostrar_cabecera(f"📊 PANEL DE CONTROL - {usuario['username'].upper()}")
        
        print("  [1] 💵 Añadir Ingreso        [2] 💸 Añadir Gasto")
        print("  [3] 📈 Ver Balance           [4] 📥 Exportar CSV")
        print("  [5] 🗑️  Eliminar Registro     [6] 🚪 Cerrar Sesión")
        print("  " + "─" * 49)
        
        opcion = input("\n  ⚡ Selecciona una acción: ").strip()

        if opcion == "1":
            gestionar_registro(ruta_n, CATEGORIAS_INGRESO, "INGRESO")
        elif opcion == "2":
            gestionar_registro(ruta_g, CATEGORIAS_GASTO, "GASTO")
        elif opcion == "3":
            mostrar_resumen(ruta_g, ruta_n)
        elif opcion == "4":
            mostrar_cabecera("📂 EXPORTAR DATOS")
            print("  (A) Exportar Gastos")
            print("  (B) Exportar Nóminas")
            sub_op = input("\n  > ¿Qué deseas exportar? (A/B): ").upper()

            if sub_op == "A":
                datos, tipo = cargar_datos(ruta_g), "gastos"
            elif sub_op == "B":
                datos, tipo = cargar_datos(ruta_n), "ingresos"
            else:
                print("  ⚠️ Opción cancelada.")
                continue

            if not datos:
                print("  ❌ No hay datos para exportar.")
            else:
                nombre_csv = f"informe_{tipo}_{usuario['username']}.csv"
                ruta_export = os.path.join(FOLDER_OUTPUT, nombre_csv)
                if exportar_a_csv(ruta_export, datos):
                    print(f"\n  ✅ ¡Éxito! Archivo: {nombre_csv}")
                    print(f"  📍 Ubicación: {ruta_export}")

        elif opcion == "5":
            mostrar_cabecera("🗑️ ELIMINAR REGISTRO")
            print("  (1) Borrar un Gasto")
            print("  (2) Borrar un Ingreso")
            sub_op = input("\n  > Selecciona: ")
            if sub_op == "1": eliminar_registro(ruta_g)
            elif sub_op == "2": eliminar_registro(ruta_n)
            
        elif opcion == "6":
            print(f"\n  Cerrando sesión de {usuario['username']}...")
            break
        else:
            print("\n  ⚠️ Opción no válida.")

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
    ingresos = cargar_datos(ruta_n)
    
    total_g = calcular_total(gastos)
    total_n = calcular_total(ingresos)
    balance = obtener_balance_general(gastos, ingresos)
    
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

def mostrar_cabecera(titulo):
    print("\n" + "═" * 38)
    print(f"{titulo:^38}")
    print("═" * 38)

def main():
    while True:
        mostrar_cabecera(f"📱 MENÚ PRINCIPAL")
        
        # Diseño de opciones con bordes suaves
        print("  ┌──────────────────────────────────┐")
        print("  │  [1] 🔑 Iniciar Sesión           │")
        print("  │  [2] 📝 Registrarse              │")
        print("  │  [3] ❌ Salir                    │")
        print("  └──────────────────────────────────┘")
        
        opcion = input("\n  > Selecciona una opción: ").strip()
        
        if opcion == "1":
            print("\n  Cargando módulo de acceso...")
            flujo_login()
        elif opcion == "2":
            print("\n  Abriendo formulario de registro...")
            flujo_registro()
        elif opcion == "3":
            print("\n  ¡Gracias por usar DAM Finance! 👋")
            print("  Cerrando sesión de forma segura...\n")
            break
        else:
            print("\n  ⚠️  Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()