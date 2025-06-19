import random
from queue import PriorityQueue
from collections import deque
import struct
import os
import pathlib
import math
import time
from typing import List, Tuple, Any


"""
Genera una matriz de booleanos de tamaño m x n con un valor inicial.

:param m: número de filas.
:param n: número de columnas.
:param valor_inicial: valor booleano con el que inicializar cada celda.
:return: matriz de booleanos.
"""
def generar_tabla_booleanos(m, n, valor_inicial=False):
    return [[valor_inicial for _ in range(n)] for _ in range(m)]



"""
    Verifica si una posición (fila, columna) está dentro de los límites de la matriz.

    :param matriz: matriz a comprobar.
    :param fila: índice de fila.
    :param columna: índice de columna.
    :return: True si la posición es válida, False en caso contrario.
    """
def es_posicion_valida(matriz, fila, columna):
    return 0 <= fila < len(matriz) and 0 <= columna < len(matriz[0])



"""
    Devuelve las posiciones adyacentes (arriba, abajo, izquierda, derecha) a una celda dada.

    :param fila: fila actual.
    :param columna: columna actual.
    :return: lista de tuplas con coordenadas adyacentes.
    """
def vecinos_adyacentes(fila, columna):
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [(fila + dx, columna + dy) for dx, dy in movimientos]



"""
    Selecciona aleatoriamente una posición no visitada de una lista de adyacentes.

    :param adyacentes: lista de posiciones adyacentes (tuplas de coordenadas).
    :param visitados: matriz de booleanos que indica qué posiciones ya han sido visitadas.
    :return: una posición no visitada o una aleatoria si todas están visitadas. Devuelve None si no hay adyacentes.
    """
def seleccionar_no_visitado(adyacentes, visitados):
    no_visitados = [pos for pos in adyacentes if not visitados[pos[0]][pos[1]]]
    if no_visitados:
        return random.choice(no_visitados)
    return random.choice(adyacentes) if adyacentes else None




"""
    Selecciona un elemento aleatorio de una lista.

    :param lista: lista de elementos.
    :return: un elemento aleatorio de la lista, o None si la lista está vacía.
    """
def seleccionar_aleatorio(lista):
    if lista:
        return random.choice(lista)
    return None



"""
    Marca una posición en una tabla con un símbolo, excepto si ya contiene 'S'.

    :param tabla: matriz de símbolos.
    :param fila: índice de fila donde marcar.
    :param columna: índice de columna donde marcar.
    :param simbolo: símbolo con el que marcar (por defecto '.').
    """
def marcar_posicion(tabla, fila, columna, simbolo="."):
    if tabla[fila][columna] != "S":
        tabla[fila][columna] = simbolo




"""
    Crea una matriz de tamaño m x n rellenada con un valor específico.

    :param m: número de filas.
    :param n: número de columnas.
    :param valor: valor inicial de cada celda (por defecto un espacio).
    :return: matriz creada como lista de listas.
    """
def crear_matriz(m, n, valor=" "):
    return [[valor for _ in range(n)] for _ in range(m)]




"""
    Guarda una matriz de caracteres en un archivo de texto plano.

    :param matriz: matriz a guardar (lista de listas de caracteres).
    :param nombre_archivo: nombre del archivo donde guardar la matriz.
    """
def guardar_matriz_en_archivo(matriz, nombre_archivo):
    with open(nombre_archivo, "w") as f:
        for fila in matriz:
            f.write("".join(fila) + "\n")



"""
    Carga una matriz desde un archivo de texto, donde cada línea representa una fila.

    :param nombre_archivo: nombre del archivo desde el cual se leerá la matriz.
    :return: matriz cargada como lista de listas de caracteres.
    """
def cargar_matriz_de_archivo(nombre_archivo):
    with open(nombre_archivo, "r") as f:
        lineas = f.readlines()
    return [list(linea.strip()) for linea in lineas]




"""
    Imprime una matriz en la consola, separando los elementos por un carácter opcional.

    :param matriz: matriz a imprimir (lista de listas).
    :param espacio: carácter o cadena usada para separar los elementos (por defecto, espacio).
    """
def imprimir_matriz(matriz, espacio=" "):
    for fila in matriz:
        print(espacio.join(fila))




"""
    Devuelve una lista de vecinos adyacentes que contienen símbolos válidos.

    :param tabla: matriz donde buscar vecinos.
    :param fila: fila actual.
    :param columna: columna actual.
    :param simbolos_validos: conjunto o lista de símbolos considerados válidos para moverse.
    :return: lista de tuplas (fila, columna) con vecinos válidos.
    """
def obtener_vecinos_disponibles(tabla, fila, columna, simbolos_validos):
    vecinos = []
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha
    for dx, dy in movimientos:
        f, c = fila + dx, columna + dy
        if 0 <= f < len(tabla) and 0 <= c < len(tabla[0]):
            if tabla[f][c] in simbolos_validos:
                vecinos.append((f, c))
    return vecinos



"""
    Busca la primera aparición de un símbolo en la matriz.

    :param tabla: matriz donde buscar (lista de listas).
    :param simbolo: símbolo a localizar.
    :return: tupla (fila, columna) con la posición encontrada o None si no se encuentra.
    """
def buscar_posicion(tabla, simbolo):
    for i in range(len(tabla)):
        for j in range(len(tabla[i])):
            if tabla[i][j] == simbolo:
                return (i, j)
    return None



"""
    Solicita al usuario una confirmación binaria (S/N) por consola.

    :param mensaje: texto que se mostrará al usuario.
    :return: True si el usuario responde 'S', False si responde 'N'.
    """
def confirmacion_binaria(mensaje):
    while True:
        respuesta = input(mensaje).strip().upper()
        if respuesta in ['S', 'N']:
            return respuesta == 'S'
        print("Respuesta inválida. Ingrese S o N.")



"""
    Algoritmo A* para encontrar el camino más corto entre dos puntos en una matriz.

    :param matriz: matriz donde se realiza la búsqueda.
    :param entrada: tupla (fila, columna) del punto de inicio.
    :param salida: tupla (fila, columna) del punto de destino.
    :param es_valido: función que determina si una celda es transitable.
    :param heuristica_func: función heurística que estima la distancia al destino.
    :return: lista de tuplas representando el camino desde entrada hasta salida, o None si no se encuentra.
    """
def a_estrella(matriz, entrada, salida, es_valido, heuristica_func):

    filas, columnas = len(matriz), len(matriz[0])
    visitados = [[float('inf')] * columnas for _ in range(filas)]
    padre = [[None] * columnas for _ in range(filas)]

    fx, fy = salida
    ex, ey = entrada
    visitados[ex][ey] = 0

    abierta = PriorityQueue()
    abierta.put((heuristica_func(ex, ey, fx, fy), 0, ex, ey))

    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while not abierta.empty():
        f, g, x, y = abierta.get()

        if (x, y) == salida:
            camino = []
            while (x, y) != entrada:
                camino.append((x, y))
                x, y = padre[x][y]
            camino.append(entrada)
            camino.reverse()
            return camino

        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas and es_valido(matriz[nx][ny]):
                nuevo_g = g + 1
                if nuevo_g < visitados[nx][ny]:
                    visitados[nx][ny] = nuevo_g
                    padre[nx][ny] = (x, y)
                    h = heuristica_func(nx, ny, fx, fy)
                    abierta.put((nuevo_g + h, nuevo_g, nx, ny))

    return None




