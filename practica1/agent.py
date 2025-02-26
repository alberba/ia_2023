# Autores: Sergi Oliver y Albert Salom

"""
ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
import abc

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio


class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass

    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass

class Estat:
    def __init__(self, filas_columnas: tuple[int, int], heuristica=4, tablero = None, pare=None):
        
        self.__lenTablero = filas_columnas[0]
        if tablero is None:
            self.__tablero = [[0 for _ in range(filas_columnas[0])] for _ in range(filas_columnas[1])]
        else:
            self.__tablero = tablero
        self.__pare = pare
        self.__heuristica = heuristica

    def es_meta(self):
        """ Comprueba si el estado actual es un estado terminal """
        return self.heuristica == 0

    def es_ficha_contraria(self, offset_x, offset_y, columna, fila) -> bool:
        """ Comprueba si la ficha en la posición (columna + offset_x, fila + offset_y) es del jugador contrario """
        return self.tablero[columna][fila] == self.tablero[columna + offset_x][fila + offset_y] and self.tablero[columna + offset_x][fila + offset_y] != 0
    
    def es_ficha_igual(self, offset_x, offset_y, columna, fila) -> bool:
        """ Comprueba si la ficha en la posición (columna + offset_x, fila + offset_y) es del mismo jugador """
        return self.tablero[columna][fila] == self.tablero[columna + offset_x][fila + offset_y]

    def __hash__(self):
        return hash(str(self.__tablero))

    def __eq__(self, other):
        return self.__tablero == other.tablero

    def __lt__(self, other):
        return False

    @abc.abstractmethod
    def mirar_combinacion(self, columna, fila):
        pass
    
    @abc.abstractmethod
    def calcular_heuristica(self) -> int:
        pass

    @abc.abstractmethod
    def genera_fills(self) -> list:
        pass
    
    
    @property
    def pare(self):
        return self.__pare
    
    @pare.setter
    def pare(self, pare):
        self.__pare = pare

    @property
    def lenTablero(self):
        return self.__lenTablero
    
    @lenTablero.setter
    def lenTablero(self, lenTablero):
        self.__lenTablero = lenTablero

    @property
    def tablero(self):
        return self.__tablero
    
    @tablero.setter
    def tablero(self, tablero):
        self.__tablero = tablero
    
    @property
    def heuristica(self):
        return self.__heuristica
    
    @heuristica.setter
    def heuristica(self, heuristica):
        self.__heuristica = heuristica