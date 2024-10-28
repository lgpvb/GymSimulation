class Apparaat:
    def __init__(self, naam):
        self.naam = naam
        self.bezet = False
        self.resterende_tijd = 0

    def gebruik_apparaat(self, duur):
        self.bezet = True
        self.resterende_tijd = duur

    def vrij_apparaat(self):
        self.bezet = False
        self.resterende_tijd = 0
