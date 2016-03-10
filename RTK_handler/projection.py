class Projection( object ):
    """ This class handles all the parameters regarding one projection """

    def __init__(self, name, angle, isox, isoy, correction):
        self.name = name
        self.angle = float(angle)
        self.isox = float(isox)
        self.isoy = float(isoy)
        self.correction = float(correction)

    def getOneOverCorrection(self):
        return float(1 / self.correction)