"""
    Realiza una búsqueda en anchura (BFS) para encontrar el camino más corto entre dos puntos.

    :param matriz: matriz donde se realiza la búsqueda.
    :param entrada: tupla (fila, columna) del punto inicial.
    :param salida: tupla (fila, columna) del destino.
    :param es_valido: función que verifica si una celda es transitable.
    :return: lista de tuplas representando el camino encontrado o None si no hay camino.
    """
def busqueda_anchura(matriz, entrada, salida, es_valido):
    filas, columnas = len(matriz), len(matriz[0])
    visitados = [[False] * columnas for _ in range(filas)]
    padre = [[None] * columnas for _ in range(filas)]

    cola = deque()
    ex, ey = entrada
    sx, sy = salida
    cola.append((ex, ey))
    visitados[ex][ey] = True

    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while cola:
        x, y = cola.popleft()
        if (x, y) == (sx, sy):
            # Reconstruir camino
            camino = []
            while (x, y) != entrada:
                camino.append((x, y))
                x, y = padre[x][y]
            camino.append(entrada)
            camino.reverse()
            return camino

        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                if es_valido(matriz[nx][ny]) and not visitados[nx][ny]:
                    visitados[nx][ny] = True
                    padre[nx][ny] = (x, y)
                    cola.append((nx, ny))

    return None  # No se encontró camino



"""
    Realiza una búsqueda en profundidad (DFS) para encontrar un camino entre dos puntos.

    :param matriz: matriz donde se realiza la búsqueda.
    :param entrada: tupla (fila, columna) del punto inicial.
    :param salida: tupla (fila, columna) del destino.
    :param es_valido: función que indica si una celda es transitable.
    :return: lista de tuplas representando el camino encontrado o None si no se encuentra.
    """
def busqueda_profundidad(matriz, entrada, salida, es_valido):
    filas, columnas = len(matriz), len(matriz[0])
    visitados = [[False] * columnas for _ in range(filas)]
    pila = [(entrada, 0)]
    camino = [entrada]
    ex, ey = entrada
    visitados[ex][ey] = True

    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while pila:
        (x, y), prof = pila[-1]

        if (x, y) == salida:
            return camino

        opciones = []
        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                if es_valido(matriz[nx][ny]) and not visitados[nx][ny]:
                    opciones.append((nx, ny))

        if opciones:
            siguiente = random.choice(opciones)
            visitados[siguiente[0]][siguiente[1]] = True
            pila.append((siguiente, prof + 1))
            camino.append(siguiente)
        else:
            pila.pop()
            camino.pop()

    return None  # No se encontró camino




"""
    Realiza una búsqueda Greedy Best-First Search para encontrar un camino hacia el objetivo.

    :param matriz: matriz donde se realiza la búsqueda.
    :param entrada: tupla (fila, columna) del punto inicial.
    :param salida: tupla (fila, columna) del destino.
    :param es_valido: función que indica si una celda es transitable.
    :param heuristica_func: función heurística que estima la distancia al objetivo.
    :return: lista de tuplas representando el camino encontrado o None si no se encuentra.
    """
def busqueda_gbfs(matriz, entrada, salida, es_valido, heuristica_func):

    filas, columnas = len(matriz), len(matriz[0])
    visitados = [[False for _ in range(columnas)] for _ in range(filas)]
    padre = [[None for _ in range(columnas)] for _ in range(filas)]

    fx, fy = salida
    ex, ey = entrada
    visitados[ex][ey] = True

    abierta = PriorityQueue()
    h_inicio = heuristica_func(ex, ey, fx, fy)
    abierta.put((h_inicio, ex, ey))

    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while not abierta.empty():
        h, x, y = abierta.get()

        if (x, y) == salida:
            camino = []
            while (x, y) != entrada:
                camino.append((x, y))
                x, y = padre[x][y]
            camino.append(entrada)
            camino.reverse()
            return camino

        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                if es_valido(matriz[nx][ny]) and not visitados[nx][ny]:
                    visited = True
                    padre[nx][ny] = (x, y)
                    hn = heuristica_func(nx, ny, fx, fy)
                    abierta.put((hn, nx, ny))
                    visitados[nx][ny] = True

    return None


"""
    Calcula la distancia de Manhattan entre dos posiciones de una matriz.

    :param fila_actual: fila del punto actual.
    :param columna_actual: columna del punto actual.
    :param fila_s: fila del destino.
    :param columna_s: columna del destino.
    :return: distancia Manhattan entre los dos puntos.
    """
def heuristica_manhattan(fila_actual, columna_actual, fila_s, columna_s):
    return abs(fila_actual - fila_s) + abs(columna_actual - columna_s)



"""
    Calcula la distancia euclídea entre dos posiciones de una matriz.

    :param fila_actual: fila del punto actual.
    :param columna_actual: columna del punto actual.
    :param fila_s: fila del destino.
    :param columna_s: columna del destino.
    :return: distancia euclídea entre los dos puntos.
    """
def heuristica_euclidea(fila_actual, columna_actual, fila_s, columna_s):
    return math.sqrt((fila_actual - fila_s) ** 2 + (columna_actual - columna_s) ** 2)



"""
    Implementa el algoritmo IDA* (Iterative Deepening A*) para encontrar un camino entre dos puntos.

    :param matriz: matriz sobre la que se busca el camino.
    :param entrada: posición inicial (fila, columna).
    :param salida: posición final (fila, columna).
    :param es_valido: función que determina si una celda es transitable.
    :param heuristica_func: función heurística que estima la distancia al destino.
    :return: lista de tuplas con el camino desde entrada hasta salida, o None si no se encuentra.
    """
def ida_star(matriz, entrada, salida, es_valido, heuristica_func):
    filas, columnas = len(matriz), len(matriz[0])
    camino = [[None] * columnas for _ in range(filas)]
    visitados = [[False] * columnas for _ in range(filas)]

    def heur(f1, c1):
        return round(heuristica_func(f1, c1, salida[0], salida[1]))

    def ida(x, y, g, umbral):
        f = g + heur(x, y)
        if f > umbral:
            return f
        if (x, y) == salida:
            return "encontrado"

        min_val = float("inf")
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas and es_valido(matriz[nx][ny]) and not visitados[nx][ny]:
                visitados[nx][ny] = True
                camino[nx][ny] = (x, y)
                resultado = ida(nx, ny, g + 1, umbral)
                if resultado == "encontrado":
                    return "encontrado"
                if resultado < min_val:
                    min_val = resultado
                visitados[nx][ny] = False  # backtrack

        return min_val

    umbral = heur(entrada[0], entrada[1])
    while True:
        visitados = [[False] * columnas for _ in range(filas)]
        visitados[entrada[0]][entrada[1]] = True
        resultado = ida(entrada[0], entrada[1], 0, umbral)
        if resultado == "encontrado":
            # reconstruir camino
            x, y = salida
            ruta = []
            while (x, y) != entrada:
                ruta.append((x, y))
                x, y = camino[x][y]
            ruta.append(entrada)
            ruta.reverse()
            return ruta
        if resultado == float("inf"):
            return None
        umbral = resultado



