import time
class AlfaBeta:
    # 1) Valores de material (centipawns)
    VALOR_PIEZA = {
        'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
        'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000
    }

    # 2) Piece‐Square Tables (ejemplo; 64 valores fila-major)
    PST_PAWN = [
        0, 5, 5, -10, -10, 5, 5, 0,
        5, 10, 10, 0, 0, 10, 10, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, 5, 10, 25, 25, 10, 5, 5,
        10, 10, 20, 30, 30, 20, 10, 10,
        20, 20, 30, 35, 35, 30, 20, 20,
        50, 50, 50, 50, 50, 50, 50, 50,
        0, 0, 0, 0, 0, 0, 0, 0
    ]
    PST_KNIGHT = [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    ]
    PST_BISHOP = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    ]
    PST_ROOK = [
        0, 0, 0, 5, 5, 0, 0, 0,
        5, 10, 10, 10, 10, 10, 10, 5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        0, 0, 0, 5, 5, 0, 0, 0
    ]
    PST_QUEEN = [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
    ]
    PST_KING_MG = [
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        20, 20, 0, 0, 0, 0, 20, 20,
        20, 30, 10, 0, 0, 10, 30, 20
    ]
    PST_KING_EG = [
        -50, -40, -30, -20, -20, -30, -40, -50,
        -30, -20, -10, 0, 0, -10, -20, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -30, 0, 0, 0, 0, -30, -30,
        -50, -30, -30, -30, -30, -30, -30, -50
    ]


    def __init__(self, estado,color,max_depth=3):
            self.estado = estado
            self.color = color
            self.max_depth = max_depth


    def evaluar(self,estado):#heuristica
        """Evalúa un estado: material + PST + estructura + seguridad + centro + movilidad + actividad rey."""
        board=estado.tablero.tablero
        score=0

        for r in range(8):
            for c in range(8):
                pieza=board[r][c]
                if pieza is None:
                    continue
                #material
                score += self.VALOR_PIEZA.get(pieza, 0)
                #PST
                idx = r*8 + c
                if(pieza.isupper() and self.color == "blanco") or (pieza.islower() and self.color == "negro"):
                    signo = 1
                else:
                    signo = -1

                up= pieza.upper()
                if up == 'P':
                    score += signo * self.PST_PAWN[idx]
                elif up == 'N':
                    score += signo * self.PST_KNIGHT[idx]
                elif up == 'B':
                    score += signo * self.PST_BISHOP[idx]
                elif up == 'R':
                    score += signo * self.PST_ROOK[idx]
                elif up == 'Q':
                    score += signo * self.PST_QUEEN[idx]
                elif up == 'K':
                    if self.esFinal(board):
                        score += signo * self.PST_KING_EG[idx]
                    else:
                        score += signo * self.PST_KING_MG[idx]

        #estructura peones
        score += self.evalPeones(board)
        #Seguridad del rey
        score += self.evalSeguridadRey(board)
        #control del centro
        for(r,c) in [(3,3),(3,4),(4,3),(4,4)]:
            pieza=board[r][c]
            if pieza is None:
                continue
            if (pieza.isupper() and self.color == "blanco") or (pieza.islower() and self.color=="negro"):
                signo = 1
            else:
                signo = -1
            score += 20 * signo

        #movilidad (generamos sucesores “virtuales” para cada bando)
        mi_moves = len(estado.sucesores_para(self.color))
        otro = "negro" if self.color == "blanco" else "blanco"
        op_moves = len(estado.sucesores_para(otro))
        score += 10 * (mi_moves - op_moves)


        #actividad del rey en el final
        if self.esFinal(board):
            score += self.evalActividadRey(board)

        return score


    def evalPeones(self,board):
        """Penaliza peones aislados y premia peones pasados."""
        val = 0
        friendly = 'P' if self.color == 'blanco' else 'p'
        enemy = 'p' if self.color == 'blanco' else 'P'
        for c in range(8):
            for r in range(8):
                if board[r][c] == friendly:
                    # aislado
                    cols = [c - 1, c + 1]
                    if all(not (0 <= c2 < 8 and any(board[r2][c2] == friendly for r2 in range(8))) for c2 in cols):
                        val -= 15
                    # pasado
                    ahead = range(r - 1, -1, -1) if self.color == 'blanco' else range(r + 1, 8)
                    if all(board[r2][c] != enemy for r2 in ahead):
                        val += 20
        return val

    def evalSeguridadRey(self,board):
        """Cuenta peones amigos alrededor del rey."""
        val = 0
        # Definimos qué peón buscamos según el color
        pawn = 'P' if self.color == 'blanco' else 'p'
        king = 'K' if self.color == 'blanco' else 'k'

        # localizar coordenadas del rey
        rk = ck = None
        for r in range(8):
            for c in range(8):
                if board[r][c] == king:
                    rk, ck = r, c
                    break
            if rk is not None:
                break

        # contar peones en las 8 casillas adyacentes
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r2, c2 = rk + dr, ck + dc
                if 0 <= r2 < 8 and 0 <= c2 < 8 and board[r2][c2] == pawn:
                    val += 1

        return val

    def esFinal(self,board):
        """Detecta fase final por poco material restante (sin contar reyes)."""
        tot = 0
        for row in board:
            for p in row:
                if p is None or p.upper() == 'K':
                    continue
                tot += abs(self.VALOR_PIEZA.get(p, 0))
        return tot < 2000

    def evalActividadRey(self,board):
        """Premia que el rey esté centrado en el final."""
        val = 0
        king = 'K' if self.color == 'blanco' else 'k'
        for r in range(8):
            for c in range(8):
                if board[r][c] == king:
                    dist = abs(r - 3.5) + abs(c - 3.5)
                    val += int(20 - dist * 4)
        return val




    def AlfaBeta(self,estado,depth,alfa,beta,maximizar):

        if depth == 0 or estado.terminado():
            return self.evaluar(estado),None

        mejorJugada=None

        if maximizar:
            valor = float("-inf")
            for sucesor, jugada in estado.sucesores():
                puntos,_ = self.AlfaBeta(sucesor,depth-1,alfa,beta,False)
                if puntos > valor:
                    valor,mejorJugada = puntos,jugada
                alfa = max(alfa,valor)
                if alfa >= beta:
                    break
            return valor,mejorJugada

        else:
            valor = float("inf")
            for sucesor, jugada in estado.sucesores():
                puntos,_ = self.AlfaBeta(sucesor,depth-1,alfa,beta,True)
                if puntos < valor:
                    valor,mejorJugada = puntos,jugada
                beta = min(beta,valor)
                if beta <= alfa:
                    break
            return valor,mejorJugada



    def hacerJugada(self):
        """Calcula la mejor jugada y la aplica al estado."""
        maximizar = (self.estado.jugadorActual() == self.color)
        _, jugada = self.AlfaBeta(
            self.estado,
            self.max_depth,
            float("-inf"),
            float("inf"),
            maximizar
        )

        if jugada is None:
            return  # no hay movimientos posibles

        # jugada viene como (fila_origen, col_origen, fila_destino, col_destino)
        f1, c1, f2, c2 = jugada
        origen = (f1, c1)
        destino = (f2, c2)

        # aplica el movimiento y ya se encarga internamente de alternar el turno
        self.estado.jugada(origen, destino)

