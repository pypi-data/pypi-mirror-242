# created by Florian Schunck on 11.11.2019
# Project: timepath
# Short description of the feature: DEBkiss inspired model implementation in Python
# Resources:
# - Jager, Tjalling (2018): DEBkiss. A simple framework for animal energy budgets
#
# ------------------------------------------------------------------------------
# Open tasks:
# LATER: plot functional response (f) or food flux over time in relation to pars
# LATER: implement growth shape correction into food flux (and others? at the
#        moment bowl shape assumed)
# TODO: calculate dissipation fractions of feeding growth and reproduction.
#        Together with the dissipated fluxes like maintenance and maturation,
#        it will make up the respiration flux.
# DONE: Revise get eaten formula!!! There is a problem, since in the loop,
#       first, all animals are fed, and then the food density is decreased
#       asymptotically (step by step) thus, less food is taken out of the world
#       than was actually consumed!
# DONE: add step function for objects which in Invertebrata is specified in
#       life. These functions should contain generalized behavior
# ------------------------------------------------------------------------------

# DECLARATIONS -----------------------------------------------------------------
# capital 'A' at the end of a variable declaration means the vairable is
# area dependent

# A:       area dependent
# V:       volume dependent

# m_a:     assimilate mass
# m_f:     food mass
# m:       body mass
# l_e:     length of environment
# l:       length of body

import numpy as np
from functools import wraps
from itertools import count

from ibes.utils.errors import errormsg
from ibes.objects.housekeeping import LOGGER
# PRIMARY PARAMETERS ===========================================================
# FEEDING ----------------------------------------------------------------------

def internal_event(event_func):
    @wraps(event_func)
    def wrapped_event_func(self):
        self.current_func_name = event_func.__name__
        self.time_dependence = False
        event_func(self)
        self.time_dependence = "Undefined"
        self.current_func_name = "Undefined"
    return wrapped_event_func

def external_environmental_event(event_func):
    @wraps(event_func)
    def wrapped_event_func(self, param):
        self.current_func_name = event_func.__name__
        self.time_dependence = False
        event_func(self, param)
        self.time_dependence = "Undefined"
        self.current_func_name = "Undefined"
    return wrapped_event_func

def process_function(step_func):
    @wraps(step_func)
    def wrapped_proc_func(self):
        self.current_func_name = step_func.__name__
        self.time_dependence = True
        step_func(self)
        self.time_dependence = "Undefined"
        self.current_func_name = "Undefined"
    return wrapped_proc_func


class Nothing:
    def __init__(self):
        self.agents = []
        self.environment = ['None']


class Common:
    """
    This model is written in seconds. dt has to be supplied in a value of hours.
    All rate constants are converted to parts or multiples of hours
    """
    _structure = False
    _pool = False
    _world = False
    _subsystem = False
    _ids = count(0)

    def __init__(
        self,
        environment="nothing",
        structure_params={},
        X0 = {}
    ):
        self.structure_params = structure_params
        # if an empty dictionary is passed all state variables are
        # initialized with zeros
        self.X0 = X0 
        self.agents = []
        self.dead_agents = []
        if environment == "nothing":
            environment = Nothing()
        self.environment = environment
        self.rates = {}
        self.pools = {}
        self.interactions = {}
        self.current_func_name = "Undefined"
        self.time_dependence = "Undefined"
        # fundamental properties of the object
        self.id = next(self._ids)  # advances the count variable by one
        self.place(environment)

    def __str__(self):
        if isinstance(self.environment, Nothing):
            return "-".join([type(self).__name__, str(self.id)])
        return " ".join(("-".join([
            type(self).__name__, str(self.id)]), "in", str(self.environment)))

    def __repr__(self):
        return "-".join([type(self).__name__, str(self.id)])

    def correct_overshoot(self, pool):
        """
        assumption: food uptake of all organisms is reduced equally for each
        agent. Relative to their normal food consumption. This should be the
        weakest possible assumption.
        The error results from overshoot due to large timesteps.
        """
        if pool.negative_state:
            return pool.mass / np.abs(pool.temp_flux)

        return 1

    def process_multiple_pools(self, mass_to_flux, base_pool_type):
        num_stab_add = 1e-100
        type_pools = [pool for _, pool in self.environment.pools.items() 
            if isinstance(pool, base_pool_type)]
        
        total_mass = np.sum([p.mass for p in type_pools])

        pot_flux = mass_to_flux(total_mass)

        fluxes = []
        for pool in type_pools:
            overfeeding_correction = self.correct_overshoot(pool)
            fractional_flux = (
                pool.mass / (total_mass + num_stab_add) * 
                overfeeding_correction *
                pot_flux
            )
            fluxes.append(fractional_flux)
        
        return type_pools, fluxes

    def flux(self, flux, pool_in=None, pool_out=None):
        # flow from pool_out to pool_in
        assert self.time_dependence != "Undefined", errormsg(
            """
            No flux-type (time-dependent/time-invariant) was found. Make sure
            you add a decorator to all functions that involve a flux. Use
            @internal_event for functions that involve fluxes that are time 
            invariant. I.e. will have the same size regardless of the timestep
            length
            Use @process_function for methods involving time dependent fluxes.
            This error can also arise from using a process function in the wrong 
            class. fluxes belong to Pools or higher level entities. Hence,
            they should only be called with self.flux(...) not 
            """
        )

        if pool_out is not None:
            if isinstance(pool_out, type):
                pool_out = self.pools[pool_out]

        if pool_in is not None:
            if isinstance(pool_in, type):
                pool_in = self.pools[pool_in]
        
        if pool_out is not None:
            pool_out.fluxes.append(
                (pool_in, (self.current_func_name, -flux, self.time_dependence))
            )

        # flow into pool in from pool out
        if pool_in is not None:
            pool_in.fluxes.append(
                (pool_out, (self.current_func_name, +flux, self.time_dependence))
            )

    def reset(self):
        self.volume = 0
        self.agents = []
        self.environment = None
        self.pools = []

    def place(self, env):
        """
        if object is a pool, make sure a pool of the same type is not already 
        present. This would lead to problems.
        if object is not a pool, make sure no duplicates of the agent
        are created in the environment.
        """
        if self._pool:
            if not type(self) in env.pools:
                self.environment = env
                env.pools.update({type(self): self})
        elif self._structure:
            pass
        else:
            # TODO: what to do with objects that are placed in Nothing?
            if not self in env.agents:
                self.environment = env
                env.agents.append(self)

    def remove_self_from_environment(self):
        index_self = self.environment.agents.index(self)
        self.environment.agents.pop(index_self)
        LOGGER.log("info", f"{self} died and was removed from agents")

    def get_or_create_pool(self, pool):
        """
        get pool fetches a pool from a list if present. If the pool does
        not exist, the a new pool is instanciated
        """
        try:
            # no assertion of len 1 necessary, because it is asserted on creation that
            # no more than one instance per type can exist in pools
            return self.pools[pool]
            
        except KeyError:
            return pool(environment=self)

    def set_rates(self, substance, uptake=0, elimination=0, decay=0):
        """
        set rates for uptake and elimination of a substance.
        substance   must be of class pool
        """
        self.rates.update({
            substance: {
                "uptake": uptake,
                "elimination": elimination,
                "decay": decay
            }
        })  