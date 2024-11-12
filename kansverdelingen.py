import numpy as np

def bereken_tijd_oefening(mean_duration: float) -> float:
    """
    Genereer oefentijd volgens Weibull-verdeling
    """
    k = 2.5  # shape parameter
    # lambda parameter zo gekozen dat expected value = mean_duration
    lambda_param = mean_duration / np.random.gamma(1 + 1/k)
    
    return np.round(np.random.weibull(k) * lambda_param).astype(int)

def bereken_tijd_in_gym() -> float:
    """
    Genereer gymtijd volgens Erlang-verdeling (speciaal geval van Gamma-verdeling)
    """
    k = 3  # shape parameter
    scale = 25  # Voor gemiddelde van 75 minuten

    return np.round(np.random.gamma(k, scale)).astype(int)

def bereken_aantal_nieuwe_sporters(minute: float) -> int:
    """
    Genereer aantal nieuwe sporters volgens Poisson-verdeling
    """
    if (60 <= minute < 180) or (690 <= minute < 840):
        return np.random.poisson(11/6)  # Piekuren
    
    return np.round(np.random.poisson(1)).astype(int)  # Normale uren