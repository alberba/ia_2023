""" Mòdul que conté l'agent per jugar al joc de les monedes.

Percepcions:
    ClauPercepcio.MONEDES
Solució:
    " XXXC"
"""

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
    def __init__(self, accions_previes = None) -> None:
        if accions_previes is None:
            accions_previes = []

        self.monedas = []
        self.accions_previes = accions_previes
    
    def genera_fills(self) -> list:
        posEspai = self.monedas.index(" ")
        self.genera_fills_botar(posEspai)

    def genera_fills_botar(self, posEspai) -> list:
        for i in range(2):
            accio = self.monedas
            if posEspai >= 2:
                accio[posEspai],  accio[posEspai - 2] =  accio[posEspai - 2], accio[posEspai]
                if accio[posEspai] == "X":
                    accio[posEspai] = "C"
                elif accio[posEspai] == "C":
                    accio[posEspai] = "X"
