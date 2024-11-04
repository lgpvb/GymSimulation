from queue import Queue
from typing import Self
from functools import total_ordering

@total_ordering
class Apparaat:
    def __init__(self, naam: str):
        self.naam = naam
        self.bezet: bool = False
        self.wachtrij = Queue()
        self.tijdstip_onbezet: int = 0

    def gebruik_apparaat(self, tijd: int):
        self.bezet = True
        self.tijdstip_onbezet = tijd

    def beëindig_gebruik(self, tijd: int):
        self.bezet = False
        self.tijdstip_onbezet = tijd

    def __lt__(self, other: Self):
        return self.tijdstip_onbezet < other.tijdstip_onbezet        

    def __repr__(self):
        return (f"Apparaat naam: {self.naam}, "
                f"Apparaat bezet: {self.bezet}, "
                f"Apparaat is onbezet op tijdstip: {self.tijdstip_onbezet}")

