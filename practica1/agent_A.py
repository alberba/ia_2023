import copy
from queue import PriorityQueue

from practica1.agent import Agent, Estat
from ia_2022 import entorn
from practica1.entorn import Accio, SENSOR

class AgentA(Agent):
    def __init__(self, nom):
        super(AgentA, self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def cerca_A(self, estat_inicial: Estat):
        self.__oberts = PriorityQueue()
        self.__tancats = set()
        estat_actual = None

        self.__oberts.put((estat_inicial.fn, estat_inicial))
        estat_actual = None

        while not self.__oberts.empty():
            _, estat_actual = self.__oberts.get()
            for estat_tancat in self.__tancats:
                if estat_actual == estat_tancat:
                    continue
            if estat_actual.es_meta():
                break

            estats_fills = estat_actual.genera_fills()
            for estat in estats_fills:
                if estat not in self.__tancats:
                    self.__oberts.put((estat.fn, estat))

            self.__tancats.add(estat_actual)
        if estat_actual.es_meta():
            estat_actual.calcular_heuristica_fn()
            accions = list()
            iterador = estat_actual
            while iterador.pare is not None:
                pare, accio = iterador.pare

                accions.append(accio)
                iterador = pare
            self.__accions = accions
    
    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estat = EstatA(percepcio[SENSOR.MIDA], 0)
        
        if self.__accions is None:
            self.cerca_A(estat)

        if self.__accions:
            accio = self.__accions.pop()
            return Accio.POSAR, accio
        else:
            return Accio.ESPERAR


class EstatA(Estat):
    def __init__(self, filas_columnas, pes: int, heuristica=4, pare=None):
        super().__init__(filas_columnas, pare)
        self.__heuristica = heuristica
        self.__pes = pes
        self.__fn = self.heuristica + self.__pes


    def es_meta(self):
        return self.heuristica == 0

    def calcular_heuristica_fn (self):
        for columna in range(self.lenTablero):
            for fila in range(self.lenTablero):
                if self.tablero[columna][fila] == 1:
                    h = self.mirar_combinacion(columna, fila)
                    if h < self.heuristica:
                        self.heuristica = h
        self.fn = self.heuristica + self.__pes

    def genera_fills(self) -> list:
        estats_generats = []

        for columna in range(self.lenTablero):
            for fila in range(self.lenTablero):
                if self.tablero[columna][fila] == 0:
                    nou_estat = copy.deepcopy(self)
                    nou_estat.pare = (self, (columna, fila))

                    nou_estat.tablero[columna][fila] = 1
                    nou_estat.pes += 1
                    nou_estat.calcular_heuristica_fn()
                    estats_generats.append(nou_estat)
        
        return estats_generats

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
        return heuristica
    
    @property
    def pes(self):
        return self.__pes
    
    @pes.setter
    def pes(self, pes):
        self.__pes = pes

    @property
    def fn(self):
        return self.__fn
    
    @fn.setter
    def fn(self, fn):
        self.__fn = fn
    
    def __lt__(self, other):
        return False
    
    @property
    def heuristica(self):
        return self.__heuristica
    
    @heuristica.setter
    def heuristica(self, heuristica):
        self.__heuristica = heuristica
