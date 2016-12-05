class Projection(object):
    """ This class handles all the parameters regarding one projection """

    def __init__(self, name, angle, io):
        self.name = str(name)
        self.angle = float(angle)
        self.io = float(io)
