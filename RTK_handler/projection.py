class Projection( object ):
    """ This class handles all the parameters regarding one projection """

    def __init__(self, name, angle, iso_u, iso_v, io):
        self.name = name
        self.angle = float(angle)
        self.iso_u = float(iso_u)
        self.iso_v = float(iso_v)
        self.io = float(io)
