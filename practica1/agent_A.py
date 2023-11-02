# Autores: Sergi Oliver y Albert Salom

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
            estat_actual.calcular_heuristica()
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
    def __init__(self, filas_columnas, pes, heuristica=4, pare=None):
        super().__init__(filas_columnas, heuristica, pare)
        self.__pes = pes
        self.__fn = self.heuristica + pes

    
    def es_meta(self):
        """"Método para verificar si se ha alcanzado el estado objetivo"""
        return self.heuristica == 0

    def genera_fills(self) -> list:
        """"Método para generar nuevos estados"""
        estats_generats = []

        for columna in range(self.lenTablero):
            for fila in range(self.lenTablero):
                if self.tablero[columna][fila] == 0:
                    # Crea una copia del estado actual
                    nou_estat = copy.deepcopy(self)
                    nou_estat.pare = (self, (columna, fila))
                    # Crea una ficha
                    nou_estat.tablero[columna][fila] = 1
                    nou_estat.pes = self.pes + 1
                    # Calcula la heurística
                    nou_estat.calcular_heuristica()
                    estats_generats.append(nou_estat)
        
        return estats_generats
    
    def calcular_heuristica(self):
        for columna in range(self.lenTablero):
            for fila in range(self.lenTablero):
                if self.tablero[columna][fila] == 1:
                    self.mirar_combinacion(columna, fila)
    
        self.fn = self.heuristica + self.pes

    def mirar_combinacion(self, columna, fila) -> int:
        """ La función comprobará las combinaciones de 4 fichas a partir de la ficha colocada en la posición (columna, fila),
        definiendo asi la heuristica con la combinación mas cerca de la solución final\n

        SALIDA: La menor heuristica encontrada en todas las direcciones
        """
        delta = ((1, 0), (0, 1), (1, 1), (1, -1))

        for i in delta:

            heuristica = 3
            distinta_ficha = False
            over_limit = False
            diferencia_x = 0
            diferencia_y = 0

            for offset in range(1, 4):
                offset_x = offset * i[0]
                offset_y = offset * i[1]
                if columna + offset_x < self.lenTablero and fila + offset_y < self.lenTablero:

                    if self.tablero[columna][fila] == self.tablero[columna + offset_x][fila + offset_y]:
                        heuristica -= 1

                    elif self.tablero[columna][fila] == self.tablero[columna + offset_x][fila + offset_y] and self.tablero[columna + offset_x][fila + offset_y] != 0:
                        # Ha encontrado una ficha del jugador contrario
                        distinta_ficha = True
                        if i[0] > 0:
                            diferencia_x = 4 - offset_x
                        elif i[0] < 0:
                            diferencia_x = 4 + offset_x
                        if i[1] > 0:
                            diferencia_y = 4 - offset_y
                        elif i[1] < 0:
                            diferencia_y = 4 + offset_y
                        break
                else:
                    # Ha superado el límite del tablero
                    over_limit = True
                    if i[0] > 0:
                        diferencia_x = columna + 4 - self.lenTablero
                    elif i[0] < 0:
                        diferencia_x = 4 - columna - 1
                    if i[1] > 0:
                        diferencia_y = fila + 4 - self.lenTablero
                    elif i[1] < 0:
                        diferencia_y = 4 - fila - 1
                    break

            if distinta_ficha or over_limit:
                diferencia = max(abs(diferencia_x), abs(diferencia_y))
                if 0 <= columna - diferencia * i[0] < self.lenTablero and 0 <= fila - diferencia * i[1] < self.lenTablero:

                    for m in range (1, diferencia + 1):
                        offset_x = m * i[0]
                        offset_y = m * i[1]
                        if self.tablero[columna][fila] == self.tablero[columna - offset_x][fila - offset_y]:
                            heuristica -= 1
                        elif self.tablero[columna][fila] != self.tablero[columna - offset_x][fila - offset_y] and self.tablero[columna - offset_x][fila - offset_y] != 0:
                            # No caben 4 casillas del jugador en esta dirección, por tanto no hay ninguna combinación
                            return 4
                else:
                    return 4      

            if heuristica < self.heuristica:
                self.heuristica = heuristica
    
    def __lt__(self, other):
        return self.fn < other.fn if self.fn != other.fn else self.heuristica < other.heuristica
    
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
