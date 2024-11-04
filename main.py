from optimalisatie import monte_carlo_optimalisatie, wachttijd_analyse
from simulatie import simulatie
from gym import Gym

if __name__ == "__main__":
    """ 
    loopbanden = int(input("Aantal loopbanden: "))
    racks = int(input("Aantal racks: "))
    banken = int(input("Aantal banken: "))
    """
    looptijd = 990 # Gym opent om 7:00 en sluit 23:30. 990 = 23*60 + 30 - 7*60

    simulatie(looptijd, loopbanden=20, racks=20, banken=20, barbells=20, dumbbells=20)

    """  
    # Tijdstippen om te analyseren (in minuten vanaf 7:00)
    tijdstippen = [i for i in range(0, 990, 30)]  # Elke 30 minuten van 7:00 tot 23:30

    # Voer Monte Carlo-optimalisatie uit
    beste_tijd_mc, gemiddelde_wachttijd_mc = monte_carlo_optimalisatie(gym, tijdstippen)
    print(f"Beste tijdstip (Monte Carlo): {beste_tijd_mc} met gemiddelde wachttijd {gemiddelde_wachttijd_mc:.2f}")

    # Voer wachttijdanalyse uit
    beste_tijd_analyse, gemiddelde_wachttijd_analyse = wachttijd_analyse(gym, tijdstippen)
    print(f"Beste tijdstip (Wachttijd Analyse): {beste_tijd_analyse} met gemiddelde wachttijd {gemiddelde_wachttijd_analyse:.2f}")
    """