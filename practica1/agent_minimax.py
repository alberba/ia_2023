# Autores: Sergi Oliver y Albert Salom

import copy
import time

from practica1.agent import Agent, Estat
from ia_2022 import entorn
from practica1.entorn import Accio, SENSOR

total_p_1 = 0
PROFUNDIDAD_MAXIMA = 3
class EstatMinimax(Estat):
    def __init__(self, filas_columnas, torn_de_max, tablero=None, pare=None):
        super().__init__(filas_columnas, 4, tablero, pare)
        self.__utilidad = 0
        self.__torn_de_max = torn_de_max

    
    def genera_fills(self) -> list['EstatMinimax']:
        """ Genera los posibles estados hijos del estado actual """

        estats_generats = []

        for columna in range(self.lenTablero):
            for fila in range(self.lenTablero):
                if self.tablero[columna][fila] == 0:
                    # Creamos un nuevo estado a partir del padre
                    nou_estat = EstatMinimax(
                        (self.lenTablero, self.lenTablero),
                        not self.torn_de_max,
                        [[cell for cell in row] for row in self.tablero],
                        pare=(self, (columna, fila))
                    )

                    nou_estat.tablero[columna][fila] = 1 if self.torn_de_max else 2

                    nou_estat.calcular_heuristica()
                    estats_generats.append(nou_estat)
        
        return estats_generats
    
    def calcular_heuristica(self):
        """ Calcula la heuristica y la utilidad de un estado """
        # Reseteamos la utilidad
        self.utilidad = 0
        self.heuristica = 4
        for columna in range(self.lenTablero):
            for fila in range(self.lenTablero):
                # Solo comprobaremos la heuristica a partir de las fichas colocadas
                if self.tablero[columna][fila] == 1 or self.tablero[columna][fila] == 2:
                    self.mirar_combinacion(columna, fila)

        return None


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
                
            self.add_utilidad(heuristica, columna, fila)
            
            if heuristica < self.heuristica:
                self.heuristica = heuristica

    def add_utilidad(self, heuristica, columna, fila):
        if heuristica < 3:
            if self.tablero[columna][fila] == 1:
                self.utilidad += 10 ** (3 - heuristica)

            else:
                self.utilidad -= 10 ** (3 - heuristica)

    
    @property
    def utilidad(self):
        return self.__utilidad
    
    @utilidad.setter
    def utilidad(self, utilidad):
        self.__utilidad = utilidad

    @property
    def torn_de_max(self):
        return self.__torn_de_max
    
    @torn_de_max.setter
    def torn_de_max(self, torn_de_max):
        self.__torn_de_max = torn_de_max

class AgentMinimax(Agent):

    # Creamos una variable de clase para que ambos agentes compartan las acciones
    accions = None

    def __init__(self, nom):
        super(AgentMinimax, self).__init__(nom)
        
        self.__tancats = set()

    def minimax(self, estat: EstatMinimax, alpha, beta, profunditat_actual: int) -> tuple[EstatMinimax, int]:
        global total_p_1
        
        if estat.es_meta():
            # La utilidad de una terminal sera de 1000 en caso de que max sea ganador o -1000 en caso de que min sea ganador
            if not estat.torn_de_max:
                return estat, 1000
            else:
                return estat, -1000                        
        
        elif profunditat_actual == PROFUNDIDAD_MAXIMA:
            # Calcula la utilidad del estado

            return estat, estat.utilidad
        
        fills_y_puntuacio = []

        for estat_fill in estat.genera_fills():
            if estat_fill in self.__tancats:
                continue

            self.__tancats.add(estat_fill)
            puntuacio_fill = self.minimax(estat_fill, alpha, beta, profunditat_actual + 1)

            fills_y_puntuacio.append(puntuacio_fill)
            if alpha >= beta:
                break
            if estat.torn_de_max:
                alpha = max(alpha, puntuacio_fill[1])
            else:
                beta = min(beta, puntuacio_fill[1])
        
        if estat.torn_de_max:
            return self.max(fills_y_puntuacio)
        else:
            return self.min(fills_y_puntuacio)



    
    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estat = EstatMinimax(percepcio[SENSOR.MIDA], True)
        
        if AgentMinimax.accions is None:

            ini = time.time()
            estat_minimax, _ = self.minimax(estat, float("-inf"), float("inf"), 0)
            while not estat_minimax.es_meta():

                estat = EstatMinimax(
                    percepcio[SENSOR.MIDA], 
                    estat_minimax.torn_de_max, 
                    [[cell for cell in row] for row in estat_minimax.tablero],
                    pare=estat_minimax.pare
                    )
                estat_minimax, _ = self.minimax(estat, float("-inf"), float("inf"), 0)
            
            self.meter_accions(estat_minimax)
            
            print("Tiempo:", time.time() - ini)
            print(AgentMinimax.accions)

        if AgentMinimax.accions:
            accio = AgentMinimax.accions.pop(0)[:2]
            return Accio.POSAR, accio
        else:
            return Accio.ESPERAR
        
    def meter_accions(self, estat_minimax: EstatMinimax):
        """ Mete las acciones del estado minimax en la variable de clase accions"""

        accions = list()
        iterador = estat_minimax

        while iterador.pare is not None:
            pare, accio = iterador.pare

            accions.insert(0, accio)
            iterador = pare
            AgentMinimax.accions = accions
    
    def max(self, puntuacio: list[tuple[EstatMinimax, int]]):
        """ Devuelve el estado minimax con la mayor puntuación """
        max = float("-inf")
        millor_estat = None

        for estat, score in puntuacio:
            if score > max:
                max = score
                millor_estat = estat
        return millor_estat, max
    
    def min(self, puntuacio: list[EstatMinimax, int]):
        """ Devuelve el estado minimax con la menor puntuación"""
        min = float("inf")
        millor_estat = None
        for estat, score in puntuacio:
            if score < min:
                min = score
                millor_estat = estat
        return millor_estat, min
