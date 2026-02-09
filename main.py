import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.persistencia import (
    cargar_datos, guardar_datos, exportar_a_csv, obtener_ruta_usuario,
    FICHERO_USUARIOS, FOLDER_OUTPUT
)
from src.modelos import (
    crear_usuario, crear_transaccion,
    CATEGORIAS_GASTO, CATEGORIAS_INGRESO
)
from src.logica import obtener_balance_general, calcular_total
from utils.validators import validar_usuario, hash_password

# ──────────────────────────
# CONSOLA RICH
# ──────────────────────────
console = Console()

# ──────────────────────────
# FUNCIONES VISUALES (NO LÓGICA)
# ──────────────────────────

def mostrar_cabecera(titulo):
    console.print(
        Panel.fit(
            f"[bold cyan]{titulo}[/bold cyan]",
            border_style="cyan"
        )
    )

def mostrar_tabla_registros(datos, titulo):
    if not datos:
        console.print("[red]No hay registros para mostrar.[/red]")
        return

    tabla = Table(title=titulo, show_lines=True)

    tabla.add_column("ID", justify="center", style="cyan")
    tabla.add_column("Fecha")
    tabla.add_column("Concepto", style="yellow")
    tabla.add_column("Cantidad (€)", justify="right", style="green")
    tabla.add_column("Categoría", style="magenta")

    for d in datos:
        tabla.add_row(
            d["id"],
            d["fecha"],
            d["concepto"],
            f"{d['cantidad']:.2f}",
            d["categoria"]
        )

    console.print(tabla)

# ──────────────────────────
# APLICACIÓN
# ──────────────────────────

def menu_app(usuario):
    ruta_g = obtener_ruta_usuario(usuario['username'], "gastos")
    ruta_n = obtener_ruta_usuario(usuario['username'], "ingresos")

    while True:
        mostrar_cabecera(f"📊 PANEL DE CONTROL - {usuario['username'].upper()}")

        console.print(
            "[bold][1][/bold] 💵 Añadir Ingreso      "
            "[bold][2][/bold] 💸 Añadir Gasto\n"
            "[bold][3][/bold] 📈 Ver Balance         "
            "[bold][4][/bold] 📥 Exportar CSV\n"
            "[bold][5][/bold] 🗑️ Eliminar Registro   "
            "[bold][6][/bold] 🚪 Cerrar Sesión"
        )

        opcion = input("\n⚡ Selecciona una acción: ").strip()

        if opcion == "1":
            gestionar_registro(ruta_n, CATEGORIAS_INGRESO, "INGRESO", ruta_g, ruta_n)
        elif opcion == "2":
            gestionar_registro(ruta_g, CATEGORIAS_GASTO, "GASTO", ruta_g, ruta_n)
        elif opcion == "3":
            mostrar_resumen(ruta_g, ruta_n)
        elif opcion == "4":
            mostrar_cabecera("📂 EXPORTAR DATOS")
            console.print("[A] Exportar Gastos\n[B] Exportar Nóminas")
            sub_op = input("> ¿Qué deseas exportar? (A/B): ").upper()

            if sub_op == "A":
                datos, tipo = cargar_datos(ruta_g), "gastos"
            elif sub_op == "B":
                datos, tipo = cargar_datos(ruta_n), "ingresos"
            else:
                console.print("[yellow]Opción cancelada.[/yellow]")
                continue

            if not datos:
                console.print("[red]No hay datos para exportar.[/red]")
            else:
                nombre_csv = f"informe_{tipo}_{usuario['username']}.csv"
                ruta_export = os.path.join(FOLDER_OUTPUT, nombre_csv)
                
                # --- BARRA DE PROGRESO DE RICH ---
                import time
                from rich.progress import track
                
                print()
                for _ in track(range(10), description=f"[cyan]Generando {nombre_csv}..."):
                    time.sleep(0.1) # Simula el procesamiento de datos
                
                if exportar_a_csv(ruta_export, datos):
                    console.print(f"\n[bold green]✅ ¡Éxito![/bold green] Archivo en: [white u]{ruta_export}[/white u]")

        elif opcion == "5":
            mostrar_cabecera("🗑️ ELIMINAR REGISTRO")
            console.print("[1] Borrar Gasto\n[2] Borrar Ingreso")
            sub_op = input("> Selecciona: ")

            if sub_op == "1":
                eliminar_registro(ruta_g)
            elif sub_op == "2":
                eliminar_registro(ruta_n)

        elif opcion == "6":
            console.print(f"[cyan]Cerrando sesión de {usuario['username']}...[/cyan]")
            break
        else:
            console.print("[red]Opción no válida.[/red]")

