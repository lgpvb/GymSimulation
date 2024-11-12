from typing import Optional
from kansverdelingen import bereken_tijd_oefening

class Oefening:
    def __init__(self, naam: str, prioriteit:int, duur:int, benodigdheden: Optional[list[str]]=None, optionele_benodigdheden: Optional[list[str]]=None):
        self.naam = naam
        self.duur = bereken_tijd_oefening(duur)
        self.prioriteit = prioriteit  
        self.benodigdheden = benodigdheden or []
        self.optionele_benodigdheden = optionele_benodigdheden or []

    def __repr__(self):
        return f"Oefening({self.naam}, duurt {self.duur} min, waarvoor {self.benodigdheden} nodig zijn."

    @staticmethod
    def benodigde_apparaten(naam_oefening: str):
        oefening_apparaten_mapping = {
            'squats': ['racks'],  
            'push-ups': [],
            'deadlifts': ['barbells'],
            'bench press': ['banken', 'barbells'], 
            'pull-ups': ['racks'],
            'lunges': ['dumbbells'],  
            'plank': [],
            'hardlopen': ['loopbanden'],
            'bicep curls': ['dumbbells'],  
            'tricep dips': ['dipbars', 'banken'],  
            'leg press': ['leg press machine']
        }
        
        result = oefening_apparaten_mapping.get(naam_oefening.lower(), [])

        if result == []:
            return None
        else:
            return result
        