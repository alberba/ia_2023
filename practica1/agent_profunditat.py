# Autores: Sergi Oliver y Albert Salom

import copy

from practica1.agent import Agent, Estat
from ia_2022 import entorn
from practica1.entorn import Accio, SENSOR

class AgentProfunditat(Agent):
    def __init__(self, nom):
        super(AgentProfunditat, self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def cerca_profunditat(self, estat: Estat):
        self.__oberts = [estat]
        self.__tancats = set()
        estat_actual = None
        # Mientras haya estados en la lista de estados abiertos
        while self.__oberts != []:
            # Mira el último estado de la lista
            estat_actual = self.__oberts.pop(len(self.__oberts) - 1)
            # Si el estado ya ha sido visitado, continúa con el siguiente
            if estat_actual in self.__tancats:
                continue
            # Si el estado actual es el estado objetivo, detiene la búsqueda
            if estat_actual.es_meta():
                break
            else:
                # Genera los nuevos estados
                estats_fills = estat_actual.genera_fills()
                estats_fills.reverse()
                 # Agrega los hijos a la lista de estados abiertos
                self.__oberts = self.__oberts + estats_fills
                # Agrega el estado actual al conjunto de estados cerrados
                self.__tancats.add(estat_actual)
        if estat_actual.es_meta():
            accions = list()
            iterador = estat_actual
            # Reconstruye la secuencia de acciones desde el estado objetivo hasta el inicial
            while iterador.pare is not None:
                pare, accio = iterador.pare

                accions.append(accio)
                iterador = pare
            self.__accions = accions
    
    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estat = EstatProfunditat(percepcio[SENSOR.MIDA])
        
        if self.__accions is None:
            self.cerca_profunditat(estat)

        if self.__accions:
            accio = self.__accions.pop()
            return Accio.POSAR, accio
        else:
            return Accio.ESPERAR


class EstatProfunditat(Estat):
    def __init__(self, filas_columnas, heuristica=4, pare=None):
        super().__init__(filas_columnas, heuristica, pare)


    def genera_fills(self) -> list:
        """ Genera los posibles estados hijos del estado actual """
        estats_generats = []

        for columna in range(self.lenTablero):
            for fila in range(self.lenTablero):
                if self.tablero[columna][fila] == 0:
                    nou_estat = copy.deepcopy(self)
                    nou_estat.pare = (self, (columna, fila))

                    nou_estat.tablero[columna][fila] = 1
                    nou_estat.calcular_heuristica()
                    estats_generats.append(nou_estat)
        
        return estats_generats
    
    def calcular_heuristica(self):
        """ Calcula la heuristica del estado actual """
        for columna in range(self.lenTablero):
            for fila in range(self.lenTablero):
                if self.tablero[columna][fila] == 1:
                    self.mirar_combinacion(columna, fila)

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