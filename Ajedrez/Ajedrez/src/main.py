from Tablero import Tablero
from EstadoAjedrez import Estado
from Humano import Humano
from AlfaBeta import AlfaBeta

def jugar_ajedrez_con_alfabeta():
    tablero = Tablero()
    estado = Estado(tablero)
    jugador_blanco = Humano(estado, "blanco")
    jugador_negro  = AlfaBeta(estado, "negro")

    while not estado.terminado():
        tablero.pintar()
        turno = estado.jugadorActual()
        print(f"\nTurno de {turno}")
        if turno == "blanco":
            jugador_blanco.hacerJugada()
        else:
            jugador_negro.hacerJugada()

    tablero.pintar()
    resultado = estado.ganador("blanco")
    if resultado == 1:
        print("Ganan las blancas")
    elif resultado == -1:
        print("Ganan las negras")
    else:
        print("Tablas")

if __name__ == "__main__":
    jugar_ajedrez_con_alfabeta()
