from ia_2022 import entorn
from quiques.agent import Barca, Estat
from quiques.entorn import AccionsBarca, SENSOR


class BarcaAmplada(Barca):
    def __init__(self):
        super(BarcaAmplada, self).__init__()
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def cerca_amplada(self, estat: Estat):
        self.__oberts = [estat]
        self.__tancats = []
        while self.__oberts != []:
            estat_actual = self.__oberts.pop()
            if estat_actual in self.__tancats:
                continue
            if estat_actual.es_segur():
                if estat_actual.es_meta():
                    self.__accions = estat_actual.accions_previes
                    return True
                else:
                    estats_fills = estat_actual.genera_fill()
                    self.__oberts = self.__oberts + estats_fills
                    self.__tancats.append(estat_actual)
            else:
                self.__tancats.append(estat_actual)
                continue

    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estat = Estat(percepcio[SENSOR.LLOC], 3, 3)

        if self.__accions is None:
            self.cerca_amplada(estat)
        if len(self.__accions) == 0:
            return AccionsBarca.ATURAR
        else:
            return AccionsBarca.MOURE, self.__accions.pop()