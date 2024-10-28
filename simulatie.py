from gym import Gym

def simulatie(looptijd, loopbanden, racks, banken):
    gym = Gym(loopbanden, racks, banken)

    for minuut  in range(looptijd):
        gym.simuleer_tijdstap(minuut)

    print(gym)
