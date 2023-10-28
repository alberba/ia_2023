import copy

from practica1.agent import Agent, Estat
from ia_2022 import entorn
from practica1.entorn import Accio, SENSOR


PROFUNDIDAD_MAXIMA = 4
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
                    nou_estat.seguents_accions = [(columna, fila, 1 if torn_de_max else 2)]

                    nou_estat.tablero[columna][fila] = 1 if torn_de_max else 2

                    nou_estat.calcular_heuristica()
                    estats_generats.append(nou_estat)
        
        return estats_generats
    
    def calcular_heuristica (self):
        # Reseteamos la utilidad
        self.utilidad = 0
        for columna in range(self.lenTablero):
            for fila in range(self.lenTablero):
                h = self.mirar_combinacion(columna, fila)
                if h < self.heuristica:
                    self.heuristica = h

    # Cuando encuentra una pieza colocada, comprueba las siguientes 3 casillas horizontalmente, diagonalmente y verticalmente 
    # para calcular la heuristica correspondiente
    def mirar_combinacion(self, columna, fila) -> int:
        
        heuristica_menor = min(self.mirar_combinacionColumnas(columna, fila), self.mirar_combinacionFilas(columna, fila),
                                self.mirar_combinacionDiagonalUp(columna, fila), self.mirar_combinacionDiagonalDown(columna, fila))
        return heuristica_menor
    
    def mirar_combinacionColumnas(self, columna: int, fila: int) -> int:
        heuristica = 4
      
        if columna + 3 < self.lenTablero:
            primera_ficha = 0

            for i in range(columna, columna + 4):

                if primera_ficha == 0 and self.tablero[i][fila] != 0:
                    primera_ficha = self.tablero[i][fila]
                    
                if primera_ficha != 0:
                    
                    if primera_ficha == self.tablero[i][fila]:
                        heuristica -= 1

                    elif primera_ficha != self.tablero[i][fila] and self.tablero[i][fila] != 0:
                        return 4
                
            # Si se trata de una ficha del jugador max, sumamos a la utilidad, si no, restamos
            if primera_ficha == 1:
                self.utilidad += (4 - heuristica)

            elif primera_ficha == 2:
                self.utilidad -= (4 - heuristica)

        return heuristica
    

                
    def mirar_combinacionFilas(self, columna: int, fila: int) -> int:
        heuristica = 4

        if fila + 3 < self.lenTablero:
            primera_ficha = 0

            for j in range(fila, fila + 4):

                if primera_ficha == 0 and self.tablero[columna][j] != 0:
                    primera_ficha = self.tablero[columna][j]

                if primera_ficha != 0:
                    
                    if primera_ficha == self.tablero[columna][j]:
                        heuristica -= 1

                    elif primera_ficha != self.tablero[columna][j] and self.tablero[columna][j] != 0:
                        # Devuelve 4 ya que no hay ninguna combinación posible
                        return 4

            # Si se trata de una ficha del jugador max, sumamos a la utilidad, si no, restamos
            if primera_ficha == 1:
                self.utilidad += (4 - heuristica)

            else:
                self.utilidad -= (4 - heuristica)

        return heuristica
                
    def mirar_combinacionDiagonalDown(self, columna: int, fila: int) -> int:
        heuristica = 4
        
        if fila + 3 < self.lenTablero:
            
            if columna + 3 < self.lenTablero:
                primera_ficha = 0
                
                for i in range(0, 4):

                    if primera_ficha == 0 and self.tablero[columna + i][fila + i] != 0:
                        primera_ficha = self.tablero[columna + i][fila + i]
                        
                    if primera_ficha != 0:

                        if primera_ficha == self.tablero[columna + i][fila + i]:
                            heuristica -= 1

                        elif primera_ficha != self.tablero[columna + i][fila + i] and self.tablero[columna + i][fila + i] != 0:
                            # Devuelve 4 ya que no hay ninguna combinación posible
                            return 4
                    
                # Si se trata de una ficha del jugador max, sumamos a la utilidad, si no, restamos
                if primera_ficha == 1:
                    self.utilidad += (4 - heuristica)
                else:
                    self.utilidad -= (4 - heuristica)

        return heuristica
    
    def mirar_combinacionDiagonalUp(self, columna: int, fila: int) -> int:
        heuristica = 4
        
        if fila - 3 >= 0:

            if columna + 3 < self.lenTablero:
                primera_ficha = 0

                for i in range(0, 4):

                    if primera_ficha == 0 and self.tablero[columna + i][fila - i] != 0:
                        primera_ficha = self.tablero[columna + i][fila - i]
                        
                    if primera_ficha != 0:   
                         
                        if primera_ficha == self.tablero[columna + i][fila - i]:
                            heuristica -= 1

                        elif primera_ficha != self.tablero[columna + i][fila - i] and self.tablero[columna + i][fila - i] != 0:
                            # Devuelve 4 ya que no hay ninguna combinación posible
                            return 4
                    
                # Si se trata de una ficha del jugador max, sumamos a la utilidad, si no, restamos
                if primera_ficha == 1:
                    self.utilidad += (4 - heuristica)

                else:
                    self.utilidad -= (4 - heuristica)

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

    # Creamos una variable de clase para que ambos agentes compartan las acciones
    accions = None

    def __init__(self, nom):
        super(AgentMinimax, self).__init__(nom)
        # Accions estará formado por una lista de acciones de manera cronológica estructurada de la siguiente forma:
        # [(columna, fila, fichaJugador), (columna, fila, fichaJugador), ...]
        self.__puntuacio = 0

    def minimax(self, estat: EstatMinimax, torn_de_max: bool, profunditat_actual: int) -> tuple[bool, EstatMinimax]:
        if profunditat_actual == PROFUNDIDAD_MAXIMA:
            # Calcula la utilidad del estado
            if not torn_de_max:
                estat.beta = estat.utilidad
            else:
                estat.alpha = estat.utilidad
            return (False, estat)
        
        elif estat.es_meta():
            # La utilidad de una terminal sera de 1000 o -1000
            if not torn_de_max:
                estat.beta = 1000
            else:
                estat.alpha = -1000
            return (True, estat)
        
        mejor_estado = None
        
        for estat_fill in estat.genera_fills(torn_de_max):
            is_finished, estat_minimax = self.minimax(estat_fill, not torn_de_max, profunditat_actual + 1)
            if torn_de_max:
                # El turno del hijo es min y el del padre es max
                if estat.alpha < estat_fill.beta and not estat_fill.beta == float('inf'):
                    estat.alpha = estat_fill.beta
                    mejor_estado = estat_fill
                if estat.alpha >= estat.beta:
                    # Poda ya que como el padre del padre es min, no va a elegir al padre
                    break
            else:
                # El turno del hijo es max y el del padre es min
                if estat.beta > estat_fill.alpha and not estat_fill.alpha == float('-inf'):
                    estat.beta = estat_fill.alpha
                    mejor_estado = estat_fill
                if estat.alpha >= estat.beta:
                    # Podamos ya que como el padre del padre es max, no va a elegir al padre
                    break
        if mejor_estado:
            estat.seguents_accions += mejor_estado.seguents_accions
            estat_minimax.seguents_accions = mejor_estado.seguents_accions + estat_minimax.seguents_accions
        return (is_finished, estat_minimax)
    
    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estat = EstatMinimax(percepcio[SENSOR.MIDA])
        
        if AgentMinimax.accions is None:
            finish, estat_minimax = self.minimax(estat, True, 0)
            while not finish:
                finish, estat_minimax = self.minimax(estat_minimax, True, 0)
            accions = list()
            iterador = estat_minimax
            while iterador.pare is not None:
                pare, accio = iterador.pare

                accions.append(accio)
                iterador = pare
            AgentMinimax.accions = accions

        if AgentMinimax.accions:
            accio = AgentMinimax.accions.pop()[:2]
            return Accio.POSAR, accio
        else:
            return Accio.ESPERAR
