# test/test_integration.py
import pytest
from Tablero import Tablero
from EstadoAjedrez import Estado
from funciones import texto_coordenadas

def test_integration_e2_e4_and_turn():
    tab = Tablero()
    estado = Estado(tab)
    f1,c1 = texto_coordenadas('e2')
    f2,c2 = texto_coordenadas('e4')
    suces = estado.sucesores()
    movimientos = [m for _,m in suces]
    assert (f1,c1,f2,c2) in movimientos
    # aplica jugada
    estado.jugada((f1,c1),(f2,c2))
    assert estado.tablero.tablero[f2][c2] == 'P'
    assert estado.tablero.tablero[f1][c1] is None
    assert estado.jugadorActual() == 'negro'

def test_knight_g1_f3_not_blocked():
    tab = Tablero()
    estado = Estado(tab)
    f1,c1 = texto_coordenadas('g1')
    f2,c2 = texto_coordenadas('f3')
    suces = estado.sucesores()
    assert (f1,c1,f2,c2) in [m for _,m in suces]
