from gym import Gym

def simulatie(looptijd, loopbanden, racks, banken, barbells, dumbbells):
    gym = Gym(loopbanden, racks, banken, barbells, dumbbells)
    
    for minuut in range(looptijd):
        gym.simuleer_tijdstap(minuut)
        if (minuut % 30) == 0:
            print("Minuut: ", minuut)
            print(gym)

    print(gym)
