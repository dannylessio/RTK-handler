class Projection(object):
    """ This class handles all the parameters regarding one projection """

    def __init__(self, name, angle, Niso_u, Niso_v, io):
        self.name = str(name)
        self.angle = float(angle)
        self.Niso_u = float(Niso_u)
        self.Niso_v = float(Niso_v)
        self.io = float(io)
