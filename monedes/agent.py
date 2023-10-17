""" Mòdul que conté l'agent per jugar al joc de les monedes.

Percepcions:
    ClauPercepcio.MONEDES
Solució:
    " XXXC"
"""
import copy

from ia_2022 import agent, entorn
from monedes.entorn import AccionsMoneda, SENSOR

SOLUCIO = " XXXC"

class Estat:
    def __init__(self, monedas: str, pare = None, accions_previes = None) -> None:
        if accions_previes is None:
            accions_previes = []

        self.monedas = list(monedas)
        self.pare = pare
        self.accions_previes = accions_previes
        self.accions_pos = []
        self.coste = 0
        self.heuristica = 0

    def es_meta(self) -> bool:
        return self.monedas == list(SOLUCIO)
    
    def genera_fills(self, tancats: list) -> list:
        posEspai = self.monedas.index(" ")
        self.accions_pos += self.genera_fills_botar(posEspai)
        self.accions_pos += self.genera_fills_desplaçar(posEspai)
        self.accions_pos += self.generar_fills_girar()

        estats_generats = []

        for accio, posMonedaAccion, coste in self.accions_pos:
            if accio in tancats:
                continue
            nou_estat = copy.deepcopy(self)
            nou_estat.pare = (self)
            # La estructura de accions_previes sera una lista de listas, donde
            # cada lista tendra la posicion de la moneda que va a actuar y el coste
            # Si coste es 1, significa que se desplaza, 2 si gira y 3 si salta
            nou_estat.accions_previes.append([posMonedaAccion, coste])

            nou_estat.monedas = accio
            nou_estat.coste += coste
            nou_estat.heuristica = nou_estat.calcular_heuristica(accio.index(" "))
            
            estats_generats.append(nou_estat)

        return estats_generats

    def genera_fills_botar(self, posEspai) -> list[str, int, int]:
        poss_accions = []
        for offset in [-2, 2]:
            if 0 <= posEspai + offset < len(self.monedas):
                accio = self.monedas.copy()
                accio[posEspai], accio[posEspai + offset] = accio[posEspai + offset], accio[posEspai]
                accio[posEspai] = girar_moneda(accio[posEspai])
                poss_accions.append([accio, posEspai + offset, 3])
        return poss_accions
            
    def genera_fills_desplaçar(self, posEspai) -> list[str, int, int]:
        pos_accions = []
        for offset in [-1, 1]:
            if 0 <= posEspai + offset < len(self.monedas):
                accio = self.monedas.copy()
                accio[posEspai], accio[posEspai + offset] = accio[posEspai + offset], accio[posEspai]
                pos_accions.append([accio, posEspai + offset, 1])
        return pos_accions
    
    def generar_fills_girar(self) -> list[str, int, int]:
        pos_accions = []
        for i in range(len(self.monedas)):
            accio = self.monedas.copy()
            if not accio[i] == " ":
                accio[i] = girar_moneda(accio[i])
                pos_accions.append([accio, i, 2])
        return pos_accions
    
    def calcular_heuristica(self, pos_espacio) -> int:
        vx = sum(1 for i in range(1, len(SOLUCIO)) if self.monedas[i] != SOLUCIO[i])
        return vx + pos_espacio

class AgentMoneda(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=0)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        print(self._posicio_pintar)

    def cerca_A(self, estat: Estat):
        self.__oberts = [estat]
        self.__tancats = []
        while self.__oberts != []:
            # Buscar Estado menor coste
            estat_actual = estat_menor_fn(self.__oberts)
            self.__oberts.remove(estat_actual)
            if estat_actual in self.__tancats:
                continue
            if estat_actual.es_meta():
                self.__accions = estat_actual.accions_previes
                return True
            else:
                estats_fills = estat_actual.genera_fills(self.__tancats)
                self.__oberts = self.__oberts + estats_fills
                self.__tancats.append(estat_actual)
        return False

    def actua(
        self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        # Tiene que devolver una acción y la posición en la que actua
        estat = Estat(percepcio[SENSOR.MONEDES])

        if self.__accions is None:
            self.cerca_A(estat)
        if len(self.__accions) == 0:
            return AccionsMoneda.RES
        else:
            accio = self.__accions.pop(0)
            posMonedaAccion, coste = accio
            if coste == 1:
                return AccionsMoneda.DESPLACAR, posMonedaAccion
            elif coste == 2:
                return AccionsMoneda.GIRAR, posMonedaAccion
            else:
                return AccionsMoneda.BOTAR, posMonedaAccion

def girar_moneda(moneda):
    if moneda == "X":
        moneda = "C"
    elif moneda == "C":
        moneda = "X"
    return moneda

def estat_menor_fn(estats: list[Estat]) -> Estat:
    estat_menor = estats[0]
    for estat in estats:
        if (estat.coste + estat.heuristica) < (estat_menor.coste + estat_menor.heuristica):
            estat_menor = estat
    return estat_menor
