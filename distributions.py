import numpy as np

def generate_exercise_duration(mean_duration: float) -> float:
    """
    Genereer oefentijd volgens Weibull-verdeling
    k = 2.5 (shape parameter) geeft realistische spreiding
    """
    k = 2.5  # shape parameter
    # lambda parameter zo gekozen dat expected value = mean_duration
    lambda_param = mean_duration / np.gamma(1 + 1/k)
    
    return np.random.weibull(k) * lambda_param

def generate_gym_duration() -> float:
    """
    Genereer totale gymtijd volgens Erlang-verdeling
    k = 3 geeft realistische vorm
    """
    k = 3  # shape parameter
    scale = 25  # Voor gemiddelde van 75 minuten

    return np.random.gamma(k, scale)

def generate_arrivals(minute: float) -> int:
    """
    Genereer aantal nieuwe sporters volgens Poisson-verdeling
    """
    if (60 <= minute < 180) or (690 <= minute < 840):
        return np.random.poisson(2)  # Piekuren
    
    return np.random.poisson(1)  # Normale uren