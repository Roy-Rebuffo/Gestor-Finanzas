def calcular_total(transacciones):
    """Suma todas las cantidades de una lista de transacciones."""
    return sum(t['cantidad'] for t in transacciones)

def obtener_balance_general(gastos, nominas):
    """Calcula la diferencia entre ingresos y gastos."""
    total_gastos = calcular_total(gastos)
    total_ingresos = calcular_total(nominas)
    return total_ingresos - total_gastos

def filtrar_por_categoria(transacciones, categoria):
    """Retorna una lista filtrada por la categoría elegida."""
    return [t for t in transacciones if t['categoria'] == categoria]