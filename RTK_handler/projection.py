class Projection(object):
    """ This class handles all the parameters regarding one projection """

    def __init__(self, name, angle, N_off_u, N_off_v, io):
        self.name = name
        self.angle = float(angle)
        self.N_off_u = float(N_off_u)
        self.N_off_v = float(N_off_v)
        self.io = float(io)
