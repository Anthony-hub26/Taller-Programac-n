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
    try:
        num = float(valor)
    except (ValueError, TypeError):
        raise ValueError(f"El campo '{nombre_campo}' debe ser un número decimal válido.")
    if num < 0:
        raise ValueError(f"El campo '{nombre_campo}' no puede ser un número negativo.")
    return num


def crear_producto(codigo, nombre, cantidad, precio):
    cod = validar_texto(codigo, "código").upper()
    nom = validar_texto(nombre, "nombre")
    cant = validar_entero_positivo(cantidad, "cantidad")
    prec = validar_decimal_no_negativo(precio, "precio")

    return{
        "tipo": "producto",
        "codigo": cod,
        "nombre": nom,
        "cantidad": cant,
        "precio": prec
    }


def crear_contenedor(nombre):
    nom = validar_texto(nombre, "nombre")
    return{
        "tipo": "contenedor",
        "nombre": nom,
        "elementos": []
    }
    pass


def agregar_elemento(contenedor, elemento):
    if not isinstance(contenedor, dict) or contenedor.get("tipo") != "contenedor" or not isinstance(contenedor.get("elementos"), list):
        raise ValueError ("El parámetro 'contenedor' no tiene una estructura de contenedor válida.")

    if not isinstance(elemento, dict) or elemento.get("tipo") not in ("producto", "contenedor"):
        raise ValueError("El 'elemento' a agregar debe ser un producto o un contenedor válido.")

    contenedor["elementos"].append(elemento)
    return True
    pass


def contar_productos(contenedor):
    total = 0
    for elem in contenedor.get("elementos", []):
        if elem.get("tipo") == "producto":
            total += 1
        elif elem.get("tipo") == "contenedor":
            total += contar_productos(elem)
    return total
    # RECURSIVA
    pass


def contar_unidades(contenedor):
    total = 0
    for elem in contenedor.get("elementos", []):
        if elem.get("tipo") == "productos":
            total += elem.get("cantidad", 0)
        elif elem.get("tipo") == "contenedor":
            total += contar_unidades(elem)
    return total
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