"""
    Mide el tiempo de ejecución de una función sin argumentos.

    :param f: función que se va a ejecutar.
    :return: duración de la ejecución en microsegundos.
    """
def medir_tiempo_ejecucion(algoritmo):
    inicio = time.time_ns()
    algoritmo.moverse()
    fin = time.time_ns()
    duracion_microsegundos = (fin - inicio) / 1000
    print("Tiempo de ejecucion: " + str(duracion_microsegundos) + "ns")



"""
    Realiza una búsqueda bidireccional desde entrada y salida hasta que se encuentren.

    :param matriz: matriz donde se realiza la búsqueda.
    :param entrada: tupla (fila, columna) del punto de inicio.
    :param salida: tupla (fila, columna) del punto de destino.
    :param es_valido: función que determina si una celda es transitable.
    :return: lista de tuplas representando el camino desde entrada hasta salida, o None si no se encuentra.
    """
def busqueda_bidireccional(matriz, entrada, salida, es_valido):

    filas, columnas = len(matriz), len(matriz[0])
    visitados_inicio = [[False] * columnas for _ in range(filas)]
    visitados_salida = [[False] * columnas for _ in range(filas)]
    padre_inicio = [[None] * columnas for _ in range(filas)]
    padre_salida = [[None] * columnas for _ in range(filas)]

    cola_inicio = deque()
    cola_salida = deque()

    ex, ey = entrada
    sx, sy = salida

    cola_inicio.append(entrada)
    cola_salida.append(salida)
    visitados_inicio[ex][ey] = True
    visitados_salida[sx][sy] = True

    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while cola_inicio and cola_salida:
        actual_inicio = cola_inicio.popleft()
        actual_salida = cola_salida.popleft()

        for dx, dy in movimientos:
            # Expansión desde inicio
            nx, ny = actual_inicio[0] + dx, actual_inicio[1] + dy
            if 0 <= nx < filas and 0 <= ny < columnas and es_valido(matriz[nx][ny]):
                if not visitados_inicio[nx][ny]:
                    visitados_inicio[nx][ny] = True
                    padre_inicio[nx][ny] = actual_inicio
                    cola_inicio.append((nx, ny))
                    if visitados_salida[nx][ny]:
                        return reconstruir_camino((nx, ny), padre_inicio, padre_salida)

            # Expansión desde salida
            nx2, ny2 = actual_salida[0] + dx, actual_salida[1] + dy
            if 0 <= nx2 < filas and 0 <= ny2 < columnas and es_valido(matriz[nx2][ny2]):
                if not visitados_salida[nx2][ny2]:
                    visitados_salida[nx2][ny2] = True
                    padre_salida[nx2][ny2] = actual_salida
                    cola_salida.append((nx2, ny2))
                    if visitados_inicio[nx2][ny2]:
                        return reconstruir_camino((nx2, ny2), padre_inicio, padre_salida)

    return None  # No se encontró camino



"""
    Reconstruye el camino completo entre dos puntos a partir de sus padres desde
    una posición de intersección (para búsqueda bidireccional).

    :param interseccion: punto donde se encontraron las dos búsquedas.
    :param padre_inicio: matriz de padres desde el punto de entrada.
    :param padre_salida: matriz de padres desde el punto de salida.
    :return: lista de tuplas representando el camino completo de entrada a salida.
    """
def reconstruir_camino(interseccion, padre_inicio, padre_salida):
    x, y = interseccion
    camino = []

    # Desde intersección a origen
    while (x, y) and padre_inicio[x][y] is not None:
        camino.append((x, y))
        x, y = padre_inicio[x][y]
    camino.append((x, y))
    camino.reverse()

    # Desde intersección a destino
    x, y = interseccion
    while padre_salida[x][y] is not None:
        x, y = padre_salida[x][y]
        camino.append((x, y))

    return camino



"""
    Realiza búsqueda en profundidad iterativa (IDDFS) para encontrar un camino entre dos puntos.

    :param matriz: matriz sobre la que se realiza la búsqueda.
    :param entrada: tupla (fila, columna) con el punto de inicio.
    :param salida: tupla (fila, columna) con el punto de destino.
    :param es_valido: función que indica si una celda es transitable.
    :return: lista de tuplas con el camino encontrado, o None si no existe.
    """
def busqueda_profundidad_iterativa(matriz, entrada, salida, es_valido):
    filas, columnas = len(matriz), len(matriz[0])

    def limite(x, y, profundidad_restante, visitados, camino):
        if (x, y) == salida:
            camino.append((x, y))
            return True
        if profundidad_restante == 0:
            return False

        visitados[x][y] = True
        camino.append((x, y))
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                if es_valido(matriz[nx][ny]) and not visitados[nx][ny]:
                    if limite(nx, ny, profundidad_restante - 1, visitados, camino):
                        return True

        camino.pop()
        return False

    limite_max = 1
    while True:
        visitados = [[False] * columnas for _ in range(filas)]
        camino = []
        if limite(entrada[0], entrada[1], limite_max, visitados, camino):
            return camino
        limite_max += 1
        if limite_max > filas * columnas:  # protección contra bucles infinitos
            return None



"""
    Realiza una búsqueda en profundidad (DFS) limitada por profundidad máxima.

    :param matriz: matriz donde se realiza la búsqueda.
    :param entrada: tupla (fila, columna) del punto inicial.
    :param salida: tupla (fila, columna) del punto de destino.
    :param es_valido: función que indica si una celda es transitable.
    :param limite: profundidad máxima permitida en la búsqueda.
    :return: lista de tuplas con el camino encontrado o None si no se encuentra dentro del límite.
    """
def busqueda_profundidad_con_limite(matriz, entrada, salida, es_valido, limite):

    filas, columnas = len(matriz), len(matriz[0])
    pila = [entrada]
    visitados = [[False for _ in range(columnas)] for _ in range(filas)]
    camino = [entrada]
    visitados[entrada[0]][entrada[1]] = True
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while pila:
        x, y = pila[-1]
        if (x, y) == salida:
            return camino

        if len(camino) - 1 >= limite:
            pila.pop()
            camino.pop()
            continue

        opciones = []
        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas and es_valido(matriz[nx][ny]):
                if not visitados[nx][ny]:
                    opciones.append((nx, ny))

        if opciones:
            siguiente = random.choice(opciones)
            visitados[siguiente[0]][siguiente[1]] = True
            pila.append(siguiente)
            camino.append(siguiente)
        else:
            pila.pop()
            camino.pop()

    return None  # No se encontró camino dentro del límite



"""
    Cambia el turno y la ficha actual en un juego por turnos como Tres en Raya.

    :param turno_actual: valor booleano indicando el turno actual (True/False).
    :param ficha_actual: ficha actual del jugador ('X' o 'O').
    :return: tupla (nuevo_turno, nueva_ficha).
    """
def intercambiar_turno(turno_actual, ficha_actual):
    nuevo_turno = not turno_actual
    nueva_ficha = "O" if ficha_actual == "X" else "X"
    return nuevo_turno, nueva_ficha



