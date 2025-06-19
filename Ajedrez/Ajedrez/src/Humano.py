from funciones import *
from ComprobarMovFichas import mover_valido

class Humano:
    def __init__(self,estado,ficha):
        self.estado = estado
        self.ficha=ficha


    def hacerJugada(self):
        while True:
            entrada = input(f"{self.ficha} mueve: ")
            try:
                origen_txt,destino_txt = entrada.split()
                f1,c1 = texto_coordenadas(origen_txt)
                f2,c2 = texto_coordenadas(destino_txt)
            except:
                print("Formato invalido. Usa: e2,e4...")
                continue

            tablero = self.estado.tablero.tablero
            tipo = self.estado.tipoPieza(tablero[f1][c1])
            if mover_valido(tipo, (f1,c1),(f2,c2), tablero, self.estado.jugadorActual()):
                self.estado.jugada((f1,c1),(f2,c2))
                break
            else:
                print("Movimiento no valido")





