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
            total += int(elem.get("cantidad", 0))
        elif elem.get("tipo") == "contenedor":
            total += contar_unidades(elem)
    return total
    # RECURSIVA
    pass


def calcular_valor_total(contenedor):
    total = 0.0
    for elem in contenedor.get("elementos", []):
        if elem.get("tipo") == "producto":
            total += int(elem.get("cantidad", 0)) * float(elem.get("precio", 0.0))
        elif elem.get("tipo") == "contenedor":
            total += calcular_valor_total(elem)
    return total
    # RECURSIVA
    pass


def buscar_producto(contenedor, codigo):
    codigo_buscado = str(codigo).strip().upper()
    for elem in contenedor.get("elementos", []):
        if elem.get("tipo") == "producto":
            if elem.get("codigo", "").upper() == codigo_buscado:
                return elem
        elif elem.get("tipo") == "contenedor":
            hallado = buscar_producto(elem, codigo_buscado)
            if hallado is not None:
                return hallado
    return None
    # RECURSIVA
    pass


def listar_productos(contenedor):
    productos = []
    for elem in contenedor.get("elementos", []):
        if elem.get("tipo") == "producto":
            productos.append(elem)
        elif elem.get("tipo") == "contenedor":
            productos.extend(listar_productos(elem))
    return productos 
    # RECURSIVA
    pass


def profundidad_maxima(contenedor):
    max_sub = 0
    for elem in contenedor.get("elementos", []):
        if elem.get("tipo") == "contenedor":
            sub_prof = profundidad_maxima(elem)
            if sub_prof > max_sub:
                max_sub = sub_prof
    return 1 + max_sub
    # RECURSIVA
    pass


def valor_por_contenedor(contenedor):
    reporte = [
        {
            "contenedor": contenedor.get("nombre", ""),
            "valor": calcular_valor_total(contenedor)
        }
    ]
    for elem in contenedor.get("elementos", []):
        if elem.get("tipo") == "contenedor":
            reporte.extend(valor_por_contenedor(elem))
    return reporte
    # RECURSIVA
    pass

def construir_estructura_ejemplo():
    raiz = crear_contenedor("Bodega principal")
    caja_a = crear_contenedor("Caja A")
    caja_b = crear_contenedor("Caja B")
    sub_b1 = crear_contenedor("Subcaja B1")
    sub_b2 = crear_contenedor("Subcaja  B2")

    agregar_elemento(raiz, crear_producto("P001", "Agua", 10, 0.75))
    agregar_elemento(caja_a, crear_producto("P002", "Baterías", 4, 3.50))
    agregar_elemento(caja_a, crear_producto("P003", "Linternar", 2, 12.00))
    agregar_elemento(sub_b1, crear_producto("P004", "Cables", 5, 4.00))
    agregar_elemento(sub_b2, crear_producto("P005", "Adaptadores", 3, 6.25))

    agregar_elemento(sub_b1, sub_b2)
    agregar_elemento(caja_b, sub_b1)
    agregar_elemento(raiz, caja_a)
    agregar_elemento(raiz, caja_b)

    return raiz
    pass

def mostrar_menu():
    print("\n################################################")
    print("SISTEMA LOGÍSTICO DE CONTENEDORES")
    print("##################################################")
    print("1. Cargar estructura de prueba")
    print("2. Ver resumen general (Conteos y Valor Total)")
    print("3. Buscar un producto por código")
    print("4. Listar todos los productos")
    print("5. Ver profundidad máxima de la bodega")
    print("6. Generar reporte del valor por contenedor")
    print("0. Salir")
    print("##################################################")
    # TODO
    pass


def ejecutar_programa():
    bodega = None
    while True:
        mostrar_menu()
        opcion = input("Selecciona un opción: ").strip()

        if opcion == "1":
            bodega = construir_estructura_ejemplo()
            print("\n [OK] Estructura de ejemplo cargada.")
        elif opcion == "2":
            if not bodega:
                print("\n[!] Primero cargue la estructura (Opción 1).")
                continue
            print("\n---RESUMEN GENERAL---")
            print(f"Productos diferentes: {contar_productos(bodega)}")
            print(f"Unidades totales    : {contar_unidades(bodega)}")
            print(f"Valor total ($)     : ${calcular_valor_total(bodega):.2f}")

        elif opcion == "3":
            if not bodega:
                print("\n[!]Primero se debe cargar la estructura (Opción 1).")
                continue
            cod = input("Ingrese el código a buscar (ej. P005): ")
            hallado = buscar_producto(bodega, cod)
            if hallado:
                print(f"\n[+] Producto encontrado: {hallado}")
            else:
                print(f"\n[-] No se encontró el producto con código '{cod}'.")
        elif opcion == "4":
            if not bodega:
                print("\n[!]Primero se debe cargar la estructura (Opción 1).")
                continue
            prods = listar_productos(bodega)
            print("\n--- LISTADO DE PRODUCTOS ---")
            for p in prods:
                print(f"[{p['codigo']}] {p['nombre']} | Cant: {p['cantidad']} | Precio: ${p['precio']:.2f}")

        elif opcion == "5":
            if not bodega:
                print("\n[!]Primero se debe cargar la estructura (Opción 1).")
                continue
            prof = profundidad_maxima(bodega)
            print(f"\nProfundiad máxima de la estructura: {prof}")

        elif opcion == "6":
            if not bodega:
                print("\n[!]Primero se debe cargar la estructura (Opción 1).")
                continue
            reporte = valor_por_contenedor(bodega)
            print("\n--- REPORTE DE VALOR POR CONTENEDOR ---")
            for item in reporte:
                print(f"Contenedor: {item['contenedor']:<20} | Subtotal: ${item['valor']:.2f}")

        elif opcion == "0":
            print("\nSaliendo del programa...")
            break
        else:
            print("\n[!] Opción válida. Intente de nuevo")
    # TODO: pueden diseñar su flujo interactivo aquí.
    pass


if __name__ == "__main__":
    ejecutar_programa()
