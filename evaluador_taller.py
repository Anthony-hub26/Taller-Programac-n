import ast
import importlib.util
import math
import multiprocessing as mp
import os
import queue
import sys
import traceback

FUNCIONES = [
    "validar_texto",
    "validar_entero_positivo",
    "validar_decimal_no_negativo",
    "crear_producto",
    "crear_contenedor",
    "agregar_elemento",
    "contar_productos",
    "contar_unidades",
    "calcular_valor_total",
    "buscar_producto",
    "listar_productos",
    "profundidad_maxima",
    "valor_por_contenedor",
]

RECURSIVAS = [
    "contar_productos",
    "contar_unidades",
    "calcular_valor_total",
    "buscar_producto",
    "listar_productos",
    "profundidad_maxima",
    "valor_por_contenedor",
]


def casi_igual(a, b, tol=1e-6):
    try:
        return math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol)
    except Exception:
        return False


def construir_estructura(mod):
    raiz = mod.crear_contenedor("Bodega principal")
    caja_a = mod.crear_contenedor("Caja A")
    caja_b = mod.crear_contenedor("Caja B")
    sub_b1 = mod.crear_contenedor("Subcaja B1")
    sub_b2 = mod.crear_contenedor("Subcaja B2")

    mod.agregar_elemento(raiz, mod.crear_producto("P001", "Agua", 10, 0.75))
    mod.agregar_elemento(caja_a, mod.crear_producto("P002", "Baterías", 4, 3.50))
    mod.agregar_elemento(caja_a, mod.crear_producto("P003", "Linternas", 2, 12.00))
    mod.agregar_elemento(sub_b1, mod.crear_producto("P004", "Cables", 5, 4.00))
    mod.agregar_elemento(sub_b2, mod.crear_producto("P005", "Adaptadores", 3, 6.25))
    mod.agregar_elemento(sub_b1, sub_b2)
    mod.agregar_elemento(caja_b, sub_b1)
    mod.agregar_elemento(raiz, caja_a)
    mod.agregar_elemento(raiz, caja_b)
    return raiz