def gestionar_registro(ruta_fichero, categorias, tipo, ruta_g, ruta_n):
    mostrar_cabecera(f"➕ NUEVO {tipo}")

    try:
        concepto = input("📝 Concepto: ")
        cantidad = float(input("💶 Cantidad: "))

        console.print("\nCategorías disponibles:")
        for i, cat in enumerate(categorias, 1):
            console.print(f"{i}. {cat}")

        sel = int(input("📂 Seleccione categoría (nº): "))
        cat_elegida = categorias[sel - 1] if 1 <= sel <= len(categorias) else "Otros"

        datos = cargar_datos(ruta_fichero)
        datos.append(crear_transaccion(concepto, cantidad, cat_elegida))

        if guardar_datos(ruta_fichero, datos):
            console.print("[green]Registro guardado correctamente.[/green]")

        mostrar_resumen(ruta_g, ruta_n)

    except (ValueError, IndexError):
        console.print("[red]Entrada no válida. Registro cancelado.[/red]")

def mostrar_resumen(ruta_g, ruta_n):
    gastos = cargar_datos(ruta_g)
    ingresos = cargar_datos(ruta_n)

    total_g = calcular_total(gastos)
    total_n = calcular_total(ingresos)
    balance = total_n - total_g

    tabla = Table(title="💰 ESTADO DE CUENTAS")
    tabla.add_column("Tipo")
    tabla.add_column("Importe (€)", justify="right")

    tabla.add_row("Ingresos", f"{total_n:.2f}")
    tabla.add_row("Gastos", f"{total_g:.2f}")

    estilo = "green" if balance >= 0 else "red"
    tabla.add_row("Balance", f"[{estilo}]{balance:.2f}[/{estilo}]")

    console.print(tabla)

def eliminar_registro(ruta_fichero):
    datos = cargar_datos(ruta_fichero)

    if not datos:
        console.print("[red]No hay registros para borrar.[/red]")
        return

    mostrar_tabla_registros(datos, "🗑️ Registros disponibles")

    id_a_borrar = input("Introduce el ID (o 'q' para cancelar): ")
    if id_a_borrar.lower() == "q":
        return

    nuevos_datos = [d for d in datos if d["id"] != id_a_borrar]

    if len(nuevos_datos) < len(datos):
        guardar_datos(ruta_fichero, nuevos_datos)
        console.print("[green]Registro eliminado correctamente.[/green]")
    else:
        console.print("[red]No se encontró ese ID.[/red]")

# ──────────────────────────
# LOGIN / REGISTRO
# ──────────────────────────

def flujo_registro():
    mostrar_cabecera("📝 REGISTRO DE USUARIO")

    username = input("Usuario: ")
    usuarios = cargar_datos(FICHERO_USUARIOS)

    if any(u["username"] == username for u in usuarios):
        console.print("[red]El usuario ya existe.[/red]")
        return

    password = input("Contraseña: ")
    email = input("Email: ")

    pw_hash = hash_password(password)
    usuarios.append(crear_usuario(username, pw_hash, email))
    guardar_datos(FICHERO_USUARIOS, usuarios)

    console.print("[green]Usuario registrado correctamente.[/green]")

def flujo_login():
    mostrar_cabecera("🔑 LOGIN")

    username = input("Usuario: ")
    password = input("Contraseña: ")

    usuario = validar_usuario(username, password)
    if usuario:
        console.print(f"[green]Bienvenido {username}![/green]")
        menu_app(usuario)
    else:
        console.print("[red]Credenciales incorrectas.[/red]")

def main():
    while True:
        mostrar_cabecera("📱 MENÚ PRINCIPAL")

        console.print(
            "[1] 🔑 Iniciar Sesión\n"
            "[2] 📝 Registrarse\n"
            "[3] ❌ Salir"
        )

        opcion = input("> Selecciona una opción: ").strip()

        if opcion == "1":
            flujo_login()
        elif opcion == "2":
            flujo_registro()
        elif opcion == "3":
            console.print("[cyan]Gracias por usar DAM Finance 👋[/cyan]")
            break
        else:
            console.print("[red]Opción no válida.[/red]")

if __name__ == "__main__":
    main()
