import random
import heapq 

from apparaat import Apparaat
from sporter import Sporter
from oefening import Oefening
from kansverdelingen import bereken_aantal_nieuwe_sporters, bereken_tijd_in_gym, bereken_tijd_oefening
from apparaat import Apparaat
from typing import Optional

from queue import PriorityQueue
from collections import deque

class Gym:
    def __init__(self, aantal_loopbanden: int, aantal_racks: int, aantal_banken: int, aantal_bb: int, aantal_db: int):
        self.sporters: list[Sporter] = []
        self.loopbanden = self.maak_apparaten("loopband", aantal_loopbanden)
        self.racks = self.maak_apparaten("Rack", aantal_racks)
        self.banken = self.maak_apparaten("Bank", aantal_banken)
        self.barbells = self.maak_apparaten("Barbell", aantal_bb)
        self.dumbbells = self.maak_apparaten("Dumbbell", aantal_db)
        self.bezoekers = 0

    def simuleer_tijdstap(self, tijd: int):
        self.nieuwe_sporters(tijd, aantal_oefeningen=6)
        self.update_sporters(tijd)
        self.verwijder_sporters(tijd)
        self.update_apparaat_status(tijd)

    def maak_apparaten(self, type_apparaat: str, aantal):
        apparaten = [Apparaat(type_apparaat+str(_)) for _ in range(aantal)] 
        heapq.heapify(apparaten) 
        return apparaten

    def apparaat_beschikbaar(self, apparaten: list[Apparaat]):
        """
        Geeft aan of een apparaat beschikbaar is
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

    def reheap_sporter(self, sporter: Sporter, oefening: Oefening, eindtijd_oefening: int, beschikbare_apparaten: Optional[list[Apparaat]] = None):
        self.sporters.remove(sporter)
        sporter.start_oefening(oefening, eindtijd_oefening, beschikbare_apparaten)
        heapq.heappush(self.sporters, sporter)

    def sporter_in_wachtrij(self, sporter: Sporter, resterende_apparaten: list[Apparaat]):
        """
        Zet sporter in wachtrij(en) voor apparaten
        """
        soort_apparaten = {}

        for benodigd in resterende_apparaten: 
            soort_apparaten[benodigd] = getattr(self, benodigd)
        
        for benodigd, apparaten in soort_apparaten.items():
            for apparaat in apparaten:
                if apparaat.wachtrij.qsize() == 0:
                    vars(self)[benodigd].remove(apparaat)
                    apparaat.wachtrij.put(sporter)
                    heapq.heappush(vars(self)[benodigd], apparaat)
                    break
                else:
                    pass    
       
    def update_sporters(self, tijd: int):
        for sporter in self.sporters:
            if sporter.bezig == False:
                for oefening in sporter.oefeningen:
                    benodigde_apparaten = Oefening.benodigde_apparaten(oefening.naam)
                    eindtijd_oefening = tijd + oefening.duur
                    beschikbare_apparaten = self.apparaten_beschikbaar(benodigde_apparaten)
                    if benodigde_apparaten == None:
                        self.reheap_sporter(sporter, oefening, eindtijd_oefening)
                        break
                    elif len(beschikbare_apparaten) == len(benodigde_apparaten):
                        self.reheap_sporter(sporter, oefening, eindtijd_oefening, beschikbare_apparaten)
                        break
                    else:
                        resterende_apparaten = list(set(benodigde_apparaten) - set(beschikbare_apparaten))
                        self.sporter_in_wachtrij(sporter, resterende_apparaten)
                        print("WAGGARIJ")
                        break

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
        tijd in de gym.
        """
        Sporter.vergelijking = 'vertrektijd'
        if len(self.sporters) > 0:
            while self.sporters and (heapq.nsmallest(1, self.sporters)[0].vertrektijd <= tijd or (not heapq.nsmallest(1, self.sporters)[0].oefeningen)):
                vertrekkende_sporter = heapq.heappop(self.sporters)
                if vertrekkende_sporter.bezig == True:
                    vertrekkende_sporter.eindig_oefening(tijd)
                self.bezoekers -= 1

    def update_apparaat_status(self, tijd: int):
        for apparaten_lijst in [self.loopbanden, self.racks, self.banken, self.barbells, self.dumbbells]:
            for apparaat in apparaten_lijst:
                if apparaat.tijdstip_waarop_onbezet == tijd:
                    apparaat.bezet = False
    
    def gemiddelde_wachttijd(self) -> float:
        totale_wachttijd = 0
        for sporter in self.sporters:
            totale_wachttijd  += sporter.wachttijd

        gem_wachttijd   = totale_wachttijd / self.bezoekers if self.bezoekers > 0 else 0
        return gem_wachttijd

    def gemiddelde_tijd_in_gym(self) -> float:
        totale_tijd_in_gym = 0

        for sporter in self.sporters:
            totale_tijd_in_gym += sporter.tijd_in_gym
        
        gem_tijd_in_gym = totale_tijd_in_gym / self.bezoekers if self.bezoekers > 0 else 0
        return gem_tijd_in_gym
    
    def aantal_bezette_apparaten(self, apparaten: list[Apparaat]) -> int:
        aantal_apparaten_bezet = 0
        for apparaat in apparaten:
            if apparaat.bezet == True:
                aantal_apparaten_bezet += 1
        
        return aantal_apparaten_bezet
    
    def aantal_bezig(self):
        aantal_bezig = 0
        for sporter in self.sporters:
            if sporter.bezig == True:
                aantal_bezig += 1

        return aantal_bezig 
    
    def genereer_oefeningen(self, aantal_oefeningen: int):
        oefeningen = [
            Oefening("squats", 0, bereken_tijd_oefening(15), Oefening.benodigde_apparaten("squats")),
            Oefening("push-ups", 0, bereken_tijd_oefening(10), Oefening.benodigde_apparaten("push-ups")),
            Oefening("deadlifts", 0, bereken_tijd_oefening(15), Oefening.benodigde_apparaten("deadlifts")),
            Oefening("bench press", 0, bereken_tijd_oefening(15), Oefening.benodigde_apparaten("bench press")),
            Oefening("pull-ups", 0, bereken_tijd_oefening(10), Oefening.benodigde_apparaten("pull-ups")),
            Oefening("lunges", 0, bereken_tijd_oefening(15), [], Oefening.benodigde_apparaten("lunges")),
            Oefening("hardlopen", 0, bereken_tijd_oefening(15), Oefening.benodigde_apparaten("loopband")),
            Oefening("plank", 0, bereken_tijd_oefening(5), []),
            Oefening("bicep curls", 0, bereken_tijd_oefening(10), Oefening.benodigde_apparaten("bicep curls"))
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
        dumbbells_bezet = self.aantal_bezette_apparaten(self.dumbbells)        
        barbells_bezet = self.aantal_bezette_apparaten(self.barbells)        
        bezig = self.aantal_bezig()

        return f"Aantal sporters: {self.bezoekers} \
                 Aantal bezige sporters: {bezig} \
                 Aantal bezette loopbanden: {loopbanden_bezet} \
                 Aantal bezette banken: {banken_bezet} \
                 Aantal bezette racks: {racks_bezet} \
                 Aantal bezette dumbbells: {dumbbells_bezet} \
                 Aantal bezette barbells: {barbells_bezet}"
    
    
