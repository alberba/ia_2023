import copy
import time

from practica1.agent import Agent, Estat
from ia_2022 import entorn
from practica1.entorn import Accio, SENSOR

total_p_1 = 0
PROFUNDIDAD_MAXIMA = 3
class EstatMinimax(Estat):
    def __init__(self, filas_columnas, torn_de_max, tablero=None, pare=None, alpha=float('-inf'), beta=float('inf'), seguents_accions=None):
        super().__init__(filas_columnas, tablero, pare)
        self.__utilidad = 0
        self.__heuristica = 4
        self.alpha = alpha
        self.beta = beta
        self.torn_de_max = torn_de_max
        if seguents_accions is None:
            seguents_accions = []
        self.seguents_accions = seguents_accions


    def es_meta(self):
        return self.heuristica == 0
    
    def genera_fills(self) -> list['EstatMinimax']:
        estats_generats = []

        for columna in range(self.lenTablero):
            for fila in range(self.lenTablero):
                if self.tablero[columna][fila] == 0:
                    nou_estat = EstatMinimax(
                        (self.lenTablero, self.lenTablero),
                        not self.torn_de_max,
                        [[cell for cell in row] for row in self.tablero],
                        pare=(self, (columna, fila)),
                        alpha=self.alpha,
                        beta=self.beta,
                        seguents_accions=self.seguents_accions + [(columna, fila, 1 if self.torn_de_max else 2)],


                    )

                    nou_estat.tablero[columna][fila] = 1 if self.torn_de_max else 2

                    nou_estat.calcular_heuristica()
                    estats_generats.append(nou_estat)
        
        return estats_generats
    
    def calcular_heuristica (self):
        # Reseteamos la utilidad
        self.utilidad = 0
        self.heuristica = 4
        for columna in range(self.lenTablero):
            for fila in range(self.lenTablero):
                if self.tablero[columna][fila] == 1 or self.tablero[columna][fila] == 2:
                    h = self.mirar_combinacion(columna, fila)
                    if h < self.heuristica:
                        self.heuristica = h
        return None

    # Cuando encuentra una pieza colocada, comprueba las siguientes 3 casillas horizontalmente, diagonalmente y verticalmente 
    # para calcular la heuristica correspondiente
    def mirar_combinacion(self, columna, fila) -> int:
        
        heuristica_menor = min(self.mirar_combinacionColumnas(columna, fila), self.mirar_combinacionFilas(columna, fila),
                                self.mirar_combinacionDiagonalUp(columna, fila), self.mirar_combinacionDiagonalDown(columna, fila))
        return heuristica_menor
    
    def mirar_combinacionColumnas(self, columna: int, fila: int) -> int:
        heuristica = 3
      
        if columna + 3 < self.lenTablero:
            
            for i in range(columna + 1, columna + 4):

                if self.tablero[columna][fila] == self.tablero[i][fila]:
                    heuristica -= 1

                elif self.tablero[columna][fila] != self.tablero[i][fila] and self.tablero[i][fila] != 0:

                    diferencia = columna + 4 - i

                    if columna - diferencia >= 0:

                        for m in range (columna - 1, columna - diferencia - 1, -1):

                            if self.tablero[columna][fila] == self.tablero[m][fila]:
                                heuristica -= 1
                            elif self.tablero[columna][fila] != self.tablero[i][fila] and self.tablero[i][fila] != 0:
                                return 4
                            
                    
                    else:
                        return 4
                

        else:

            diferencia = columna + 3 - self.lenTablero
            primer_indice = 0
            
            if columna - diferencia >= 0:

                for i in range(columna - 1, columna - diferencia + 1, -1):

                    if self.tablero[i][fila] == 1 or self.tablero[i][fila] == 2:
                        primer_indice = i + 1
                        break

                if primer_indice == 0:
                    primer_indice = columna - diferencia

                else:

                    if primer_indice + 3 > self.lenTablero:
                        return 4
                    
                    else:
                        
                        for i in range(columna + 1, primer_indice + 4):
                            
                            if self.tablero[columna][fila] == self.tablero[i][fila]:
                                heuristica -= 1
                                
                            elif self.tablero[columna][fila] != self.tablero[i][fila] and self.tablero[i][fila] != 0:
                                return 4   
                            
            else:
                return 4   
            
        # Si se trata de una ficha del jugador max, sumamos a la utilidad, si no, restamos
        if heuristica < 3:
            if self.tablero[columna][fila] == 1:
                self.utilidad += 10 ** (3 - heuristica)

            else:
                self.utilidad -= 10 ** (3 - heuristica)
        

        return heuristica
    

                
    def mirar_combinacionFilas(self, columna: int, fila: int) -> int:
        heuristica = 3
      
        if fila + 3 < self.lenTablero:

            for i in range(fila + 1, fila + 4):

                if self.tablero[columna][fila] == self.tablero[columna][i]:
                    heuristica -= 1

                elif self.tablero[columna][fila] != self.tablero[columna][i] and self.tablero[columna][i] != 0:

                    diferencia = fila + 4 - i

                    if fila - diferencia >= 0:

                        for m in range (fila - 1, fila - diferencia - 1, -1):

                            if self.tablero[columna][fila] == self.tablero[columna][m]:
                                heuristica -= 1

                            elif self.tablero[columna][fila] != self.tablero[columna][m] and self.tablero[columna][m] != 0:
                                return 4  
                    
                    else:
                        return 4
                

        else:

            diferencia = fila + 3 - self.lenTablero
            primer_indice = 0
            
            if fila - diferencia >= 0:

                for i in range(fila - 1, fila - diferencia + 1, -1):

                    if self.tablero[columna][i] == 1 or self.tablero[columna][i] == 2:
                        primer_indice = i + 1
                        break

                if primer_indice == 0:
                    primer_indice = fila - diferencia

                else:

                    if primer_indice + 3 > self.lenTablero:
                        return 4
                    
                    else:
                        
                        for i in range(fila + 1, primer_indice + 4):
                            
                            if self.tablero[columna][fila] == self.tablero[columna][i]:
                                heuristica -= 1
                                
                            elif self.tablero[columna][fila] != self.tablero[columna][i] and self.tablero[columna][i] != 0:
                                return 4   
                            
            else:
                return 4   
            
         # Si se trata de una ficha del jugador max, sumamos a la utilidad, si no, restamos
        if heuristica < 3:
            if self.tablero[columna][fila] == 1:
                self.utilidad += 10 ** (3 - heuristica)

            else:
                self.utilidad -= 10 ** (3 - heuristica)
            
        return heuristica
                
    def mirar_combinacionDiagonalDown(self, columna: int, fila: int) -> int:
        heuristica = 3
      
        if fila + 3 < self.lenTablero:

            if columna + 3 < self.lenTablero:

                for i in range(1, 4):

                    if self.tablero[columna][fila] == self.tablero[columna + i][fila + i]:
                        heuristica -= 1

                    elif self.tablero[columna][fila] != self.tablero[columna + i][fila + i] and self.tablero[columna + i][fila + i] != 0:

                        diferencia = fila + 4 - i

                        if fila - diferencia >= 0:

                            if columna - diferencia >= 0:

                                for m in range (-1, - diferencia - 1, -1):

                                    if self.tablero[columna][fila] == self.tablero[columna + m][fila + m]:
                                        heuristica -= 1

                                    elif self.tablero[columna][fila] != self.tablero[columna + m][fila + m] and self.tablero[columna + m][fila + m] != 0:
                                        return 4  
                        
                        else:
                            return 4
                

        else:

            diferencia = fila + 3 - self.lenTablero
            primer_indice = 0
            
            if fila - diferencia >= 0:

                if columna - diferencia >= 0:

                    for i in range(-1, -diferencia + 1, -1):

                        if self.tablero[columna + i][fila + i] == 1 or self.tablero[columna + i][fila + i] == 2:
                            primer_indice = i + 1
                            break

                    if primer_indice == 0:
                        primer_indice = fila - diferencia

                    else:

                        if primer_indice + 3 > self.lenTablero:
                            return 4
                        
                        else:
                            
                            for i in range(1, primer_indice + 4):
                                
                                if self.tablero[columna][fila] == self.tablero[columna + i][fila + i]:
                                    heuristica -= 1
                                    
                                elif self.tablero[columna][fila] != self.tablero[columna + i][fila + i] and self.tablero[columna + i][fila + i] != 0:
                                    return 4   
                            
            else:
                return 4   
            
        # Si se trata de una ficha del jugador max, sumamos a la utilidad, si no, restamos
        if heuristica < 3:
            if self.tablero[columna][fila] == 1:
                self.utilidad += 10 ** (3 - heuristica)

            else:
                self.utilidad -= 10 ** (3 - heuristica)
            
        return heuristica
    
    def mirar_combinacionDiagonalUp(self, columna: int, fila: int) -> int:
        heuristica = 3
      
        if fila - 3 < self.lenTablero:

            if columna + 3 < self.lenTablero:

                for i in range(1, 4):

                    if self.tablero[columna][fila] == self.tablero[columna + i][fila - i]:
                        heuristica -= 1

                    elif self.tablero[columna][fila] != self.tablero[columna + i][fila - i] and self.tablero[columna + i][fila - i] != 0:

                        diferencia = columna + 4 - i

                        if fila + diferencia >= 0:

                            if columna - diferencia >= 0:

                                for m in range (-1, - diferencia - 1, -1):

                                    if self.tablero[columna][fila] == self.tablero[columna + m][fila - m]:
                                        heuristica -= 1

                                    elif self.tablero[columna][fila] != self.tablero[columna + m][fila - m] and self.tablero[columna + m][fila - m] != 0:
                                        return 4  
                        
                        else:
                            return 4
                

        else:

            diferencia = columna + 3 - self.lenTablero
            primer_indice = 0
            
            if fila + diferencia >= 0:

                if columna - diferencia >= 0:

                    for i in range(-1, -diferencia + 1, -1):

                        if self.tablero[columna + i][fila - i] == 1 or self.tablero[columna + i][fila - i] == 2:
                            primer_indice = i + 1
                            break

                    if primer_indice == 0:
                        primer_indice = columna - diferencia

                    else:

                        if primer_indice + 3 > self.lenTablero or primer_indice - 3 <= 0:
                            return 4
                        
                        else:
                            
                            for i in range(1, primer_indice + 4):
                                
                                if self.tablero[columna][fila] == self.tablero[columna + i][fila - i]:
                                    heuristica -= 1
                                    
                                elif self.tablero[columna][fila] != self.tablero[columna + i][fila - i] and self.tablero[columna + i][fila - i] != 0:
                                    return 4   
                            
            else:
                return 4   
            
        # Si se trata de una ficha del jugador max, sumamos a la utilidad, si no, restamos
        if heuristica < 3:
            if self.tablero[columna][fila] == 1:
                self.utilidad += 10 ** (3 - heuristica)

            else:
                self.utilidad -= 10 ** (3 - heuristica)
            
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
        
        self.__tancats = set()

    def minimax(self, estat: EstatMinimax, profunditat_actual: int) -> EstatMinimax:
        global total_p_1
        
        if estat.es_meta():
            # La utilidad de una terminal sera de 1000 o -1000
            if not estat.torn_de_max:
                estat.beta = 1000
            else:
                estat.alpha = -1000
            return estat
        elif profunditat_actual == PROFUNDIDAD_MAXIMA:
            # Calcula la utilidad del estado
            if not estat.torn_de_max:
                estat.beta = estat.utilidad
            else:
                estat.alpha = estat.utilidad
            return estat
        
        hijos = estat.genera_fills()
        aux = False
        millor_estat = None
        tiempo = time.time()
        for estat_fill in hijos:
            if estat_fill in self.__tancats:
                continue

            # Heredamos alpha y beta
            estat_fill.alpha = estat.alpha
            estat_fill.beta = estat.beta

            estat_minimax = self.minimax(estat_fill, profunditat_actual + 1)
            if estat_minimax is None:
                continue
            aux = True
            if estat.torn_de_max:
                # El turno del hijo es min y el del padre es max
                if estat.alpha < estat_fill.beta and not estat_fill.beta == float('inf'):
                    estat.alpha = estat_fill.beta
                    millor_estat = estat_minimax
                if estat.alpha >= estat.beta:
                    # Poda ya que como el padre del padre es min, no va a elegir al padre
                    millor_estat = None
                    break
            else:
                # El turno del hijo es max y el del padre es min
                if estat.beta > estat_fill.alpha and not estat_fill.alpha == float('-inf'):
                    estat.beta = estat_fill.alpha
                    millor_estat = estat_minimax
                if estat.alpha >= estat.beta:
                    # Podamos ya que como el padre del padre es max, no va a elegir al padre
                    millor_estat = None
                    break
            self.__tancats.add(estat_fill)
        total_p_1 += 1 if profunditat_actual == 1 else 0
        #print(f"Profundidad actual: {profunditat_actual}. Tiempo: {time.time() - tiempo} Total juegos P1: {total_p_1}") if profunditat_actual <= 1 else None
            
        return millor_estat if aux else None

    
    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        ini = time.time()
        estat = EstatMinimax(percepcio[SENSOR.MIDA], True)
        
        if AgentMinimax.accions is None:
            estat_minimax = self.minimax(estat, 0)
            while not estat_minimax.es_meta():
                accions = list()
                iterador = estat_minimax
                while iterador.pare is not None:
                    pare, accio = iterador.pare

                    accions.append(accio)
                    iterador = pare
                if AgentMinimax.accions is None:
                    AgentMinimax.accions = accions
                else:
                    AgentMinimax.accions += accions
                estat = EstatMinimax(
                    percepcio[SENSOR.MIDA], 
                    estat_minimax.torn_de_max, 
                    [[cell for cell in row] for row in estat_minimax.tablero], 
                    alpha=float('-inf'), 
                    beta=float('inf'), 
                    )
                estat_minimax = self.minimax(estat, 0)
            
        #print("Tiempo:", time.time() - ini)

        if AgentMinimax.accions:
            accio = AgentMinimax.accions.pop()[:2]
            return Accio.POSAR, accio
        else:
            return Accio.ESPERAR