def cargar_modulo(ruta):
    spec = importlib.util.spec_from_file_location("entrega_estudiante", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def probar_modulo(ruta, salida):
    resultado = {"puntaje": 0.0, "detalle": [], "error_import": None}
    try:
        mod = cargar_modulo(ruta)
    except Exception as exc:
        resultado["error_import"] = f"{type(exc).__name__}: {exc}"
        resultado["detalle"].append(("Importación del archivo", 0, 5, resultado["error_import"]))
        salida.put(resultado)
        return

    # 1. Importación segura (5)
    resultado["puntaje"] += 5
    resultado["detalle"].append(("Importación del archivo", 5, 5, "OK"))

    # 2. Funciones obligatorias (5)
    presentes = [f for f in FUNCIONES if callable(getattr(mod, f, None))]
    puntos = 5 * len(presentes) / len(FUNCIONES)
    resultado["puntaje"] += puntos
    faltantes = sorted(set(FUNCIONES) - set(presentes))
    resultado["detalle"].append(("Funciones obligatorias", puntos, 5, "Faltan: " + ", ".join(faltantes) if faltantes else "OK"))

    # Si faltan funciones críticas, continuar solo con las pruebas posibles.
    def ejecutar(nombre, maximo, prueba):
        try:
            obtenido = prueba()
            if isinstance(obtenido, tuple):
                ok, msg = obtenido
            else:
                ok, msg = bool(obtenido), ""
            pts = maximo if ok else 0
            resultado["puntaje"] += pts
            resultado["detalle"].append((nombre, pts, maximo, msg or ("OK" if ok else "No cumple")))
        except Exception as exc:
            resultado["detalle"].append((nombre, 0, maximo, f"{type(exc).__name__}: {exc}"))

    # 3. Validaciones y constructores (15)
    def test_validaciones():
        if not all(callable(getattr(mod, f, None)) for f in ["validar_texto","validar_entero_positivo","validar_decimal_no_negativo"]):
            return False, "Faltan validadores"
        if mod.validar_texto("  Hola ") != "Hola":
            return False, "validar_texto debe limpiar espacios"
        if mod.validar_entero_positivo("7") != 7:
            return False, "validar_entero_positivo('7') debe devolver 7"
        if not casi_igual(mod.validar_decimal_no_negativo("2.5"), 2.5):
            return False, "validar_decimal_no_negativo('2.5') debe devolver 2.5"
        for fun, valor in [(mod.validar_texto, ""), (mod.validar_entero_positivo, 0), (mod.validar_entero_positivo, -3), (mod.validar_decimal_no_negativo, -1)]:
            try:
                fun(valor)
                return False, "Los valores inválidos deben generar ValueError"
            except ValueError:
                pass
        return True, "Validaciones correctas"
    ejecutar("Validación de entradas", 7, test_validaciones)

    def test_constructores():
        if not all(callable(getattr(mod, f, None)) for f in ["crear_producto","crear_contenedor","agregar_elemento"]):
            return False, "Faltan constructores"
        p = mod.crear_producto(" p9 ", " Cable ", "2", "3.5")
        c = mod.crear_contenedor(" Caja ")
        claves = {"tipo","codigo","nombre","cantidad","precio"}
        if not isinstance(p, dict) or not claves.issubset(p):
            return False, "crear_producto no devuelve el diccionario esperado"
        if p["codigo"] != "P9" or p["cantidad"] != 2 or not casi_igual(p["precio"], 3.5):
            return False, "Producto mal normalizado"
        if not isinstance(c, dict) or c.get("tipo") != "contenedor" or not isinstance(c.get("elementos"), list):
            return False, "crear_contenedor no devuelve la estructura esperada"
        r = mod.agregar_elemento(c, p)
        if p not in c["elementos"] or r is not True:
            return False, "agregar_elemento debe agregar y devolver True"
        return True, "Constructores correctos"
    ejecutar("Creación de productos y contenedores", 8, test_constructores)

    # Construir estructura común
    try:
        raiz = construir_estructura(mod)
    except Exception as exc:
        raiz = None
        resultado["detalle"].append(("Preparación de estructura de prueba", 0, 0, f"No se pudo construir: {exc}"))

    if raiz is not None:
        # 4. Conteos (15)
        ejecutar("Conteo recursivo de productos", 7.5,
                 lambda: (mod.contar_productos(raiz) == 5, f"Esperado 5; obtenido {mod.contar_productos(raiz)}"))
        ejecutar("Conteo recursivo de unidades", 7.5,
                 lambda: (mod.contar_unidades(raiz) == 24, f"Esperado 24; obtenido {mod.contar_unidades(raiz)}"))

        # 5. Valor total (15)
        esperado_valor = 10*0.75 + 4*3.50 + 2*12.00 + 5*4.00 + 3*6.25
        ejecutar("Cálculo recursivo del valor total", 15,
                 lambda: (casi_igual(mod.calcular_valor_total(raiz), esperado_valor),
                          f"Esperado {esperado_valor:.2f}; obtenido {mod.calcular_valor_total(raiz)}"))

        # 6. Buscar/listar (15)
        def test_buscar():
            encontrado = mod.buscar_producto(raiz, "p005")
            if not isinstance(encontrado, dict) or encontrado.get("codigo") != "P005":
                return False, "No encuentra un producto anidado o no ignora mayúsculas/minúsculas"
            if mod.buscar_producto(raiz, "NOEXISTE") is not None:
                return False, "Debe devolver None si no existe"
            return True, "Búsqueda correcta"
        ejecutar("Búsqueda recursiva", 7.5, test_buscar)

        def test_listar():
            lista = mod.listar_productos(raiz)
            if not isinstance(lista, list):
                return False, "Debe devolver una lista"
            codigos = sorted(str(p.get("codigo")) for p in lista if isinstance(p, dict))
            return (codigos == ["P001","P002","P003","P004","P005"], f"Códigos obtenidos: {codigos}")
        ejecutar("Listado plano recursivo", 7.5, test_listar)

        # 7. Profundidad + reporte (15)
        ejecutar("Profundidad máxima", 7,
                 lambda: (mod.profundidad_maxima(raiz) == 4, f"Esperado 4; obtenido {mod.profundidad_maxima(raiz)}"))

        def test_reporte():
            reporte = mod.valor_por_contenedor(raiz)
            if not isinstance(reporte, list):
                return False, "Debe devolver una lista"
            mapa = {}
            for fila in reporte:
                if isinstance(fila, dict) and "contenedor" in fila and "valor" in fila:
                    mapa[fila["contenedor"]] = fila["valor"]
            esperados = {
                "Subcaja B2": 18.75,
                "Subcaja B1": 38.75,
                "Caja B": 38.75,
                "Caja A": 38.0,
                "Bodega principal": 84.25,
            }
            for nombre, valor in esperados.items():
                if nombre not in mapa or not casi_igual(mapa[nombre], valor):
                    return False, f"Reporte incorrecto para {nombre}: {mapa.get(nombre)}"
            return True, "Reporte correcto"
        ejecutar("Reporte recursivo por contenedor", 8, test_reporte)

    salida.put(resultado)


def analizar_codigo(ruta):
    detalle = []
    puntos = 0.0
    try:
        codigo = open(ruta, "r", encoding="utf-8").read()
        arbol = ast.parse(codigo)
    except Exception as exc:
        return 0, [("Análisis estático", 0, 15, f"No se pudo analizar: {exc}")]

    # Recursividad real: 10 puntos distribuidos entre 7 funciones.
    recursivas_encontradas = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)) and nodo.name in RECURSIVAS:
            for sub in ast.walk(nodo):
                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id == nodo.name:
                    recursivas_encontradas.append(nodo.name)
                    break
    recursivas_encontradas = sorted(set(recursivas_encontradas))
    puntos_rec = 10 * len(recursivas_encontradas) / len(RECURSIVAS)
    puntos += puntos_rec
    faltan = sorted(set(RECURSIVAS) - set(recursivas_encontradas))
    detalle.append(("Uso real de recursividad", puntos_rec, 10,
                    "Recursivas detectadas: " + ", ".join(recursivas_encontradas) + (" | Faltan: " + ", ".join(faltan) if faltan else "")))

    # Buenas prácticas mínimas: 5 puntos.
    imports_externos = []
    prohibidos = []
    tiene_main_guard = False
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            imports_externos.extend(alias.name for alias in nodo.names)
        elif isinstance(nodo, ast.ImportFrom):
            imports_externos.append(nodo.module or "")
        elif isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name) and nodo.func.id in {"eval", "exec"}:
            prohibidos.append(nodo.func.id)
        elif isinstance(nodo, ast.If):
            test = nodo.test
            if isinstance(test, ast.Compare) and isinstance(test.left, ast.Name) and test.left.id == "__name__":
                tiene_main_guard = True

    buenas = 0
    msgs = []
    if not imports_externos:
        buenas += 2
    else:
        msgs.append("Imports detectados: " + ", ".join(imports_externos))
    if not prohibidos:
        buenas += 1
    else:
        msgs.append("Uso no permitido: " + ", ".join(prohibidos))
    if tiene_main_guard:
        buenas += 2
    else:
        msgs.append("Falta if __name__ == '__main__'")
    puntos += buenas
    detalle.append(("Buenas prácticas y seguridad", buenas, 5, "OK" if not msgs else " | ".join(msgs)))

    return puntos, detalle


