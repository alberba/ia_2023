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
    def __init__(self, filas_columnas: tuple[int, int], heuristica=4, pare=None):
        
        self.__lenTablero = filas_columnas[0]
        self.__tablero = [[0 for _ in range(filas_columnas[0])] for _ in range(filas_columnas[1])]
        self.__heuristica = heuristica
        self.__pare = pare

    def __hash__(self):
        return hash((self.__lenTablero, str(self.__tablero)))

    def __eq__(self, other):
        return self.__tablero == other.tablero

    def __lt__(self, other):
        return False

    def es_meta(self):
        return self.__heuristica == 0

    @abc.abstractmethod
    def calcular_heuristica_fn(self) -> int:
        pass

    @abc.abstractmethod
    def genera_fills(self) -> list:
        pass
    
    @property
    def tablero(self):
        return self.__tablero
    
    @property
    def pare(self):
        return self.__pare
    
    @pare.setter
    def pare(self, pare):
        self.__pare = pare

    @property
    def heuristica(self):
        return self.__heuristica
    
    @heuristica.setter
    def heuristica(self, heuristica):
        self.__heuristica = heuristica

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
