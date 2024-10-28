import itertools
from functools import total_ordering
from typing import Self
from apparaat import Apparaat

class Sporter:
    id_counter = itertools.count(1)  

    def __init__(self, oefeningen):
        self.id = next(Sporter.id_counter)
        self.oefeningen = sorted(oefeningen, key=lambda x: x.prioriteit)
        self.wachttijd: int = 0
        self.tijd_in_gym: int = 0

    def start_oefening(self, apparaat: Apparaat):
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
    
    @total_ordering
    def __lt__(self, other: Self):
        return self.wachttijd < other.wachttijd

    def __eq__(self, other: Self):
        return self.id == other.id
