import pytest
from ComprobarMovFichas import mover_valido

@pytest.mark.parametrize("pieza, origen, destino, color, ok", [
    ("P", (6,4), (5,4), "blanco", True),
    ("P", (6,4), (4,4), "blanco", True),
    ("P", (6,4), (5,5), "blanco", False),
    ("p", (1,3), (2,3), "negro", True),
    ("p", (1,3), (3,3), "negro", True),
    ("p", (1,3), (2,2), "negro", False),
    ("N", (7,1), (5,2), "blanco", True),
    ("N", (7,1), (6,3), "blanco", True),
    ("N", (7,1), (7,2), "blanco", False),
    ("R", (4,4), (4,7), "blanco", True),
    ("R", (4,4), (1,4), "blanco", True),
    ("R", (4,4), (4,6), "blanco", False),
    ("B", (4,4), (7,7), "blanco", True),
    ("B", (4,4), (2,2), "blanco", True),
    ("B", (4,4), (1,7), "blanco", False),
    ("Q", (4,4), (4,7), "blanco", True),
    ("Q", (4,4), (7,7), "blanco", True),
    ("Q", (4,4), (5,6), "blanco", False),
    ("K", (4,4), (5,5), "blanco", True),
    ("K", (4,4), (4,6), "blanco", False),
])
def test_mover_valido(pieza, origen, destino, color, ok):
    board = [[None]*8 for _ in range(8)]
    board[origen[0]][origen[1]] = pieza
    # Coloca una pieza aliada para el caso especial del caballo bloqueado
    if pieza.upper() == 'N' and origen == (7,1) and destino == (7,2) and not ok:
        board[7][2] = 'N'
    # Bloqueo para piezas de largo alcance
    dr = destino[0] - origen[0]
    dc = destino[1] - origen[1]
    if not ok and pieza.upper() in ('R','B','Q') and max(abs(dr), abs(dc)) > 1:
        ir = origen[0] + (dr // max(1, abs(dr)))
        ic = origen[1] + (dc // max(1, abs(dc)))
        board[ir][ic] = 'X'
    assert mover_valido(pieza.lower(), origen, destino, board, color) == ok
