# test/test_alfabeta.py
import pytest
from Tablero import Tablero
from EstadoAjedrez import Estado
from AlfaBeta import AlfaBeta

def test_alfabeta_makes_valid_move_depth1():
    tab = Tablero()
    estado = Estado(tab)
    ia = AlfaBeta(estado, 'blanco', max_depth=1)
    ia.hacerJugada()
    assert estado.jugadorActual() == 'negro'
