from typing import Optional

class Oefening:
    def __init__(self, naam: str, prioriteit:int, duur:float, benodigdheden: Optional[list[str]]=None, optioneel_benodigdheden: Optional[list[str]]=None):
        self.naam = naam
        self.duur = duur
        self.benodigdheden = benodigdheden or []
        self.optioneel_benodigdheden = optioneel_benodigdheden or []
        self.prioriteit = prioriteit  

    def __repr__(self):
        return f"Oefening({self.naam}, {self.duur} min, {self.benodigdheden})"
