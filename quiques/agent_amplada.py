from ia_2022 import entorn
from quiques.agent import Barca, Estat
from quiques.entorn import AccionsBarca, SENSOR


class BarcaAmplada(Barca):
    def __init__(self):
        super(BarcaAmplada, self).__init__()
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def actua(
            self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        
        self.__oberts = [Estat(percepcio[SENSOR.LLOC], percepcio[SENSOR.LLOPS_ESQ], percepcio[SENSOR.POLLS_ESQ])]
        self.__tancats = []
        while self.__oberts != []:
            self.__oberts.pop()
            if 
        
