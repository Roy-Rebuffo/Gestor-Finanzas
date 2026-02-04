# 💰 Gestor de Finanzas Personales (DAM)

Proyecto de gestión de ingresos y gastos desarrollado en Python para el módulo de Programación.

## 🚀 Funcionalidades
* **Sistema Multi-Usuario**: Cada usuario tiene su propia base de datos (archivos JSON independientes).
* **Seguridad**: Registro y login con encriptación de contraseñas (SHA-256).
* **Gestión de Transacciones (CRUD)**: Añadir, ver y eliminar ingresos (nominas) y gastos.
* **Cálculo de Balance**: Resumen automático de ingresos, gastos y saldo actual.
* **Exportación**: Generación de informes en formato CSV para Excel.

## 📁 Estructura del Proyecto
* `main.py`: Punto de entrada y menús del programa.
* `src/`: Lógica del sistema (Modelos, Persistencia y Cálculos).
* `utils/`: Validadores y utilidades de seguridad.
* `output/`: Almacenamiento de datos en JSON y exportaciones CSV.

## 🛠️ Instalación y Uso
1. Clonar el repositorio o descargar el código.
2. Ejecutar el script principal:
   ```bash
   python main.py