import random
from queue import PriorityQueue
from apparaat import Apparaat
from sporter import Sporter
from oefening import Oefening
from distributions import *

class Gym:
    def __init__(self, loopbanden, racks, banken):
        self.loopbanden = [Apparaat("Loopband") for _ in range(loopbanden)]
        self.racks = [Apparaat("Rack") for _ in range(racks)]
        self.banken = [Apparaat("Bank") for _ in range(banken)]
        self.sporters = []
        self.wachtrijen = {
            "Loopband": PriorityQueue(),
            "Rack": PriorityQueue(),
            "Bank": PriorityQueue(),
        }
        self.bezoekers = 0

    def nieuwe_sporter(self, oefeningen):
        sporter = Sporter(oefeningen)
        self.sporters.append(sporter)
        self.bezoekers += 1
        return sporter

    def update_apparaat_status(self):
        for apparaten_lijst in [self.loopbanden, self.racks, self.banken]:
            for apparaat in apparaten_lijst:
                if apparaat.resterende_tijd > 0:
                    apparaat.resterende_tijd -= 1
                elif apparaat.bezet and not self.wachtrijen[apparaat.naam].empty():
                    sporter = self.wachtrijen[apparaat.naam].get()
                    sporter.start_oefening(apparaat)

    def simuleer_tijdstap(self, tijd):
        # Nieuwe sporters komen op basis van een Poisson-verdeling binnen, piektijden van 8:00 tot 10:00 en van 18:30 tot 21:00
        nieuwe_sporters = bereken_aantal_nieuwe_sporters(tijd)
        for _ in range(nieuwe_sporters):
            oefeningen = self.genereer_oefeningen()
            verlatingstijd = tijd + bereken_tijd_in_gym()
            nieuwe_sporter = Sporter(oefeningen, verlatingstijd)
            self.sporters.append(nieuwe_sporter)
            #self.nieuwe_sporter(oefeningen, verlatingstijd)
            """
            sporter = self.nieuwe_sporter()
            sporter.start_training(self)
            """

        self.update_apparaat_status()

    def genereer_oefeningen(self):
        # Genereert willekeurige set oefeningen voor een sporter
        alle_oefeningen = [
            Oefening("Squats", 1, random.randint(10, 15), []),
            Oefening("Push-ups", 6, 10, []),
            Oefening("Deadlifts", 3, 15, ["Barbell"]),
            Oefening("Bench press", 2, 15, ["Bench", "Barbell"]),
            Oefening("Pull-ups", 4, 10, ["rack"]),
            Oefening("Lunges", 5, 15, [], ['Dumbbells']),
            Oefening("Plank", 7, 5, [])
        ]
        return random.sample(alle_oefeningen, 6)
    
    def gemiddelde_wachttijd(self):
        totale_wachttijd = 0
        for sporter in self.sporters:
            totale_wachttijd  += sporter.wachttijd

        gem_wachttijd   = totale_wachttijd / self.bezoekers if self.bezoekers > 0 else 0

        return gem_wachttijd

    def gemiddelde_tijd_in_gym(self):
        totale_tijd_in_gym = 0

        for sporter in self.sporters:
            totale_tijd_in_gym += sporter.tijd_in_gym
        
        gem_tijd_in_gym = totale_tijd_in_gym / self.bezoekers if self.bezoekers > 0 else 0
        
        return gem_tijd_in_gym
    
    def __repr__(self):
        return f"{self.gemiddelde_tijd_in_gym()}, {self.gemiddelde_wachttijd()}"