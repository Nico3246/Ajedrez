
BOARD_SIZE = 8


class Tablero:
    def __init__(self):
        # crea un tablero vacío de tamaño BOARD_SIZE x BOARD_SIZE
        self.tablero = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.colocarFichas()

    def pintar(self,lineaGanadora=None):#muestra el tablero la linea ganadora sera la que se pinte en rojo
        # 1) Cabecera columnas con ancho fijo 3
        cols = "   " + "".join(f"{c:^3}" for c in "abcdefgh")
        print(cols)

        # 2) Cada fila
        for i, fila in enumerate(self.tablero):
            rank = 8 - i
            piezas = []
            for c in fila:
                ch = c if c is not None else '.'
                piezas.append(f"{ch:^3}")
            piezas = "".join(piezas)
            print(f"{rank} {piezas} {rank}")

        # 3) Pie idéntico a la cabecera
        print(cols)

    def colocarFichas(self):
        #colocar negras
        self.tablero[0] = ['r','n','b','q','k','b','n','r']
        self.tablero[1] = ['p']*8

        #colocar blancas
        self.tablero[6] = ['P'] * 8
        self.tablero[7] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

    def clone(self):
        nuevo = Tablero()
        nuevo.tablero = [fila[:] for fila in self.tablero]
        return nuevo












