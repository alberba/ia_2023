""" Fitxer que conté l'agent Barca.

Percepcions:
    ClauPercepcio.LLOC
    ClauPercepcio.QUICA_ESQ
    ClauPercepcio.LLOP_ESQ
    ClauPercepcio.QUICA_DRETA
    ClauPercepcio.LLOP_DRETA

Accions:
    AccionsBarca.MOURE, (nombre_de_quiques, nombres_de_llop)
    AccionsBarca.ATURA
"""
import abc
import copy
import itertools

from ia_2022 import agent, entorn
from quiques.entorn import SENSOR, Lloc

MAX_ANIMALS = 3


class Barca(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=1)

    def pinta(self, display):
        print(self._posicio_pintar)

    @abc.abstractmethod
    def actua(self, percep: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass


class Estat:
    # QUIQUES, LLOPS
    # Només funciona en aquest problema
    acc_poss = [
        acc
        for acc in itertools.product([0, 1, 2], [0, 1, 2])
        if (acc[-1] + acc[-2]) < 3 and not (acc[-1] == 0 and acc[-2] == 0)
    ]

    def __init__(self, local_barca: Lloc, llops_esq: int, polls_esq: int, pare=None,
                 accions_previes=None):
        if accions_previes is None:
            accions_previes = []

        self.pare = pare
        self.llops_esq = llops_esq
        self.quica_esq = polls_esq
        self.local_barca = local_barca

        self.accions_previes = accions_previes

    def __hash__(self):
        return hash((self.llops_esq, self.quica_esq))

    @property
    def llops_dreta(self):
        return MAX_ANIMALS - self.llops_esq

    @property
    def quica_dreta(self):
        return MAX_ANIMALS - self.quica_esq

    def __eq__(self, other):
        """Overrides the default implementation"""
        return (
                self.llops_esq == other.llops_esq
                and self.quica_esq == other.quica_esq
                and self.local_barca == other.local_barca
        )

    def legal(self) -> bool:
        """ Mètode per detectar si un estat és legal.

        Un estat és legal si no hi ha cap valor negatiu ni major que el màxim

        Returns:
            Booleà indicant si és legal o no.
        """
        return (0 <= self.llops_esq <= MAX_ANIMALS) and (0 <= self.quica_esq <= MAX_ANIMALS)

    def es_meta(self) -> bool:
        return self.quica_esq == 0 and self.llops_esq == 0

    def es_segur(self) -> bool:
        """ Únicament és segur si hi ha manco llops que gallines, o bé no hi ha gallines.

        Returns:
            Booleà indicant si és segur o no.
        """
        return (
                self.quica_esq >= self.llops_esq or self.quica_esq == 0
        ) and (
                self.quica_dreta >= self.llops_dreta or self.quica_dreta == 0
        )

    def genera_fill(self) -> list:
        """ Mètode per generar els estats fills.

        Genera tots els estats fill a partir de l'estat actual.

        Returns:
            Llista d'estats fills generats.
        """
        estats_generats = []

        for accio in self.acc_poss:
            nou_estat = copy.deepcopy(self)
            nou_estat.pare = (self)
            nou_estat.accions_previes.append(accio)

            quiques, llops = accio

            if self.local_barca is Lloc.ESQ:
                quiques = -quiques
                llops = -llops

            nou_estat.local_barca = -self.local_barca
            nou_estat.quica_esq += quiques
            nou_estat.llops_esq += llops

            if nou_estat.legal():
                estats_generats.append(nou_estat)

        return estats_generats

    def __str__(self):
        return (f"Llops esq: {self.llops_esq}, Quiques esq: {self.quica_esq} | "
                f"Llops dreta: {self.llops_dreta}, Quiques dreta: {self.quica_dreta} | Accio {self.accions_previes}")
