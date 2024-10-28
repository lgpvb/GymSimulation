from gym import Gym
import numpy as np

def monte_carlo_optimalisatie(gym: Gym, tijdstippen: list[int] , runs=100):
    # Voor elk tijdstip voeren we de simulatie meerdere keren uit en berekenen het gemiddelde
    resultaten = {}
    for tijd in tijdstippen:
        wachttijden = []
        for _ in range(runs):
            gym.simuleer_tijdstap(tijd)
            wachttijden.append(gym.gemiddelde_wachttijd())
        resultaten[tijd] = np.mean(wachttijden)
    beste_tijd = min(resultaten, key=resultaten.get)
    return beste_tijd, resultaten[beste_tijd]

def wachttijd_analyse(gym: Gym, tijdstippen: list[int]):
    # Analyseer de gemiddelde wachttijden voor alle tijdstippen
    wachttijden_per_tijdstip = {}
    for tijd in tijdstippen:
        gym.simuleer_tijdstap(tijd)
        wachttijden_per_tijdstip[tijd] = gym.gemiddelde_wachttijd()
    
    optimale_tijd = min(wachttijden_per_tijdstip, key=lambda k: sum(wachttijden_per_tijdstip[k].values()))
    return optimale_tijd, wachttijden_per_tijdstip[optimale_tijd]
