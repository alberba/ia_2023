""" Fitxer que conté l'agent barca en profunditat.

S'ha d'implementar el mètode:
    actua()
"""
from ia_2022 import entorn
from quiques.agent import Barca, Estat
from quiques.entorn import AccionsBarca, SENSOR


class BarcaProfunditat(Barca):
    def __init__(self):
        super(BarcaProfunditat, self).__init__()
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def cerca_profunditat(self, estat: Estat):
        self.__oberts = [estat]
        self.__tancats = []
        while self.__oberts != []:
            estat_actual = self.__oberts.pop(len(self.__oberts) - 1)
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
        
        estat = Estat(percepcio.__getitem__(SENSOR.LLOC), 3, 3)

        if self.__accions is None:
            self.cerca_profunditat(estat)
        if len(self.__accions) == 0:
            return AccionsBarca.ATURAR
        else:
            return AccionsBarca.MOURE, self.__accions.pop()
