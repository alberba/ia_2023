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
        super().__init__(filas_columnas, heuristica, pare)
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
        heuristica_menor = 3
        heuristica_menor = min(heuristica_menor, self.mirar_combinacionColumnas(columna, fila), self.mirar_combinacionFilas(columna, fila),
                                self.mirar_combinacionDiagonalUp(columna, fila), self.mirar_combinacionDiagonalDown(columna, fila))
        return heuristica_menor
    
    def mirar_combinacionColumnas(self, columna: int, fila: int) -> int:
        heuristica = 3
        if columna + 3 < self.lenTablero:
            for i in range(columna + 1, columna + 4):
                if self.tablero[i][fila] == 1:
                    heuristica -= 1
        return heuristica
                
    def mirar_combinacionFilas(self, columna: int, fila: int) -> int:
        heuristica = 3
        if fila + 3 < self.lenTablero:
            for j in range(fila + 1, fila + 4):
                if self.tablero[columna][j] == 1:
                    heuristica -= 1
        return heuristica
                
    def mirar_combinacionDiagonalDown(self, columna: int, fila: int) -> int:
        heuristica = 3
        if fila + 3 < self.lenTablero:
            if columna + 3 < self.lenTablero:
                for i in range(1, 4):
                    if self.tablero[i + columna][i + fila] == 1:
                        heuristica -= 1
        return heuristica
    
    def mirar_combinacionDiagonalUp(self, columna: int, fila: int) -> int:
        heuristica = 3
        if fila - 3 >= 0:
            if columna +3 < self.lenTablero:
                for i in range(1, 4):
                    if self.tablero[columna + i][fila - i] == 1:
                        heuristica -= 1
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
