# Mass class
class Var:
    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return str(self.x)

class Statevar(Var):
    def __init__(self, x, record={}, i=0):
        super().__init__(x)
        if len(record) == 0:
            record = {0: self.x}
            i = 0
        self.i = i
        self.record = record

    def update(self, other, op):
        mul = 1
        if op == "sub":
            mul = -1
        record = self.record.copy()
        i = self.i + 1
        env = self.env
        for key, val in other.record.items():
            record.update({key+i: val*mul})

        kwargs = {"env": env, "record": record, "i": i}

        return kwargs

class Timestep(Var):
    pass

class Rate(Var):
    pass

class Mass(Statevar):
    def __init__(self, x, env=None, **kwargs):
        super().__init__(x, **kwargs)
        self.env = env

    def __add__(self, other):
        x = self.x + other.x
        kwargs = self.update(other, "add")
        return Mass(x, **kwargs)
    
    def __sub__(self, other):
        x = self.x - other.x
        kwargs = self.update(other, "sub")
        return Mass(x, **kwargs)

    def __mul__(self, other):
        assert isinstance(other, Rate)
        x = self.x * other.x
        return dMdt(x)

class dMdt(Rate):
    def __mul__(self, other):
        assert isinstance(other, Timestep)
        x = self.x * other.x
        return Flux(x)

class Flux(Mass):
    pass

# a = Mass(1.2)
# b = Mass(5)
# c =a + b
# d = Mass(2)
# e = c -d

# print(e)


# dt = Timestep(10)

# mass = Mass(500)
# rate = Rate(0.01)

# dmdt = mass * rate

# flux = dmdt * dt

# mass += flux
# mass -= flux
