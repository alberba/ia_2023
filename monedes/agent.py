""" Mòdul que conté l'agent per jugar al joc de les monedes.

Percepcions:
    ClauPercepcio.MONEDES
Solució:
    " XXXC"
"""
import copy
from queue import PriorityQueue

from ia_2022 import agent, entorn
from monedes.entorn import AccionsMoneda, SENSOR

SOLUCIO = " XXXC"

class Estat:
    def __init__(self, monedas: str, pes: int, pare = None, accions_previes = None):
        self.__monedas = list(monedas)
        self.__pare = pare
        self.__pes = pes

    def __hash__(self):
        return hash(tuple(self.__monedas))
    
    @property
    def info(self):
        return self.__monedas
    
    def __eq__(self, other) -> bool:
        return self.__monedas == other.__monedas

    def es_meta(self) -> bool:
        return self.__monedas == list(SOLUCIO)
    
    def genera_fills(self) -> list:
        fills = list()
        posEspai = self.__monedas.index(" ")

        fills += self.genera_fills_botar(posEspai)
        fills += self.genera_fills_desplaçar(posEspai)
        fills += self.generar_fills_girar()

        return fills
            
    def genera_fills_desplaçar(self, posEspai) -> list[str, int, int]:
        pos_accions = []
        for offset in [-1, 1]:
            if 0 <= posEspai + offset < len(self.__monedas):
                accio = self.__monedas.copy()
                accio[posEspai], accio[posEspai + offset] = accio[posEspai + offset], accio[posEspai]
                pos_accions.append(
                    Estat(
                        accio,
                        self.__pes + 1,
                        (self, (AccionsMoneda.DESPLACAR, posEspai + offset))
                    )
                )
        return pos_accions
    
    def generar_fills_girar(self) -> list[str, int, int]:
        pos_accions = []
        for i in range(len(self.__monedas)):
            accio = self.__monedas.copy()
            if not accio[i] == " ":
                accio[i] = self.girar_moneda(accio[i])
                pos_accions.append(
                    Estat(
                        accio,
                        self.__pes + 2,
                        (self, (AccionsMoneda.GIRAR, i))
                    )
                )
        return pos_accions
    
    def genera_fills_botar(self, posEspai) -> list[str, int, int]:
        poss_accions = list()
        for offset in [-2, 2]:
            if 0 <= posEspai + offset < len(self.__monedas):
                accio = self.__monedas.copy()
                accio[posEspai], accio[posEspai + offset] = accio[posEspai + offset], accio[posEspai]
                accio[posEspai] = self.girar_moneda(accio[posEspai])
                poss_accions.append(
                    Estat(
                        accio,
                        self.__pes + 3,
                        (self, (AccionsMoneda.BOTAR, posEspai + offset))
                    )
                )
        return poss_accions
    
    def calcular_heuristica(self) -> int:
        pos_espacio = self.__monedas.index(" ")
        vx = sum(1 for i in range(1, len(SOLUCIO)) if self.__monedas[i] != SOLUCIO[i])
        return vx + pos_espacio + self.__pes
    
    def girar_moneda(self, moneda):
        if moneda == "X":
            moneda = "C"
        elif moneda == "C":
            moneda = "X"
        return moneda
    
    @property
    def pare(self):
        return self.__pare
    
    @pare.setter
    def pare(self, pare):
        self.__pare = pare

    def __str__(self):
        return f"Monedes: {self.__monedas}, pes: {self.__pes}"
    
    def __lt__(self, other):
        return False

class AgentMoneda(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=0)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        print(self._posicio_pintar)

    def cerca_A(self, estat_inicial: Estat):
        self.__oberts = PriorityQueue()
        self.__tancats = set()

        self.__oberts.put((estat_inicial.calcular_heuristica(), estat_inicial))

        estat_actual = None

        while not self.__oberts.empty():
            _, estat_actual = self.__oberts.get()
            if estat_actual in self.__tancats:
                continue

            if estat_actual.es_meta():
                break

            estats_fills = estat_actual.genera_fills()
            for estat_f in estats_fills:
                self.__oberts.put((estat_f.calcular_heuristica(), estat_f))
            
            self.__tancats.add(estat_actual)
        
        if estat_actual.es_meta():
            accions = list()
            iterador = estat_actual
            while iterador.pare is not None:
                pare, accio = iterador.pare

                accions.append(accio)
                iterador = pare
            self.__accions = accions
        return False

    def actua(
        self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        # Tiene que devolver una acción y la posición en la que actua
        estat = Estat(percepcio[SENSOR.MONEDES], 0, pare=None)

        if self.__accions is None:
            self.cerca_A(estat)

        if self.__accions:
            accio = self.__accions.pop()
            return accio[0], accio[1]
        else:
            return AccionsMoneda.RES, None

