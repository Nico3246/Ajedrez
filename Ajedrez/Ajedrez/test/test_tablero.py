# test/test_tablero.py
import pytest
from Tablero import Tablero

def test_initial_layout_and_clear():
    t = Tablero()
    # filas 0 y 1 deben contener piezas negras
    assert t.tablero[0] == ['r','n','b','q','k','b','n','r']
    assert all(p=='p' for p in t.tablero[1])
    # filas 6 y 7 blancas
    assert t.tablero[7] == ['R','N','B','Q','K','B','N','R']
    assert all(p=='P' for p in t.tablero[6])
    # no haya None, usa ' ' para vacías
    for r in range(2,6):
        assert all(c == ' ' for c in t.tablero[r])
