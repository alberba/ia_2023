""" Mòdul que conté l'agent per jugar al joc de les monedes.

Percepcions:
    ClauPercepcio.MONEDES
Solució:
    " XXXC"
"""
import copy

from ia_2022 import agent, entorn

SOLUCIO = " XXXC"


class AgentMoneda(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=0)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        print(self._posicio_pintar)

    def actua(
        self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass

class Estat:
    def __init__(self, monedas: str, pare = None, accions_previes = None) -> None:
        if accions_previes is None:
            accions_previes = []

        self.monedas = monedas
        self.pare = pare
        self.accions_previes = accions_previes
        self.accions_pos = []
        self.coste = 0
        self.heuristica = None

    def es_meta(self) -> bool:
        return self.monedas == list(SOLUCIO)
    
    def genera_fills(self) -> list:
        posEspai = self.monedas.index(" ")
        self.accions_pos += self.genera_fills_botar(posEspai)
        self.accions_pos += self.genera_fills_desplaçar(posEspai)
        self.accions_pos += self.generar_fills_girar()

        estats_generats = []

        for accio, coste in self.accions_pos:
            nou_estat = copy.deepcopy(self)
            nou_estat.pare = (self)
            nou_estat.accions_previes.append(accio)

            self.monedas = accio
            self.coste += coste
            self.heuristica = self.calcular_heuristica(accio.index(" "))
            
            estats_generats.append(nou_estat)

        return estats_generats

    def genera_fills_botar(self, posEspai) -> list[str, int]:
        poss_accions = []
        for offset in [-2, 2]:
            if 0 <= posEspai + offset < len(self.monedas):
                accio = self.monedas.copy()
                accio[posEspai], accio[posEspai + offset] = accio[posEspai + offset], accio[posEspai]
                accio[posEspai] = girar_moneda(accio[posEspai])
                poss_accions.append([accio, 3])
        return poss_accions
            
    def genera_fills_desplaçar(self, posEspai) -> list[str, int]:
        pos_accions = []
        for offset in [-1, 1]:
            if 0 <= posEspai + offset < len(self.monedas):
                accio = self.monedas.copy()
                accio[posEspai], accio[posEspai + offset] = accio[posEspai + offset], accio[posEspai]
                pos_accions.append([accio, 1])
        return pos_accions
    
    def generar_fills_girar(self) -> list[str, int]:
        pos_accions = []
        for i in range(len(self.monedas)):
            accio = self.monedas.copy()
            if not accio[i] == " ":
                accio[i] = girar_moneda(accio[i])
                pos_accions.append([accio, 2])
        return pos_accions
    
    def calcular_heuristica(self, pos_espacio) -> int:
        vx = sum(1 for i in range(1, len(SOLUCIO)) if self.monedas[i] == SOLUCIO[i])
        return vx + pos_espacio

def girar_moneda(moneda):
    if moneda == "X":
        moneda = "C"
    elif moneda == "C":
        moneda = "X"
    return moneda

