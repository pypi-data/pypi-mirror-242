import numpy as np
from itertools import count
from prettytable import PrettyTable

from ibes.objects.base import Common
from ibes.objects.housekeeping import CLOCK, BALANCE, SCHEDULE, LOGGER

class Pool(Common):
    """
    of static objects only one can ever exist in any environment. Hence the
    concentration of the object is the environmental concentration

    Pools should not update derived variables. These calculations should be
    done in place during step methods
    """
    rates = {}
    _pool = True
    _stressor = False
    _ids = count(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = self.environment.id
        self.fluxes = []
        self.previous_flux = []
        BALANCE.pools.append(self)

    def __repr__(self):
        name = super().__repr__()
        quant = " ({:.3e})".format(getattr(self, self._dim))
        return name + quant

    def __str__(self):
        return self.flux_table(self.fluxes)

    def print_previous_flux(self):
        print(self.flux_table(self.previous_flux))

    def flux_table(self, fluxes):
        name = type(self).__name__
        tbl = PrettyTable()
        tbl.field_names = ["Process", "Pool", "influx", "outflux", "from to"]
        inflow = 0
        outflow = 0
        tbl, inflow, outflow = self.five_col_style(
            fluxes, tbl, inflow, outflow)
        tbl.add_row(["===", "===", "===", "===", "==="])
        tbl.add_row(["", "Sum", inflow, outflow, ""])
        tbl.align = "r"
        return tbl.get_string()

    def three_col_style(self, fluxes, tbl, inflow, outflow):
        for (pool, (step, value, time_dependent)) in fluxes:
            if value < 0:
                tbl.add_row([type(pool).__name__, "", str(value)])
                outflow += value
            else:
                tbl.add_row([type(pool).__name__, str(value), ""])
                inflow += value
        return tbl, inflow, outflow

    def four_col_style(self, fluxes, tbl, inflow, outflow):
        if len(fluxes) == 0:
            tbl.add_row([type(self).__name__, "", "", ""])
        for (pool, (step, value, time_dependent)) in fluxes:
            if value < 0:
                tbl.add_row([type(self).__name__, "",
                            str(value), type(pool).__name__])
                outflow += value
            else:
                tbl.add_row([type(self).__name__, str(
                    value), "", type(pool).__name__])
                inflow += value
        tbl.add_row(["---", "---", "---", "---"])

        return tbl, inflow, outflow

    def five_col_style(self, fluxes, tbl, inflow, outflow):
        if len(fluxes) == 0:
            tbl.add_row(["", type(self).__name__, "", "", ""])
        for (pool, (step, value, time_dependent)) in fluxes:
            value = value * max(1, time_dependent * CLOCK.dt_to_seconds())
            if value < 0:
                tbl.add_row([step, type(self).__name__, "",
                            str(value), type(pool).__name__])
                outflow += value
            else:
                tbl.add_row([step, type(self).__name__, str(
                    value), "", type(pool).__name__])
                inflow += value
        tbl.add_row(["---", "---", "---", "---", "---"])

        return tbl, inflow, outflow

    def set_X0(self, defaults):
        try:
            x0 = self.environment.X0[type(self).__name__]
            for dimension, init_value in x0.items():
                setattr(self, dimension, init_value)
        except KeyError:
            for dimension, init_value in defaults.items():
                setattr(self, dimension, init_value)
                LOGGER.log("debug",
                    f"{self.environment}: no init value assigned to " +\
                    f"{type(self).__name__} ({dimension}), "+\
                    f"setting to: {init_value}"
                )

    def balance(self, from_pools="all", direction="all", derivative=True, 
                previous_flux=False):
        
        if previous_flux:
            fluxes = self.previous_flux
        else:
            fluxes = self.fluxes

        if from_pools != "all":
            fluxes = [(pool, flux)
                      for (pool, flux) in fluxes if type(pool) in from_pools]

        if direction == "influx":
            fluxes = [(pool, flux) for (pool, flux) in fluxes if flux[1] > 0]

        if direction == "outflux":
            fluxes = [(pool, flux) for (pool, flux) in fluxes if flux[1] < 0]

        sum_flux = 0
        for (pool, (process, flux, time_dependent)) in fluxes:
            if derivative:
                sum_flux += flux
            else:
                if time_dependent:
                    sum_flux += flux * CLOCK.dt_to_seconds()
                else:
                    sum_flux += flux

        return sum_flux

    def calc_flux(self):
        temp_flux = self.balance(derivative=False)
        self.temp_flux = temp_flux
        return temp_flux

    def update(self):
        """
        common update method for all statevariables
        """
        flux = self.temp_flux
        # backup of last flux for debugging and nulling the flux dict for next
        # step
        self.reset_flux(copy=True)
        # check if the conditions for a discrete events are given and if yes
        # schedule them
        return flux

    def reset_flux(self, copy=False):
        if copy:
            self.previous_flux = self.fluxes.copy()
        self.fluxes = []


    def reset(self):
        super().reset()

    # def reverse(self):
    #     """
    #     reverses the mass flux after an update and sets fluxes to
    #     an empty dict. Works only if update was run in test mode
    #     """
    #     if self._pool:
    #         flux = self.balance()
    #         self.mass -= flux
    #         self.concentration = self.calc_concentration()
    #         self.fluxes = []


class DerivedPool(Pool):
    _dim = "dimensionless"
    def __init__(self, **kwargs):
        setattr(self, self._dim, np.nan)
        super().__init__(**kwargs)

    def update(self, **kwargs):
        val = self.compute()
        setattr(self, self._dim, val)

    def compute(self):
        return getattr(self, self._dim)


class MassPool(Pool):
    _dim = "mass"

    def __init__(self, mass=0, density=1, **kwargs):
        super().__init__(**kwargs)
        self.set_X0(defaults={"mass": mass, "density": density})
        self.negative_state = False

    def update(self, **kwargs):
        flux = super().update(**kwargs)
        self.mass += flux

    def leftover(self):
        return self.mass + self.balance(derivative=False)

    @property
    def volume(self):
        return self.mass / self.density

class DiscretePool(Pool):
    _dim = "N"

    def __init__(self, N=0, **kwargs):
        super().__init__(**kwargs)
        self.set_X0(defaults={"N": N})

    def update(self, **kwargs):
        flux = super().update(**kwargs)
        self.N += flux
        assert self.N >= 0


class RatePool(Pool):
    _dim = "rate"

    def __init__(self, rate=0, **kwargs):
        super().__init__(**kwargs)
        self.set_X0(defaults={"rate": rate})

    def update(self, **kwargs):
        flux = super().update(**kwargs)
        self.rate += flux


class TimePool(Pool):
    _dim = "time"

    def __init__(self, time=0, **kwargs):
        super().__init__(**kwargs)
        self.set_X0(defaults={"time": time})

    def update(self, **kwargs):
        flux = super().update(**kwargs)
        self.time += flux
        assert self.time >= 0


class BooleanPool(Pool):
    _dim = "switch"

    def __init__(self, switch=1, **kwargs):
        super().__init__(**kwargs)
        self.set_X0(defaults={"switch": switch})

    def update(self, **kwargs):
        flux = super().update(**kwargs)
        self.switch += flux
        assert self.switch == 0 or self.switch == 1

class IO(MassPool):
    pass

class Biomass(MassPool):
    pass


class POM(MassPool):
    pass

class DOM(MassPool):
    pass


class DissolvedPool(MassPool):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def concentration(self, molar=False):
        conc = self.mass / self.environment.volume()
        
        if molar:
            conc = conc / self.molar_mass
        
        return conc

class CO2(DissolvedPool):
    pass


class SuspendedPool(DissolvedPool):
    pass


class Food(SuspendedPool):
    pass

        