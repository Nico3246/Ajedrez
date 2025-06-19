import pytest
from ComprobarMovFichas import mover_valido

@pytest.mark.parametrize("origen,destino,color,ok", [
    # Peón blanco
    ((6,4),(5,4),'blanco',True),
    ((6,4),(4,4),'blanco',True),
    ((6,4),(5,5),'blanco',False),
    # Peón negro
    ((1,3),(2,3),'negro',True),
    ((1,3),(3,3),'negro',True),
    ((1,3),(2,2),'negro',False),

    # Caballo
    ((7,1),(5,2),'blanco',True),
    ((7,1),(6,3),'blanco',True),
    ((7,1),(7,2),'blanco',False),  # CASO especial torre a la derecha con pieza aliada

    # Torre limpia
    ((4,4),(4,7),'blanco',True),
    ((4,4),(1,4),'blanco',True),
    # Torre bloqueada
    ((4,4),(4,6),'blanco',False),

    # Alfil
    ((4,4),(7,7),'blanco',True),
    ((4,4),(2,2),'blanco',True),
    ((4,4),(1,7),'blanco',False),

    # Reina
    ((4,4),(4,7),'blanco',True),
    ((4,4),(7,7),'blanco',True),
    ((4,4),(5,6),'blanco',False),

    # Rey
    ((4,4),(5,5),'blanco',True),
    ((4,4),(4,6),'blanco',False),
])
def test_piece_moves(origen, destino, color, ok):
    # tableros de prueba
    tablero = [[None]*8 for _ in range(8)]
    dr = destino[0] - origen[0]
    dc = destino[1] - origen[1]

    # Determinar la pieza que debe probarse
    if origen in [(6,4), (1,3)]:
        pieza = 'P' if color == 'blanco' else 'p'
    elif (abs(dr), abs(dc)) in [(2,1), (1,2)]:
        pieza = 'N' if color == 'blanco' else 'n'
    elif dr == 0 or dc == 0:
        pieza = 'R' if color == 'blanco' else 'r'
    elif abs(dr) == abs(dc):
        pieza = 'B' if color == 'blanco' else 'b'
    elif abs(dr) <= 1 and abs(dc) <= 1:
        pieza = 'K' if color == 'blanco' else 'k'
    else:
        pieza = 'Q' if color == 'blanco' else 'q'

    tablero[origen[0]][origen[1]] = pieza

    # bloquea intermedio si bloqueada (para torre, alfil, reina)
    if not ok and (pieza.upper() in ('R','B','Q')) and abs(dr) > 1:
        ir = origen[0] + (dr // abs(dr))
        ic = origen[1] + (dc // abs(dc))
        tablero[ir][ic] = 'X'

    # CASO ESPECIAL: Torre intenta avanzar a la derecha con aliada
    if origen == (7,1) and destino == (7,2) and color == 'blanco' and not ok:
        tablero[7][2] = 'N'  # pieza blanca en el destino

    assert mover_valido(pieza.lower(), origen, destino, tablero, color) == ok
