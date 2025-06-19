def torre(posActual,posDestino):
    filaActual, columnActual = posActual
    filaDestino, columnDestino = posDestino

    if(filaActual == filaDestino or columnActual == columnDestino):
        return True
    else:
        return False

def alfil(posActual,posDestino):
    filaActual, columnActual = posActual
    filaDestino, columnDestino = posDestino

    if(abs(filaActual - filaDestino) ==  abs(columnActual - columnDestino)):#distancia horizontal igual a la distancia vertical
        return True
    else:
        return False

def caballo(posActual,posDestino):
    filaActual, columnActual = posActual
    filaDestino, columnDestino = posDestino

    x=abs(filaActual - filaDestino)
    y=abs(columnActual - columnDestino)

    if (x,y) in [(2,1),(1,2)]:#Se mueve 2 casillas en una dirección (fila o columna) y luego 1 casilla en la dirección perpendicular
        return True
    else:
        return False


def reina(posActual,posDestino):
    filaActual, columnActual = posActual
    filaDestino, columnDestino = posDestino

    if filaActual == filaDestino or columnActual == columnDestino:
        return True
    elif abs(filaActual - filaDestino) == abs(columnActual - columnDestino):
        return True
    else:
        return False

def rey(posActual,posDestino):
    filaActual, columnActual = posActual
    filaDestino, columnDestino = posDestino

    x=abs(filaActual - filaDestino)
    y=abs(columnActual - columnDestino)

    if (x <= 1 and y <= 1) and (x + y != 0):
        return True
    else:
        return False

def peon(origen, destino,color):
    filaActual, columnActual = origen
    filaDestino, columnDestino = destino

    direccion=-1 if color == "blanco" else 1
    filaInicio= 6 if color == "blanco" else 1

    if filaDestino - filaActual == direccion and columnActual == columnDestino:
        return True

    if filaActual == filaInicio and filaDestino-filaActual == 2*direccion and columnActual == columnDestino:
        return True

    return False


def caminoLibre(origen,destino,tablero):
    filaActual, columnActual = origen
    filaDestino, columnDestino = destino

    if filaActual != filaDestino:
        pasoFila=(filaDestino-filaActual) // max(1,abs(filaDestino-filaActual))
    else:
        pasoFila=0

    if columnActual != columnDestino:
        pasoColumna=(columnDestino-columnActual) // max(1,abs(columnDestino-columnActual))
    else:
        pasoColumna=0


    f,c = filaActual + pasoFila,columnActual + pasoColumna
    while(f,c)!=(filaDestino,columnDestino):
        if(tablero[f][c] is not None):
            return False
        f+=pasoFila
        c+=pasoColumna

    return True


def mover_valido(pieza, origen, destino, tablero, color):
    filaD, colD = destino
    destino_pieza = tablero[filaD][colD]

    # determinar color del destino, sea dict o str
    if isinstance(destino_pieza, dict):
        color_destino = destino_pieza.get('color')
    elif isinstance(destino_pieza, str) and destino_pieza.strip() != '':
        color_destino = 'blanco' if destino_pieza.isupper() else 'negro'
    else:
        color_destino = None

    # si hay aliada, no es válido
    if color_destino == color:
        return False

    mapping = {
        'p': 'peon',
        'n': 'caballo',
        'r': 'torre',
        'b': 'alfil',
        'q': 'reina',
        'k': 'rey'
    }
    pieza_tipo = mapping.get(pieza, pieza)  # si no está en mapping, asumimos que ya es nombre completo

    # Movimiento según tipo
    if pieza_tipo == "torre":
        if not torre(origen, destino): return False
        if not caminoLibre(origen, destino, tablero): return False
        return True

    elif pieza_tipo == "alfil":
        if not alfil(origen, destino): return False
        if not caminoLibre(origen, destino, tablero): return False
        return True

    elif pieza_tipo == "reina":
        if not reina(origen, destino): return False
        if not caminoLibre(origen, destino, tablero): return False
        return True

    elif pieza_tipo == "caballo":
        return caballo(origen, destino)

    elif pieza_tipo == "rey":
        return rey(origen, destino)

    elif pieza_tipo == "peon":
        filaA, colA = origen
        filaD, colD = destino
        direccion = -1 if color == "blanco" else 1
        filaInicio = 6 if color == "blanco" else 1

        # Avance simple
        if colA == colD:
            if filaD - filaA == direccion and tablero[filaD][colD] is None:
                return True
            if filaA == filaInicio and filaD - filaA == 2 * direccion:
                intermedia = filaA + direccion
                if tablero[intermedia][colD] is None and tablero[filaD][colD] is None:
                    return True
        # Captura diagonal
        elif abs(colD - colA) == 1 and filaD - filaA == direccion:
            # usa 'color_destino' ya calculado, no destino_pieza['color']
            if color_destino is not None and color_destino != color:
                return True
            else:
                return False

        return False

    else:
        raise ValueError(f"Pieza desconocida: {pieza}")








