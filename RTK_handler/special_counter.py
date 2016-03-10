class SpecialCounter( object ):

    def __init__(self, number_of_digits):
        self.counter = 0
        self.zero = "0"
        self.number_of_digits = number_of_digits
        self.value = (self.zero * self.number_of_digits)

    def increment(self):
        self.counter = self.counter + 1
        self.value = (self.zero * (self.number_of_digits -
                                   len(str(self.counter)))) + str(self.counter)

    def getValue(self):
        return self.value
