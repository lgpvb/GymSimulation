import itertools
from functools import total_ordering
from typing import Self
from apparaat import Apparaat
from oefening import Oefening
from typing import Optional

@total_ordering
class Sporter:
    id_counter:int = itertools.count(1)  
    vergelijking: str = 'vertrektijd'

    def __init__(self, oefeningen: list[Oefening], vertrektijd: int):
        self.id = next(Sporter.id_counter)
        self.oefeningen = sorted(oefeningen, key=lambda x: x.prioriteit)
        self.vertrektijd: int = vertrektijd
        self.wachttijd: int = 0
        self.tijd_in_gym: int = 0
        self.bezig: bool = False

    def start_oefening(self, oefening: Oefening,  tijd: int, apparaten: Optional[list[Apparaat]] = None, ):
        self.bezig = True
        self.oefeningen.remove(oefening)
        if apparaten:
            for apparaat in apparaten:
                apparaat.gebruik_apparaat(tijd)

    def eindig_oefening(self, tijd: int, apparaten: Optional[list[Apparaat]] = None):
        self.bezig = False
        if apparaten:
            for apparaat in apparaten:
                apparaat.gebruik_apparaat(tijd)

    def __lt__(self, other: Self):
        return self.vertrektijd < other.vertrektijd
        """
        match self.vergelijking:
            case 'vertrektijd':
                return self.vertrektijd < other.vertrektijd
            case 'wachttijd':
                return self.wachttijd < other.wachttijd
        """
        
    def __repr__(self):
        return f"Sporter(id={self.id}, " \
                "vertrektijd={self.vertrektijd}, " \
                "wachttijd={self.wachttijd}, " \
                "tijd_in_gym={self.tijd_in_gym}, " \
                "bezig={self.bezig}, " \
                "oefeningen={self.oefeningen})" 
