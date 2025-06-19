# jugar.py

from Tablero import Tablero
from EstadoAjedrez import Estado
from Humano import Humano
from AlfaBeta import AlfaBeta

def jugarAjedrezHumanoVsHumano():
    tablero = Tablero()
    estado  = Estado(tablero)
    j1 = Humano(estado, "blanco")
    j2 = Humano(estado, "negro")
    while not estado.terminado():
        tablero.pintar()
        if estado.jugadorActual() == "blanco":
            j1.hacerJugada()
        else:
            j2.hacerJugada()
    tablero.pintar()
    print("¡Fin del juego!")

def jugarAjedrezHumanoVsIA():
    tablero = Tablero()
    estado  = Estado(tablero)
    humano   = Humano(estado, "blanco")
    ia       = AlfaBeta(estado, "negro")
    while not estado.terminado():
        tablero.pintar()
        if estado.jugadorActual() == "blanco":
            humano.hacerJugada()
        else:
            ia.hacerJugada()
    tablero.pintar()
    ganador = estado.ganador("blanco")
    if ganador == 1:
        print("Ganan las blancas")
    elif ganador == -1:
        print("Ganan las negras")
    else:
        print("Tablas")
