from ComprobarMovFichas import mover_valido


class Estado:
    def __init__(self,tablero):
        self.tablero = tablero
        self.turnoBlanco = True
        self.turnoNegro = False


    def jugadorActual(self):
        if self.turnoBlanco == True:
            return "blanco"
        else:
            return "negro"


    def colorPieza(self,pieza):
        if pieza is None:
            return None

        if pieza.isupper():
            return "blanco"
        else:
            return "negro"


    def tipoPieza(self,pieza):
        letras={
            'P': 'peon', 'N': 'caballo', 'B': 'alfil', 'R': 'torre', 'Q': 'reina', 'K': 'rey',
            'p': 'peon', 'n': 'caballo', 'b': 'alfil', 'r': 'torre', 'q': 'reina', 'k': 'rey'
        }
        return letras.get(pieza)

    def sucesores(self):
        lista=[]
        jugador = self.jugadorActual()

        for fila in range(8):
            for col in range(8):
                pieza = self.tablero.tablero[fila][col]
                if pieza is None or self.colorPieza(pieza) != jugador:
                    continue
                tipo = self.tipoPieza(pieza)

                for df in range(8):
                    for dc in range(8):
                        if df==fila and dc == col:
                            continue
                        if not mover_valido(tipo,(fila,col),(df,dc),self.tablero.tablero,jugador):
                            continue

                        #crear nuevo tablero y guardar la copia
                        nuevoTablero=self.tablero.clone()
                        nuevoTablero.tablero[df][dc]=pieza
                        nuevoTablero.tablero[fila][col]=None

                        nuevoEstado=Estado(nuevoTablero)
                        nuevoEstado.turnoBlanco = not self.turnoBlanco
                        nuevoEstado.turnoNegro = not self.turnoNegro

                        #guardar sucesores
                        lista.append((nuevoEstado,(fila,col,df,dc)))

        return lista


    def terminado(self):
        board = self.tablero.tablero
        plano=sum(board, [])
        return not any(p=="K" for p in plano) or not any(p=="k" for p in plano)


    def ganador(self,fichaIa):
        hayReyBlanco = any(pieza == "K" for fila in self.tablero.tablero for pieza in fila)

        hayReyNegro = any(pieza == "k" for fila in self.tablero.tablero for pieza in fila)

        if not hayReyBlanco:
            if fichaIa=="negro":
                return 1
            else:
                return -1

        if not hayReyNegro:
            if fichaIa=="blanco":
                return 1
            else:
                return -1

        return 0

    def jugada(self,origen,destino):
        """
        Aplica el movimiento (origen, destino) directamente en self.tablero
        y alterna el turno.
        origen: (fila, col)
        destino: (fila, col)
        """
        pieza = self.tablero.tablero[origen[0]][origen[1]]
        self.tablero.tablero[destino[0]][destino[1]] = pieza
        self.tablero.tablero[origen[0]][origen[1]] = None
        #cambiar turno
        self.turnoBlanco = not self.turnoBlanco

    def sucesores_para(self,color):
        """
        Genera los sucesores como si fuese el turno de `color`,
        pero sin modificar para siempre self.turnoBlanco.
        """
        orig = self.turnoBlanco
        # Ponemos el turno “virtual”
        self.turnoBlanco = (color == "blanco")
        lst = self.sucesores()          # genera sucesores usando ese turno
        self.turnoBlanco = orig        # restauramos el turno original
        return lst

    def cambiarturno(self):
        """
        Invierte el turno de juego.
        Después de llamar a este método, jugadorActual() cambiará
        de 'blanco' a 'negro' o viceversa.
        """
        self.turnoBlanco = not self.turnoBlanco
        # Si quieres mantener también sincronizado turnoNegro:
        self.turnoNegro = not self.turnoNegro


















