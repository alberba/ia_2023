import copy

from practica1.agent import Agent, Estat
from ia_2022 import entorn
from practica1.entorn import Accio, SENSOR


class EstatMinimax(Estat):
    def __init__(self, filas_columnas, pare=None, alpha=float('-inf'), beta=float('inf'), seguents_accions=None):
        super().__init__(filas_columnas, pare)
        self.__utilidad = 0
        self.__heuristica = 4
        self.alpha = alpha
        self.beta = beta
        if seguents_accions is None:
            seguents_accions = []
        self.seguents_accions = seguents_accions


    def es_meta(self):
        return self.heuristica == 0
    
    def genera_fills(self, torn_de_max: bool) -> list['EstatMinimax']:
        estats_generats = []

        for columna in range(self.lenTablero):
            for fila in range(self.lenTablero):
                if self.tablero[columna][fila] == 0:
                    nou_estat = copy.deepcopy(self)
                    nou_estat.pare = (self, (columna, fila))
                    nou_estat.seguents_accions = [(columna, fila, 1)]

                    if torn_de_max:
                        nou_estat.tablero[columna][fila] = 1
                    else:
                        nou_estat.tablero[columna][fila] = 2

                    nou_estat.calcular_heuristica()
                    estats_generats.append(nou_estat)
        
        return estats_generats
    
    def calcular_heuristica (self):
        for columna in range(self.lenTablero):
            for fila in range(self.lenTablero):
                if self.tablero[columna][fila] == 1 or self.tablero[columna][fila] == 2:
                    h = self.mirar_combinacion(columna, fila)
                    if h < self.heuristica:
                        self.heuristica = h

    # Cuando encuentra una pieza colocada, comprueba las siguientes 3 casillas horizontalmente, diagonalmente y verticalmente 
    # para calcular la heuristica correspondiente
    def mirar_combinacion(self, columna, fila) -> int:
        heuristica_menor = 3
        heuristica_menor = min(heuristica_menor, self.mirar_combinacionColumnas(columna, fila), self.mirar_combinacionFilas(columna, fila),
                                self.mirar_combinacionDiagonalUp(columna, fila), self.mirar_combinacionDiagonalDown(columna, fila))
        return heuristica_menor
    
    def mirar_combinacionColumnas(self, columna: int, fila: int) -> int:
        heuristica = 3
        if columna + 3 < self.lenTablero:
            for i in range(columna + 1, columna + 4):
                if self.tablero[columna][fila] == self.tablero[i][fila] == 1:
                    heuristica -= 1
                elif self.tablero[columna][fila] != self.tablero[i][fila] and self.tablero[i][fila] != 0:
                    heuristica = 4
                    break

        return heuristica
                
    def mirar_combinacionFilas(self, columna: int, fila: int) -> int:
        heuristica = 3
        if fila + 3 < self.lenTablero:
            for j in range(fila + 1, fila + 4):
                if self.tablero[columna][fila] == self.tablero[columna][j]:
                    heuristica -= 1
                elif self.tablero[columna][fila] != self.tablero[columna][j] and self.tablero[columna][j] != 0:
                    heuristica = 4
                    break

        return heuristica
                
    def mirar_combinacionDiagonalDown(self, columna: int, fila: int) -> int:
        heuristica = 3
        if fila + 3 < self.lenTablero:
            if columna + 3 < self.lenTablero:
                for i in range(1, 4):
                    if self.tablero[columna][fila] == self.tablero[columna + i][fila + i]:
                        heuristica -= 1
                    elif self.tablero[columna][fila] != self.tablero[columna + i][fila + i] and self.tablero[columna + i][fila + i] != 0:
                        heuristica = 4
                        break

        return heuristica
    
    def mirar_combinacionDiagonalUp(self, columna: int, fila: int) -> int:
        heuristica = 3
        if fila - 3 >= 0:
            if columna + 3 < self.lenTablero:
                for i in range(1, 4):
                    if self.tablero[columna][fila] == self.tablero[columna + i][fila - i]:
                        heuristica -= 1
                    elif self.tablero[columna][fila] != self.tablero[columna + i][fila - i] and self.tablero[columna + i][fila - i] != 0:
                        heuristica = 4
                        break

        return heuristica
    
    @property
    def heuristica(self):
        return self.__heuristica
    
    @heuristica.setter
    def heuristica(self, heuristica):
        self.__heuristica = heuristica
    
    @property
    def utilidad(self):
        return self.__utilidad
    
    @utilidad.setter
    def utilidad(self, utilidad):
        self.__utilidad = utilidad

class AgentMinimax(Agent):
    def __init__(self, nom):
        super(AgentMinimax, self).__init__(nom)
        # Accions estará formado por una lista de acciones de manera cronológica estructurada de la siguiente forma:
        # [(columna, fila, fichaJugador), (columna, fila, fichaJugador), ...]
        self.__accions = None
        self.__puntuacio = 0

    def minimax(self, estat: EstatMinimax, torn_de_max: bool) -> int:
        if estat.es_meta():
            # Funciona al reves ya que tenemos en cuenta de que si en el estado actual el turno es de max y
            # la partida ha acabado, quiere decir que min ha ganado
            if not torn_de_max:
                estat.beta = 1
            else:
                estat.alpha = -1
            return None
        
        for estat_fill in estat.genera_fills(torn_de_max):
            self.minimax(estat_fill, not torn_de_max)
            if torn_de_max:
                # El turno del hijo es min y el del padre es max
                if estat.alpha < estat_fill.beta and not estat_fill.beta == float('inf'):
                    estat.alpha = estat_fill.beta
                    seguents_accions = estat_fill.seguents_accions
                if estat.alpha >= estat.beta:
                    # Poda ya que como el padre del padre es min, no va a elegir al padre
                    break
            else:
                # El turno del hijo es max y el del padre es min
                if estat.beta > estat_fill.alpha and not estat_fill.alpha == float('-inf'):
                    estat.beta = estat_fill.alpha
                    seguents_accions = estat_fill.seguents_accions
                if estat.alpha >= estat.beta:
                    # Podamos ya que como el padre del padre es max, no va a elegir al padre
                    break
            if estat.alpha != float('-inf') or  estat.beta != float('inf'):
                estat.seguents_accions.append(seguents_accions)
    
    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estat = EstatMinimax(percepcio[SENSOR.MIDA])
        
        if self.__accions is None:
            self.minimax(estat, True)
            self.__accions = estat.seguents_accions

        if self.__accions:
            accio = self.__accions.pop()[:2]
            return Accio.POSAR, accio
        else:
            return Accio.ESPERAR
