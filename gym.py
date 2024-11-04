import random
import heapq 

from queue import PriorityQueue
from apparaat import Apparaat
from sporter import Sporter
from oefening import Oefening
from distributions import bereken_aantal_nieuwe_sporters, bereken_tijd_in_gym, bereken_tijd_oefening
from apparaat import Apparaat
from typing import Optional

from collections import deque

class Gym:
    def __init__(self, aantal_loopbanden: int, aantal_racks: int, aantal_banken: int, aantal_bb: int, aantal_db: int):
        self.sporters: list[Sporter] = []
        self.loopbanden = self.maak_apparaten("Loopband", aantal_loopbanden)
        self.racks = self.maak_apparaten("Rack", aantal_loopbanden)
        self.banken = self.maak_apparaten("Bank", aantal_banken)
        self.barbells = self.maak_apparaten("Barbell", aantal_bb)
        self.dumbbells = self.maak_apparaten("Dumbbell", aantal_db)
        self.bezoekers = 0

    def maak_apparaten(self, type_apparaat: str, aantal):
        apparaten = [Apparaat(type_apparaat+str(_) for _ in range(aantal))] 
        heapq.heapify(apparaten) 
        return apparaten

    @staticmethod
    def apparaat_beschikbaar(apparaten: list[Apparaat]):
        """
        Geeft aan of één type apparaat beschikbaar is
        """
        for apparaat in apparaten:
            if apparaat.bezet == False:
                return apparaat
        return None

    def apparaten_beschikbaar(self, benodigde_apparaten: list[str]):
        """
        Geeft aan of alle benodigde apparaten beschikbaar zijn
        """
        if not benodigde_apparaten:
            return None

        soort_apparaten = {}
        beschikbare_apparaten = []

        for benodigd in benodigde_apparaten: 
            soort_apparaten[benodigd] = getattr(self, benodigd)
        
        for benodigd, apparaten in soort_apparaten.items():
            beschikbaar_apparaat = self.apparaat_beschikbaar(apparaten)
            if beschikbaar_apparaat:
                beschikbare_apparaten.append(beschikbaar_apparaat)

        return beschikbare_apparaten
                
    def sporter_heap(self, sporter: Sporter, oefening: Oefening, eindtijd_oefening: int, beschikbare_apparaten: Optional[list[Apparaat]] = None):
        self.sporters.remove(sporter)
        sporter.start_oefening(oefening, eindtijd_oefening, beschikbare_apparaten)
        heapq.heappush(self.sporters, sporter)

    def sporter_in_wachtrij(self, resterende_apparaten: list[Apparaat]):
        """
        Zet sporter in wachtrij(en) voor apparaten
        """
        soort_apparaten = {}
        apparaten = {}
        for benodigd in resterende_apparaten: 
            apparaten[benodigd] = getattr(self, benodigd)
        
        for benodigd, apparaten in soort_apparaten.items():
            for apparaat in apparaten:
                if apparaat.wachtrij.qsize() <= 1:
                    vars(self)[benodigd].remove(apparaat)
                    apparaat.wachtrij = 1
                    heapq.heappush(vars(self)[benodigd], apparaat)
                    break

    def update_sporters(self, tijd: int):
        for sporter in self.sporters:
            if sporter.bezig == False:
                for oefening in sporter.oefeningen:
                    benodigde_apparaten = Oefening.benodigde_apparaten(oefening.naam)
                    eindtijd_oefening = tijd + oefening.duur
                    beschikbare_apparaten = self.apparaten_beschikbaar(benodigde_apparaten)
                    if beschikbare_apparaten == None:
                        self.sporter_heap(sporter, oefening, eindtijd_oefening)
                        break
                    elif len(beschikbare_apparaten) == len(benodigde_apparaten):
                        self.sporter_heap(sporter, oefening, eindtijd_oefening, beschikbare_apparaten)
                        break
                    else:
                        resterende_apparaten = list(set(benodigde_apparaten) - set(beschikbare_apparaten))
                        self.sporter_in_wachtrij(resterende_apparaten)

    def nieuwe_sporters(self, tijd: int, aantal_oefeningen: int):
        aantal_nieuwe_sporters = bereken_aantal_nieuwe_sporters(tijd)
        self.bezoekers += aantal_nieuwe_sporters
        Sporter.vergelijking = 'vertrektijd'
        for _ in range(aantal_nieuwe_sporters):
            oefeningen = self.genereer_oefeningen(aantal_oefeningen)
            vertrektijd = tijd + bereken_tijd_in_gym()
            nieuwe_sporter = Sporter(oefeningen, vertrektijd)
            heapq.heappush(self.sporters, nieuwe_sporter)

    def verwijder_sporters(self, tijd: int):
        """
        Verwijder sporters die alle oefeningen hebben voltooid, of ze zijn langer dan hun gewenste
        tijd in de gym en hebben minstens 90% van de oefeningen voltooid.
        """
        Sporter.vergelijking = 'vertrektijd'
        if len(self.sporters) > 0:
            while heapq.nsmallest(1, self.sporters)[0] == tijd:
                vertrekkende_sporter = heapq.heappop(self.sporters)
                if vertrekkende_sporter.bezig == True:
                    vertrekkende_sporter.eindig_oefening()
                self.bezoekers -= 1

    def update_apparaat_status(self, tijd: int):
        for apparaten_lijst in [self.loopbanden, self.racks, self.banken, self.barbells, self.dumbbells]:
            for apparaat in apparaten_lijst:
                if apparaat.tijdstip_onbezet == tijd:
                    apparaat.bezet = False
                elif apparaat.tijdstip_onbezet < tijd:
                    print("Apparaat zou onbezet moeten zijn...")
                
    
    def simuleer_tijdstap(self, tijd: int):
        self.nieuwe_sporters(tijd, aantal_oefeningen=6)
        self.update_sporters(tijd)
        self.verwijder_sporters(tijd)
        self.update_apparaat_status(tijd)
    
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
    
    def aantal_bezette_apparaten(self, apparaten: list[Apparaat]) -> int:
        aantal_apparaten = 0
        for apparaat in apparaten:
            if apparaat.bezet == True:
                aantal_apparaten += 1
        
        return aantal_apparaten
    
    def genereer_oefeningen(self, aantal_oefeningen: int):
        oefeningen = [
            Oefening("Squats", 0, bereken_tijd_oefening(15), ["Rack"]),
            Oefening("Push-ups", 0, bereken_tijd_oefening(10), []),
            Oefening("Deadlifts", 0, bereken_tijd_oefening(15), ["Barbell"]),
            Oefening("Bench press", 0, bereken_tijd_oefening(15), ["Bench", "Barbell"]),
            Oefening("Pull-ups", 0, bereken_tijd_oefening(10), ["Rack"]),
            Oefening("Lunges", 0, bereken_tijd_oefening(15), [], ['Dumbbells']),
            Oefening("Plank", 0, bereken_tijd_oefening(5), [])
        ]
        
        geselecteerde_oefeningen = random.sample(oefeningen, aantal_oefeningen)
        prioriteiten = random.sample(range(1, aantal_oefeningen + 1), aantal_oefeningen)
        
        for oefening, prioriteit in zip(geselecteerde_oefeningen, prioriteiten):
            oefening.prioriteit = prioriteit
            
        return geselecteerde_oefeningen
    
    def __repr__(self):
        loopbanden_bezet = self.aantal_bezette_apparaten(self.loopbanden)
        banken_bezet = self.aantal_bezette_apparaten(self.banken)
        racks_bezet = self.aantal_bezette_apparaten(self.racks)        

        return f"Aantal sporters: {self.bezoekers} \
                 Aantal bezette loopbanden: {loopbanden_bezet} \
                 Aantal bezette banken: {banken_bezet} \
                 Aantal bezette racks: {racks_bezet}"
    
    