def imprimir_resultado(resultado, estatico):
    total = min(100.0, resultado.get("puntaje", 0) + estatico[0])
    print("\n" + "="*72)
    print("EVALUACIÓN AUTOMÁTICA - TALLER INTEGRADOR DE RECURSIVIDAD")
    print("="*72)
    for nombre, obtenido, maximo, mensaje in resultado.get("detalle", []) + estatico[1]:
        print(f"{nombre:<42} {obtenido:>5.1f}/{maximo:<5.1f}  {mensaje}")
    print("-"*72)
    print(f"NOTA AUTOMÁTICA: {total:.1f} / 100")
    print("="*72)
    print("Nota: la calificación automática valida requisitos funcionales y técnicos.")
    print("El docente puede revisar adicionalmente claridad, explicación y autoría del trabajo.")


def main():
    if len(sys.argv) >= 2:
        ruta = sys.argv[1].strip('"')
    else:
        ruta = input("Ingrese la ruta o nombre del archivo .py del equipo: ").strip().strip('"')

    ruta = os.path.abspath(ruta)
    if not os.path.isfile(ruta):
        print("ERROR: No se encontró el archivo:", ruta)
        sys.exit(1)

    estatico = analizar_codigo(ruta)

    q = mp.Queue()
    p = mp.Process(target=probar_modulo, args=(ruta, q))
    p.start()
    p.join(10)

    if p.is_alive():
        p.terminate()
        p.join()
        resultado = {
            "puntaje": 0,
            "detalle": [("Ejecución/importación", 0, 85, "Tiempo excedido. Revise inputs fuera del main guard o recursión infinita.")],
        }
    else:
        try:
            resultado = q.get(timeout=1)
        except queue.Empty:
            resultado = {
                "puntaje": 0,
                "detalle": [("Ejecución/importación", 0, 85, "El evaluador no recibió resultados del proceso de prueba.")],
            }

    imprimir_resultado(resultado, estatico)


if __name__ == "__main__":
    mp.freeze_support()
    main()
