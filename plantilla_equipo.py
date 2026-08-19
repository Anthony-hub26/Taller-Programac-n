"""
TALLER INTEGRADOR - FUNDAMENTOS DE PROGRAMACIÓN
Equipo: ________________________________
Integrantes: ____________________________

IMPORTANTE:
- No cambien los nombres de las funciones solicitadas.
- El menú debe ejecutarse únicamente dentro de:
      if __name__ == "__main__":
- No usen librerías externas.
"""


def validar_texto(valor, nombre_campo="texto"):
    if not isinstance(valor, str):
        raise ValueError(f"El campo '{nombre_campo}' debe ser una cadena de texto.")
    texto_limpio = valor.strip()
    if not texto_limpio:
        raise ValueError(f"El campo '{nombre_campo}' no puede estar vacío.")
    return texto_limpio


def validar_entero_positivo(valor, nombre_campo="cantidad"):
    try:
        num = int(valor)
    except (ValueError, TypeError):
        raise ValueError(f"El campo '{nombre_campo}' debe se un número entero válido.")
    if num <= 0:
        raise ValueError(f"El campo '{nombre_campo}' debe ser un entero mayor que cero.")
    return num

def validar_decimal_no_negativo(valor, nombre_campo="precio"):
    # TODO
    pass


def crear_producto(codigo, nombre, cantidad, precio):
    # TODO
    pass


def crear_contenedor(nombre):
    # TODO
    pass


def agregar_elemento(contenedor, elemento):
    # TODO
    pass


def contar_productos(contenedor):
    # RECURSIVA
    pass


def contar_unidades(contenedor):
    # RECURSIVA
    pass


def calcular_valor_total(contenedor):
    # RECURSIVA
    pass


def buscar_producto(contenedor, codigo):
    # RECURSIVA
    pass


def listar_productos(contenedor):
    # RECURSIVA
    pass


def profundidad_maxima(contenedor):
    # RECURSIVA
    pass


def valor_por_contenedor(contenedor):
    # RECURSIVA
    pass


def mostrar_menu():
    # TODO
    pass


def ejecutar_programa():
    # TODO: pueden diseñar su flujo interactivo aquí.
    pass


if __name__ == "__main__":
    ejecutar_programa()
