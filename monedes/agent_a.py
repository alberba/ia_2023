from monedes.agent import AgentMoneda, Estat
from monedes.entorn import AccionsMoneda
from ia_2022 import agent, entorn

class MonedasA(AgentMoneda):
    def __init__(self):
        super(AgentMoneda, self).__init__()
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

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
                estats_fills = estat_actual.genera_fills()
                self.__oberts = self.__oberts + estats_fills
                self.__tancats.append(estat_actual)
        return False

    def actua(
        self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estat = Estat("CX CX")

        if self.__accions is None:
            self.cerca_A(estat)
        if len(self.__accions) == 0:
            return AccionsMoneda.RES
        else:
            if self.__accions.

def estat_menor_fn(estats: list[Estat]) -> Estat:
    estat_menor = estats[0]
    for estat in estats:
        if (estat.coste + estat.heuristica) < (estat_menor.coste + estat_menor.heuristica):
            estat_menor = estat
    return estat_menor