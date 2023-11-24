
class SciNum:
    def __init__(self, value, power_of_ten, unit):
        self.value = value
        self.power_of_ten = power_of_ten
        self.unit = unit

    # Returns the value without powers of ten
    def getVal(self):
        return self.value

    # Returns the power of ten
    def getPow(self):
        return self.power_of_ten

    # Returns the metric unit
    def getUnit(self):
        if self.unit == "":
            return "This number has no units."
        else:
            return self.unit

    # Returns the number without units rounded up
    def getRoundFloat(self):
        return round(self.value) * pow(10, self.power_of_ten)

    # Returns the full number with value, powers of 10 and units, rounded up
    def getRoundFullStr(self):
        return str(round(self.value)) + " × 10^(" + str(self.power_of_ten) + ") " + self.unit

    # Returns the full number with value, powers of 10 and units
    def getFullStr(self):
        return str(self.value) + " × 10^(" + str(self.power_of_ten) + ") " + self.unit

    # Returns the number without units
    def getFloat(self):
        return self.value * pow(10, self.power_of_ten)


# Pi
pi = SciNum(22/7, 0, "")

# Euler's Constant
e = SciNum(2.7182818285, 0, "")

# Value of Phi / φ
phi = SciNum(1.61803399, 0, "")
φ = phi

# Speed of Light
c = SciNum(2.99792458, 8, "m/s")

# Planck Constant
h = SciNum(6.62607015, -34, "J⋅s")

# H-Bar
hbar = SciNum(1.054571817, -34, "J⋅s")

# Magnetic permeability in vacuum
μ0 = SciNum(1.25663706212, -6, "N / A^2")
u0 = μ0
magper = u0

# Electric permittivity in vacuum
ε0 = SciNum(8.8541878128, -12, "F / m")       # "8.8541878128(13)×10−12 F⋅m−1"
e0 = ε0
elecper = e0
