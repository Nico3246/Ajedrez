import pytest
from ComprobarMovFichas import mover_valido

@pytest.mark.parametrize("origen,destino,color,esperado", [
    # Avances válidos
    ((6,4),(5,4),'blanco',True),
    ((6,4),(4,4),'blanco',True),
    ((1,3),(2,3),'negro',True),
    ((1,3),(3,3),'negro',True),
    # Avances no válidos
    ((6,4),(3,4),'blanco',False),
    ((1,3),(4,3),'negro',False),
    # Captura válida solo si hay enemigo
    ((6,4),(5,5),'blanco',False),
    ((1,3),(2,2),'negro',False),
])
def test_peon_simple(origen, destino, color, esperado):
    tablero = [[None]*8 for _ in range(8)]
    fila_o, col_o = origen
    tablero[fila_o][col_o] = 'P' if color == 'blanco' else 'p'
    # Para probar captura, pon enemigo en destino
    if (abs(destino[1] - col_o) == 1) and ((destino[0] - fila_o) == (-1 if color == 'blanco' else 1)):
        if esperado:
            tablero[destino[0]][destino[1]] = 'p' if color == 'blanco' else 'P'
    assert mover_valido(tablero[fila_o][col_o].lower(), origen, destino, tablero, color) == esperado
