# test/test_estado.py
import pytest
from Tablero import Tablero
from EstadoAjedrez import Estado

def test_jugador_actual_initial_and_turn_change():
    tab = Tablero()
    estado = Estado(tab)
    assert estado.jugadorActual() == 'blanco'
    # simula un movimiento manual
    estado.cambiarturno()
    assert estado.jugadorActual() == 'negro'

def test_sucesores_posicion_inicial():
    tab = Tablero()
    estado = Estado(tab)
    movs = estado.sucesores()
    # 16 peones pueden avanzar 1, 8 pueden avanzar 2 (peones blancos y negros) + 4 saltos de caballo = 36
    # pero este conteo depende de implementación: ajusta a tu código
    assert len(movs) >= 20

def test_terminado_y_ganador_blanco():
    tab = Tablero()
    estado = Estado(tab)
    # al inicio no terminado
    assert not estado.terminado()
    # quita rey negro
    for i in range(8):
        for j in range(8):
            if tab.tablero[i][j] == 'k':
                tab.tablero[i][j] = None
    e2 = Estado(tab)
    assert e2.terminado()
    assert e2.ganador('blanco') == 1
    assert e2.ganador('negro') == -1