"""
    Verifica si una matriz está completamente llena (sin celdas con valor vacío).

    :param matriz: matriz a verificar.
    :param valor_vacio: valor que representa una celda vacía (por defecto, espacio).
    :return: True si no hay celdas vacías, False en caso contrario.
    """
def esta_lleno(matriz, valor_vacio=" "):
    for fila in matriz:
        for celda in fila:
            if celda == valor_vacio:
                return False
    return True



"""
    Traduce una posición lineal a coordenadas (fila, columna) en una matriz cuadrada.

    :param pos: posición lineal (empezando desde 1).
    :param tamMatriz: tamaño del lado de la matriz (asume matriz cuadrada).
    :return: tupla (fila, columna) correspondiente a la posición.
    """
def traducir_posicion(pos,tamMatriz):
    fila = (pos - 1) // tamMatriz
    columna = (pos - 1) % tamMatriz
    return fila, columna



"""
    Busca una línea ganadora (tres en raya) en una matriz 3x3.

    :param matriz: matriz del juego (3x3).
    :param valor_vacio: símbolo que representa una celda vacía.
    :return: lista de coordenadas [(i1,j1), (i2,j2), (i3,j3)] si hay línea ganadora, o None si no hay.
    """
def buscar_linea_en_matriz(matriz, valor_vacio=" "):
    # Horizontales
    for i in range(3):
        if matriz[i][0] == matriz[i][1] == matriz[i][2] and matriz[i][0] != valor_vacio:
            return [(i, 0), (i, 1), (i, 2)]

    # Verticales
    for i in range(3):
        if matriz[0][i] == matriz[1][i] == matriz[2][i] and matriz[0][i] != valor_vacio:
            return [(0, i), (1, i), (2, i)]

    # Diagonal principal
    if matriz[0][0] == matriz[1][1] == matriz[2][2] and matriz[0][0] != valor_vacio:
        return [(0, 0), (1, 1), (2, 2)]

    # Diagonal inversa
    if matriz[0][2] == matriz[1][1] == matriz[2][0] and matriz[0][2] != valor_vacio:
        return [(0, 2), (1, 1), (2, 0)]

    return None



"""
    Crea una copia profunda de una matriz (lista de listas).

    :param matriz: matriz original a copiar.
    :return: nueva matriz independiente con los mismos valores.
    """
def copiar_matriz(matriz):
    return [fila[:] for fila in matriz]




"""
    Implementa el algoritmo de Minimax con poda Alfa-Beta para juegos como Tres en Raya.

    :param estado_inicial: estado actual del juego (objeto con métodos terminado, sucesores, ganador).
    :param ficha: ficha de la IA que está maximizando ('X' o 'O').
    :param verbose: si es True, muestra información sobre los nodos y tiempo.
    :return: jugada óptima desde el estado dado.
    """
def poda_alfa_beta(estado_inicial, ficha, verbose=False):
    import time
    nodos = 0

    def max_valor(estado, alfa, beta):
        nonlocal nodos
        nodos += 1
        if estado.terminado():
            return estado.ganador(ficha)
        valor = float('-inf')
        for sucesor, _ in estado.sucesores():
            valor = max(valor, min_valor(sucesor, alfa, beta))
            if valor >= beta:
                return valor
            alfa = max(alfa, valor)
        return valor

    def min_valor(estado, alfa, beta):
        nonlocal nodos
        nodos += 1
        if estado.terminado():
            return estado.ganador(ficha)
        valor = float('inf')
        for sucesor, _ in estado.sucesores():
            valor = min(valor, max_valor(sucesor, alfa, beta))
            if valor <= alfa:
                return valor
            beta = min(beta, valor)
        return valor

    mejor_valor = float('-inf')
    alfa = float('-inf')
    beta = float('inf')
    mejor_jugada = None

    inicio = time.perf_counter_ns()
    for sucesor, jugada in estado_inicial.sucesores():
        valor = min_valor(sucesor, alfa, beta)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_jugada = jugada
        alfa = max(alfa, mejor_valor)
    fin = time.perf_counter_ns()
    duracion = (fin - inicio) / 1000  # microsegundos

    if verbose:
        print(f"Nodos explorados: {nodos}")
        print(f"Tiempo empleado: {duracion} µs")

    return mejor_jugada



"""
    Implementa el algoritmo Minimax clásico sin poda para juegos por turnos como Tres en Raya.

    :param estado_inicial: estado actual del juego (debe tener métodos terminado, sucesores, ganador y jugadorActual).
    :param ficha: ficha que representa al jugador que maximiza ('X' o 'O').
    :param verbose: si es True, muestra el número de nodos explorados y tiempo de ejecución.
    :return: jugada óptima desde el estado dado.
    """
def minimax(estado_inicial, ficha, verbose=False):
    import time
    nodos = 0

    def max_valor(estado):
        nonlocal nodos
        nodos += 1
        if estado.terminado():
            return estado.ganador(ficha)
        valor = float("-inf")
        for sucesor, _ in estado.sucesores():
            if sucesor.jugadorActual() == ficha:
                valor = max(valor, max_valor(sucesor))
            else:
                valor = max(valor, min_valor(sucesor))
        return valor

    def min_valor(estado):
        nonlocal nodos
        nodos += 1
        if estado.terminado():
            return estado.ganador(ficha)
        valor = float("inf")
        for sucesor, _ in estado.sucesores():
            if sucesor.jugadorActual() == ficha:
                valor = min(valor, max_valor(sucesor))
            else:
                valor = min(valor, min_valor(sucesor))
        return valor

    mejor_valor = float("-inf") if estado_inicial.jugadorActual() == ficha else float("inf")
    mejor_jugada = None

    inicio = time.perf_counter_ns()
    for sucesor, jugada in estado_inicial.sucesores():
        if sucesor.jugadorActual() == ficha:
            valor = max_valor(sucesor)
        else:
            valor = min_valor(sucesor)

        if estado_inicial.jugadorActual() == ficha:
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_jugada = jugada
        else:
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_jugada = jugada
    fin = time.perf_counter_ns()
    duracion = (fin - inicio) / 1000  # microsegundos

    if verbose:
        print(f"Nodos explorados: {nodos}")
        print(f"Tiempo empleado: {duracion} µs")

    return mejor_jugada




"""
    Solicita al usuario que introduzca un número entero dentro de un rango válido.

    :param mensaje: mensaje que se muestra al usuario.
    :param minimo: valor mínimo aceptado (inclusive).
    :param maximo: valor máximo aceptado (inclusive).
    :return: número entero introducido por el usuario dentro del rango.
    """
