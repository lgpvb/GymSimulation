import itertools
from functools import total_ordering
from typing import Self
from apparaat import Apparaat


class Sporter:
    id_counter = itertools.count(1)  

    def __init__(self, oefeningen, verlatingstijd: int):
        self.id = next(Sporter.id_counter)
        self.oefeningen = sorted(oefeningen, key=lambda x: x.prioriteit)
        self.verlatingstijd: int = verlatingstijd
        self.wachttijd: int = 0
        self.tijd_in_gym: int = 0
        self.bezig: bool = False

    def start_oefening(self, apparaat: Apparaat):
        self.bezig = True
        huidige_oefening = self.oefeningen[0]
        if apparaat.naam in huidige_oefening.benodigdheden:
            self.oefeningen.pop(0)
        """
        for oefening in self.oefeningen:
            if gym.apparaat_beschikbaar(oefening):
                gym.koppel_apparaat(oefening, self)
            else:
                gym.voeg_aan_wachtrij_toe(oefening, self)
        """
    
    def eindig_oefening(self, apparaat: Apparaat):
        self.bezig = False

    
    @total_ordering
    def __lt__(self, other: Self):
        return self.wachttijd < other.wachttijd

    def __eq__(self, other: Self):
        return self.id == other.id