def leer_entrada_entero_en_rango(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo or valor > maximo:
                print(f"El número debe estar entre {minimo} y {maximo}.")
                continue
            return valor
        except ValueError:
            print("Entrada no válida. Por favor, introduce un número entero.")




"""
    Muestra los resultados almacenados en un archivo utilizando la clase Contador del módulo Resultados.

    :param ruta_archivo: ruta del archivo que contiene los datos a mostrar.
    """
def mostrar_resultados_archivo(ruta_archivo):
    from Resultados import Contador
    contador = Contador(ruta_archivo)
    contador.mostrarResultados()



"""
    Reinicia el contenido de múltiples archivos escribiendo una lista de valores en cada uno.

    :param lista_archivos: lista de rutas de archivos a reiniciar.
    :param valores_por_linea: lista de valores a escribir, uno por línea, en cada archivo.
    """
def reiniciar_archivos_con_valores(lista_archivos, valores_por_linea):
    for archivo in lista_archivos:
        with open(archivo, "w") as f:
            for valor in valores_por_linea:
                f.write(f"{valor}\n")



"""
    Muestra un menú en consola con opciones numeradas y lee una opción válida del usuario.

    :param titulo: título del menú.
    :param opciones: lista de textos para cada opción.
    :param minimo: número mínimo permitido (por defecto 1).
    :param maximo: número máximo permitido (por defecto igual al número de opciones).
    :return: número entero seleccionado por el usuario dentro del rango permitido.
    """
def mostrar_menu_y_leer_opcion(titulo, opciones, minimo=1, maximo=None):
    if maximo is None:
        maximo = len(opciones)

    print("\n")
    print("┌" + "─" * 32 + "┐")
    print("│{:^32}│".format(titulo))
    print("├" + "─" * 32 + "┤")
    for idx, texto in enumerate(opciones, start=1):
        print("│ {:<2}. {:<25}│".format(idx, texto))
    print("└" + "─" * 32 + "┘")

    return leer_entrada_entero_en_rango("Selecciona una opción: ", minimo, maximo)



"""
    Devuelve el texto con formato ANSI para mostrarlo en color en la consola.

    :param texto: Cadena de texto a colorear
    :param color: Nombre del color ("rojo", "verde", "amarillo", "azul", "magenta", "cian", "gris", "reset")
    :return: Texto coloreado con código ANSI
    """
def colorear_texto(texto, color="reset"):
    
    colores = {
        "rojo": "\033[31m",
        "verde": "\033[32m",
        "amarillo": "\033[33m",
        "azul": "\033[34m",
        "magenta": "\033[35m",
        "cian": "\033[36m",
        "gris": "\033[90m",
        "reset": "\033[0m"
    }
    color_ansi = colores.get(color.lower(), colores["reset"])
    reset_ansi = colores["reset"]
    return f"{color_ansi}{texto}{reset_ansi}"



#----------------------------------------------------------

def redimensionar_array(original, nuevo_tam):
    """
    Redimensiona una lista en Python.
    - original: lista original.
    - nuevo_tam: nuevo tamaño que queremos asignar.
    Devuelve una nueva lista redimensionada.
    """
    viejo_tam = len(original)
    nuevo = [None] * nuevo_tam
    for i in range(min(viejo_tam, nuevo_tam)):
        nuevo[i] = original[i]
    return nuevo


def intercambiar(a, b):
    """
    Intercambia los valores de dos variables.
    Devuelve una tupla con los valores intercambiados.
    """
    return b, a


def ordenar_burbuja(array, comp):
    """
    Ordena una lista usando el algoritmo de burbuja y un comparador personalizado.
    - array: lista a ordenar.
    - comp: función que compara dos elementos y devuelve True si el primero es 'mayor' que el segundo.
    """
    n = len(array)
    for i in range(n - 1):
        for j in range(n - 1):
            if comp(array[j], array[j + 1]):
                array[j], array[j + 1] = intercambiar(array[j], array[j + 1])


def es_cantidad_cero(cantidad):
    """
    Devuelve True si la cantidad es 0.
    Útil para verificar si un contenedor está vacío.
    """
    return cantidad == 0



def copiar_cadena(origen: str, tam_max: int) -> str:
    """
    Copia una cadena a otra sin sobrepasar el tamaño máximo.
    Devuelve una nueva cadena con longitud máxima tam_max - 1.
    """
    return origen[:tam_max - 1]



def insertar_ordenado_binario(nombre_archivo, cantidad, nuevo, fmt, menor_que):
    """
    Inserta un nuevo elemento en un archivo binario ordenado.

    - nombre_archivo: ruta del archivo binario.
    - cantidad: número actual de elementos (entero en la cabecera del archivo).
    - nuevo: nuevo objeto a insertar (por ejemplo, un número o tupla).
    - fmt: formato struct (por ejemplo, 'i' para int, 'f' para float, etc.).
    - menor_que: función que compara si un elemento es menor que otro.
    
    Devuelve el nuevo valor de cantidad.
    """
    size = struct.calcsize(fmt)
    with open(nombre_archivo, 'rb+') as f:
        f.seek(0)
        raw = f.read(4)
        if raw:
            cantidad = struct.unpack('i', raw)[0]
        else:
            cantidad = 0

        pos = cantidad
        f.seek(4)
        for i in range(cantidad):
            data = f.read(size)
            actual = struct.unpack(fmt, data)[0]
            if menor_que(nuevo, actual):
                pos = i
                break

        # Desplazar elementos hacia la derecha
        for i in range(cantidad, pos, -1):
            f.seek(4 + (i - 1) * size)
            data = f.read(size)
            f.seek(4 + i * size)
            f.write(data)

        # Escribir nuevo elemento en la posición correcta
        f.seek(4 + pos * size)
        f.write(struct.pack(fmt, nuevo))

        # Actualizar cantidad
        cantidad += 1
        f.seek(0)
        f.write(struct.pack('i', cantidad))
    
    return cantidad



def buscar_elemento_binario_condicion(nombre_archivo, cantidad, fmt, condicion):
    """
    Busca el primer elemento que cumple cierta condición en un archivo binario.

    - nombre_archivo: nombre del archivo binario.
    - cantidad: número de elementos en el archivo (excluyendo la cabecera).
    - fmt: formato 'struct' para leer (ej. 'i' para int).
    - condicion: función que devuelve True si el elemento cumple la condición.

    Devuelve la posición (1-based) o -1 si no se encuentra.
    """
    size = struct.calcsize(fmt)
    with open(nombre_archivo, 'rb') as f:
        f.seek(4)  # saltar la cabecera (int con cantidad)
        for i in range(1, cantidad + 1):
            data = f.read(size)
            if not data:
                break
            valor = struct.unpack(fmt, data)[0]
            if condicion(valor):
                return i
    return -1



def eliminar_elemento_binario_por_pos(nombre_archivo, cantidad, posicion, fmt):
    """
    Elimina un elemento de un archivo binario por posición (1-based).
    
    - nombre_archivo: ruta del archivo.
    - cantidad: número total de elementos antes de eliminar.
    - posicion: posición 1-based del elemento a eliminar.
    - fmt: formato de struct.
    
    Devuelve el nuevo valor de cantidad.
    """
    if posicion < 1 or posicion > cantidad:
        return cantidad

    size = struct.calcsize(fmt)
    with open(nombre_archivo, 'rb+') as f:
        for i in range(posicion, cantidad):
            f.seek(4 + i * size)
            data = f.read(size)
            f.seek(4 + (i - 1) * size)
            f.write(data)

        cantidad -= 1
        f.seek(0)
        f.write(struct.pack('i', cantidad))
    
    return cantidad



class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

def insertar_ordenado_lista_enlazada(inicio, nuevo, menor):
    """
    Inserta un nodo en una lista enlazada simple ordenada según un criterio.
    - inicio: nodo inicial (o None).
    - nuevo: nodo a insertar.
    - menor: función que compara si un nodo es menor que otro.
    Devuelve el nuevo nodo inicio.
    """
    if not inicio or menor(nuevo, inicio):
        nuevo.siguiente = inicio
        return nuevo
    actual = inicio
    while actual.siguiente and not menor(nuevo, actual.siguiente):
        actual = actual.siguiente
    nuevo.siguiente = actual.siguiente
    actual.siguiente = nuevo
    return inicio



def buscar_en_lista_enlazada(inicio, condicion):
    """
    Busca el primer nodo que cumple cierta condición.
    - inicio: nodo inicial de la lista enlazada.
    - condicion: función que recibe un nodo y devuelve True si es el buscado.
    Devuelve el nodo encontrado o None.
    """
    while inicio:
        if condicion(inicio):
            return inicio
        inicio = inicio.siguiente
    return None




def calcular_media(datos, obtener_valor):
    """
    Calcula la media de una lista de objetos usando una función extractora.
    - datos: lista de objetos.
    - obtener_valor: función que extrae un número (float/int) de cada objeto.
    """
    n = len(datos)
    if n == 0:
        return 0.0
    suma = sum(obtener_valor(d) for d in datos)
    return suma / n



def ordenar_por_campo(array, menor):
    """
    Ordena una lista de objetos por inserción directa según un comparador.
    - array: lista a ordenar (in place).
    - menor: función que devuelve True si a < b.
    """
    for i in range(1, len(array)):
        actual = array[i]
        j = i - 1
        while j >= 0 and menor(actual, array[j]):
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = actual


import random

def generar_aleatorio(minimo, maximo):
    """
    Genera un número entero aleatorio entre mínimo y máximo (ambos incluidos).

    :param minimo: valor mínimo del rango.
    :param maximo: valor máximo del rango.
    :return: número aleatorio entero entre mínimo y máximo.
    """
    return random.randint(minimo, maximo)



def busqueda_lineal(v, valor):
    """
    Realiza una búsqueda lineal para encontrar un valor en una lista.

    :param v: lista donde buscar.
    :param valor: valor a buscar en la lista.
    :return: índice del valor si se encuentra, o -1 si no está presente.
    """
    for i in range(len(v)):
        if v[i] == valor:
            return i
    return -1



def ordenar_burbuja_enteros(v):
    """
    Ordena una lista de enteros usando el algoritmo de burbuja (versión simple).

    :param v: lista de números enteros a ordenar.
    """
    n = len(v)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if v[j] < v[i]:
                v[i], v[j] = v[j], v[i]



def vaciar_array_enteros():
    """
    Simula vaciar un array de enteros en Python.

    :return: una tupla con una lista vacía y el valor 0 representando el nuevo tamaño.
    """
    return [], 0



def potencia_lineal(base, exponente):
    """
    Calcula la potencia de un número de forma lineal usando un bucle.

    :param base: base de la potencia.
    :param exponente: exponente al que elevar la base (entero no negativo).
    :return: resultado de base elevado a exponente.
    """
    resultado = 1
    for _ in range(exponente):
        resultado *= base
    return resultado


def potencia_recursiva(base, exponente):
    """
    Calcula la potencia de un número de forma recursiva.

    :param base: base de la potencia.
    :param exponente: exponente al que se eleva la base.
    :return: resultado de base^exponente.
    """
    if exponente == 0:
        return 1
    return base * potencia_recursiva(base, exponente - 1)




def potencia_rapida(base, exponente):
    """
    Calcula la potencia de un número usando exponenciación rápida.

    :param base: base de la potencia.
    :param exponente: exponente al que se eleva la base.
    :return: resultado de base^exponente calculado eficientemente.
    """
    if exponente == 0:
        return 1
    half = potencia_rapida(base, exponente // 2)
    if exponente % 2 == 0:
        return half * half
    else:
        return half * half * base



def tiempo_recursivo_a1(n):
    """
    Simula el tiempo de ejecución de un algoritmo recursivo con la relación:
    T(n) = 2T(n-1) + 3T(n-2) + operaciones cuadráticas.

    :param n: tamaño del problema.
    :return: tiempo simulado de ejecución.
    """
    if n < 5:
        return 1
    tiempo_division = 3 * n * n
    tiempo_recursivo = 2 * tiempo_recursivo_a1(n - 1) + 3 * tiempo_recursivo_a1(n - 2)
    tiempo_combinacion = 2 * n
    return tiempo_division + tiempo_recursivo + tiempo_combinacion



# Calcula el factorial de un número entero no negativo.
# - n: entero mayor o igual a 0.
# Devuelve el valor de n! (factorial de n). Usa recursión.
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)




def tiempo_recursivo_a2(n):
    """
    Simula un coste de tiempo para un algoritmo con división en subproblemas fraccionarios.

    :param n: tamaño del problema.
    :return: tiempo simulado de ejecución basado en la relación:
             T(n) = n^2·log(n) + 2·T(n/2) + T(n/3), o factorial para n < 5.
    """
    if n < 5:
        return factorial(n)
    tiempo_div_comb = n * n * math.log(n)
    tiempo_recursivo = 2 * tiempo_recursivo_a2(n // 2) + tiempo_recursivo_a2(n // 3)
    return tiempo_div_comb + tiempo_recursivo



def esta_vacio(vec):
    """
    Comprueba si una lista está vacía.

    :param vec: lista a verificar.
    :return: True si la lista está vacía, False en caso contrario.
    """
    return len(vec) == 0




def busqueda_binaria_rec(A, izq, der, x):
    """
    Realiza búsqueda binaria recursiva en una lista ordenada.

    :param A: lista ordenada donde buscar.
    :param izq: índice izquierdo del rango de búsqueda.
    :param der: índice derecho del rango de búsqueda.
    :param x: valor a buscar.
    :return: índice del valor si se encuentra, o -1 si no está presente.
    """
    if izq > der:
        return -1
    medio = (izq + der) // 2
    if A[medio] == x:
        return medio
    elif A[medio] > x:
        return busqueda_binaria_rec(A, izq, medio - 1, x)
    else:
        return busqueda_binaria_rec(A, medio + 1, der, x)




def busqueda_binaria_primera(A, izq, der, x):
    """
    Busca la primera aparición de un valor en una lista ordenada usando búsqueda binaria.

    :param A: lista ordenada donde buscar.
    :param izq: índice izquierdo del rango de búsqueda.
    :param der: índice derecho del rango de búsqueda.
    :param x: valor a buscar.
    :return: índice de la primera aparición de x si se encuentra, o -1 si no está presente.
    """
    if izq > der:
        return -1
    medio = (izq + der) // 2
    if A[medio] == x and (medio == izq or A[medio - 1] != x):
        return medio
    elif A[medio] >= x:
        return busqueda_binaria_primera(A, izq, medio - 1, x)
    else:
        return busqueda_binaria_primera(A, medio + 1, der, x)




def busqueda_binaria_interpolada(A, izq, der, x):
    """
    Realiza búsqueda binaria interpolada en una lista ordenada.
    Útil cuando los datos están distribuidos de manera uniforme.

    :param A: lista ordenada donde buscar.
    :param izq: índice izquierdo del rango de búsqueda.
    :param der: índice derecho del rango de búsqueda.
    :param x: valor a buscar.
    :return: índice del valor si se encuentra, o -1 si no está presente o fuera de rango.
    """
    if izq > der or x < A[izq] or x > A[der]:
        return -1
    if A[der] == A[izq]:
        pos = (izq + der) // 2
    else:
        pos = izq + ((x - A[izq]) * (der - izq)) // (A[der] - A[izq])
    if pos < izq or pos > der:
        pos = (izq + der) // 2
    if A[pos] == x:
        return pos
    elif A[pos] > x:
        return busqueda_binaria_interpolada(A, izq, pos - 1, x)
    else:
        return busqueda_binaria_interpolada(A, pos + 1, der, x)




def ordenacion_insercion(A, izq, der):
    """
    Ordena una lista de enteros en el rango [izq, der] usando inserción directa.

    :param A: lista de enteros a ordenar.
    :param izq: índice inicial del subarreglo.
    :param der: índice final del subarreglo.
    """
    for i in range(izq + 1, der + 1):
        clave = A[i]
        j = i - 1
        while j >= izq and A[j] > clave:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = clave




def merge(A, izq, medio, der):
    """
    Fusiona dos subarreglos adyacentes de A en orden:
      - primer subarreglo: A[izq..medio]
      - segundo subarreglo: A[medio+1..der]

    :param A: lista de enteros a ordenar.
    :param izq: índice inicial del primer subarreglo.
    :param medio: índice final del primer subarreglo.
    :param der: índice final del segundo subarreglo.
    :return: nada, modifica A in-place fusionando ambos subarreglos ordenadamente.
    """
    tmp = []
    i, j = izq, medio + 1

    # Fusionar mientras haya elementos en ambas mitades
    while i <= medio and j <= der:
        if A[i] < A[j]:
            tmp.append(A[i])
            i += 1
        else:
            tmp.append(A[j])
            j += 1

    # Copiar restos del primer subarreglo
    while i <= medio:
        tmp.append(A[i])
        i += 1

    # Copiar restos del segundo subarreglo
    while j <= der:
        tmp.append(A[j])
        j += 1

    # Reemplazar A[izq..der] con tmp
    for p, val in enumerate(tmp):
        A[izq + p] = val






def merge_sort(A, izq, der):
    """
    Ordena una lista en el rango [izq, der] usando el algoritmo Merge Sort (divide y vencerás).

    :param A: lista de enteros a ordenar.
    :param izq: índice inicial del subarreglo.
    :param der: índice final del subarreglo.
    """
    if izq < der:
        medio = (izq + der) // 2
        merge_sort(A, izq, medio)
        merge_sort(A, medio + 1, der)
        merge(A, izq, medio, der)





def merge_sort_hibrido(A, izq, der, k):
    """
    Merge Sort híbrido: si el tamaño del subarreglo es <= k, usa inserción directa, 
    en caso contrario sigue recursivamente con Merge Sort.

    :param A: lista de enteros a ordenar.
    :param izq: índice inicial del subarreglo.
    :param der: índice final del subarreglo.
    :param k: umbral para cambiar a inserción directa cuando el subarreglo es pequeño.
    """
    if der - izq + 1 <= k:
        ordenacion_insercion(A, izq, der)
    else:
        medio = (izq + der) // 2
        merge_sort_hibrido(A, izq, medio, k)
        merge_sort_hibrido(A, medio + 1, der, k)
        merge(A, izq, medio, der)






def guardar_vector_en_archivo(vec, nombre_archivo):
    """
    Guarda los valores de una lista de enteros en un archivo de texto,
    uno por línea.

    :param vec: lista de enteros a guardar.
    :param nombre_archivo: nombre del archivo donde se escribirán los valores.
    """
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        for val in vec:
            f.write(f"{val}\n")





def medir_tiempo_ejecucion(f):
    """
    Mide el tiempo de ejecución de la función f (sin argumentos)
    y devuelve la duración en microsegundos.
    """
    t0 = time.perf_counter()
    f()
    t1 = time.perf_counter()
    # time.perf_counter devuelve segundos en coma flotante
    return (t1 - t0) * 1_000_000  # convertir a microsegundos




def guardar_resultados_csv(datos, nombre_archivo):
    """
    Guarda una lista de valores flotantes en un archivo CSV, formateando los decimales
    con coma y usando ';' como separador. Cada valor se escribe en una línea separada.

    :param datos: lista de floats a guardar.
    :param nombre_archivo: nombre del archivo CSV de destino.
    """
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        for valor in datos:
            # Formatear con 6 decimales y cambiar '.' → ','
            s = f"{valor:.6f}".replace('.', ',')
            f.write(f"{s};\n")




def contar_operaciones_busqueda(v, valor):
    """
    Realiza búsqueda lineal en una lista y cuenta el número de operaciones realizadas:
      - incremento por cada iteración del bucle.
      - acceso a v[i].
      - comparación (éxito o fracaso).

    :param v: lista donde se hace la búsqueda.
    :param valor: valor a buscar en la lista.
    :return: tupla (posición, operaciones):
             - posición: índice del valor en la lista, o -1 si no se encuentra.
             - operaciones: número total de operaciones contadas durante la búsqueda.
    """
    operaciones = 0
    for i, elem in enumerate(v):
        operaciones += 1  # por el bucle (i)
        operaciones += 1  # acceso a v[i]
        if elem == valor:
            operaciones += 1  # comparación éxito
            return i, operaciones
        operaciones += 1  # comparación fallida
    return -1, operaciones




def formatear_decimal_para_excel(valor):
    """
    Formatea un número flotante con 6 decimales y reemplaza el punto decimal por coma,
    para compatibilidad con hojas de cálculo que usan coma como separador decimal.

    :param valor: número flotante a formatear.
    :return: cadena con el número formateado (seis decimales) y punto cambiado por coma.
    """
    s = f"{valor:.6f}"
    return s.replace('.', ',')



def split(s: str, delim: str) -> List[str]:
    """
    Divide una cadena en tokens separándola por un delimitador dado.
    - s: cadena de entrada.
    - delim: carácter delimitador.
    Devuelve una lista de strings con los tokens resultantes.
    """
    return s.split(delim)


def trim(s: str) -> str:
    """
    Elimina espacios en blanco al inicio y al final de una cadena.
    - s: cadena de entrada.
    Devuelve una nueva cadena sin espacios en los extremos.
    """
    return s.strip()


def to_uppercase(s: str) -> str:
    """
    Convierte todos los caracteres de una cadena a mayúsculas.
    - s: cadena de entrada.
    Devuelve la cadena transformada en mayúsculas.
    """
    return s.upper()


def to_lowercase(s: str) -> str:
    """
    Convierte todos los caracteres de una cadena a minúsculas.
    - s: cadena de entrada.
    Devuelve la cadena transformada en minúsculas.
    """
    return s.lower()


def replace_all(s: str, old: str, new: str) -> str:
    """
    Reemplaza todas las ocurrencias de un substring por otro.
    - s: cadena de entrada.
    - old: substring a buscar.
    - new: substring de reemplazo.
    Devuelve la nueva cadena con los reemplazos realizados.
    """
    return s.replace(old, new)


def starts_with(s: str, prefix: str) -> bool:
    """
    Comprueba si una cadena comienza con un prefijo dado.
    - s: cadena de entrada.
    - prefix: prefijo a comprobar.
    Devuelve True si 's' comienza con 'prefix', False en caso contrario.
    """
    return s.startswith(prefix)


def ends_with(s: str, suffix: str) -> bool:
    """
    Comprueba si una cadena termina con un sufijo dado.
    - s: cadena de entrada.
    - suffix: sufijo a comprobar.
    Devuelve True si 's' termina con 'suffix', False en caso contrario.
    """
    return s.endswith(suffix)


def existe_archivo(ruta: str) -> bool:
    """
    Comprueba si un archivo o directorio existe en el sistema.
    - ruta: cadena con la ruta al archivo o directorio.
    Devuelve True si existe, False en caso contrario.
    """
    return pathlib.Path(ruta).exists()


def leer_fichero_texto(nombre_archivo: str) -> str:
    """
    Lee el contenido completo de un fichero de texto.
    - nombre_archivo: ruta al archivo de texto.
    Devuelve un string con todo el contenido del fichero.
    """
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        return f.read()


def escribir_texto_en_fichero(nombre_archivo: str, texto: str) -> None:
    """
    Escribe un texto completo en un fichero, sobrescribiendo si existe.
    - nombre_archivo: ruta al archivo de salida.
    - texto: contenido que se escribirá en el fichero.
    Si no se puede abrir el archivo, lanza RuntimeError.
    """
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(texto)
    except Exception as e:
        raise RuntimeError(f"No se pudo abrir {nombre_archivo} para escritura: {e}")


def obtener_extension(ruta: str) -> str:
    """
    Obtiene la extensión de un archivo (incluido el punto).
    - ruta: cadena con la ruta al archivo.
    Devuelve un string con la extensión (p. ej., ".txt"), o cadena vacía si no tiene.
    """
    return pathlib.Path(ruta).suffix


def obtener_nombre_sin_extension(ruta: str) -> str:
    """
    Obtiene el nombre de archivo sin la extensión.
    - ruta: cadena con la ruta al archivo.
    Devuelve un string con el nombre sin extensión.
    """
    return pathlib.Path(ruta).stem


def unir_rutas(base: str, subruta: str) -> str:
    """
    Une dos rutas de sistema garantizando separador correcto.
    - base: ruta base.
    - subruta: subruta o archivo a anexar.
    Devuelve la ruta combinada.
    """
    return str(pathlib.Path(base) / pathlib.Path(subruta))



def mcd(a: int, b: int) -> int:
    """
    Calcula el máximo común divisor (MCD) de dos enteros.
    - a, b: enteros de entrada (no negativos).
    Devuelve gcd(a, b).
    """
    return math.gcd(a, b)


def mcm(a: int, b: int) -> int:
    """
    Calcula el mínimo común múltiplo (MCM) de dos enteros.
    - a, b: enteros de entrada (no negativos).
    Devuelve lcm(a, b).
    """
    # math.lcm está disponible en Python 3.9+
    try:
        return math.lcm(a, b)
    except AttributeError:
        return abs(a * b) // math.gcd(a, b)


def es_primo(n: int) -> bool:
    """
    Comprueba si un número es primo usando método sencillo.
    - n: entero a comprobar.
    Devuelve True si n es primo (>1), False en caso contrario.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def potencia_mod(base: int, exponente: int, mod: int) -> int:
    """
    Calcula base^exponente mod módulo de forma rápida.
    - base: número base.
    - exponente: exponente (>= 0).
    - mod: módulo (> 0).
    Devuelve (base^exponente) % mod.
    """
    return pow(base, exponente, mod)



def uf_init(n: int) -> Tuple[List[int], List[int]]:
    """
    Inicializa las estructuras de datos para Union-Find (Disjoint Set).
    - n: número de elementos (0..n-1).
    Devuelve una tupla (padre, rango):
      - padre: lista donde padre[i] = i inicialmente.
      - rango: lista de ceros del mismo tamaño.
    """
    padre = list(range(n))
    rango = [0] * n
    return padre, rango


def uf_find(padre: List[int], x: int) -> int:
    """
    Encuentra el representante (raíz) del conjunto al que pertenece x.
    Aplica compresión de caminos.
    - padre: lista de padres del Union-Find.
    - x: índice del elemento.
    Devuelve la raíz del conjunto.
    """
    if padre[x] != x:
        padre[x] = uf_find(padre, padre[x])
    return padre[x]


def uf_unite(padre: List[int], rango: List[int], a: int, b: int) -> None:
    """
    Une los conjuntos que contienen a 'a' y 'b' (por rango).
    - padre: lista de padres del Union-Find.
    - rango: lista de rangos por cada elemento.
    - a, b: índices de los elementos a unir.
    Si ya están en el mismo conjunto, no hace nada.
    """
    ra = uf_find(padre, a)
    rb = uf_find(padre, b)
    if ra == rb:
        return
    if rango[ra] < rango[rb]:
        padre[ra] = rb
    elif rango[ra] > rango[rb]:
        padre[rb] = ra
    else:
        padre[rb] = ra
        rango[ra] += 1


def measure_time(func: callable, *args, **kwargs) -> Tuple[Any, float]:
    """
    Mide el tiempo de ejecución de una función en segundos.
    - func: función o callable sin valor de retorno fijo.
    - *args, **kwargs: argumentos para pasar a la función.
    Devuelve una tupla (resultado, tiempo) donde:
      - resultado: valor devuelto por func(*args, **kwargs).
      - tiempo: duración en segundos como float.
    """
    inicio = time.time()
    resultado = func(*args, **kwargs)
    fin = time.time()
    dur = fin - inicio
    return resultado, dur


def string_format(fmt: str, *args: Any, **kwargs: Any) -> str:
    """
    Función string_format estilo formato con llaves que devuelve str.
    - fmt: cadena de formato, usa {} para posicionales o {nombre} para keyword args.
    - args, kwargs: argumentos a formatear.
    Devuelve un string con el resultado formateado.
    Ejemplo:
        string_format("Hola {}, tienes {} mensajes", "Juan", 5)
    """
    try:
        return fmt.format(*args, **kwargs)
    except Exception as e:
        raise ValueError(f"Error en string_format con formato '{fmt}': {e}")




def es_potencia_de_dos(x: int) -> bool:
    """
    Comprueba si un entero es potencia de dos.
    - x: entero a comprobar (>0).
    Devuelve True si x es potencia de dos, False en caso contrario.
    """
    return x > 0 and (x & (x - 1)) == 0


def popcount(x: int) -> int:
    """
    Cuenta el número de bits a 1 en un entero (popcount).
    - x: entero a analizar (>=0).
    Devuelve el número de bits con valor 1.
    """
    return bin(x).count('1')


def texto_coordenadas(pos):
    """convierte coordenadas de ajedrez a coordenadas reales e2=>(6,4)"""
    col=ord(pos[0]) - ord("a")
    fila=8-int(pos[1])
    return fila,col

def coordenadas_texto(fila,col):
    """convierte coordenadas reales a texto (6,4)=>e2"""
