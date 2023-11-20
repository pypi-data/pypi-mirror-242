# created by Florian Schunck on 11.11.2019
# Project: timepath
# Short description of the feature: DEBkiss inspired model implementation in Python
# Resources:
# - Jager, Tjalling (2018): DEBkiss. A simple framework for animal energy budgets
#
# ------------------------------------------------------------------------------
# Open tasks:
# TODO: merge functions get_eaten and calculate_feeding_amount
#
# ------------------------------------------------------------------------------
import numpy as np

from ibes.objects.base import Common, process_function
from ibes.objects.structures import Subsystem
from ibes.objects.stressors import Chemical, Esfenvalerate
from ibes.objects.pools import POM, Food, CO2, DOM
from ibes.objects.housekeeping import CLOCK

class Water(Subsystem):
    pass

class World(Common):
    _world = True
    
    def __init__(
            self,
            # state variables
            rate_decay_esfenvalerate=0,  #[ 1 / s]
            **kwargs,  # [cm 3]
    ):
        super().__init__(**kwargs)

        # parameters
        self.name = "World"
        self.rates[Esfenvalerate] = {"decay": rate_decay_esfenvalerate}
        # initialize calculate state variables
        self.correction_overfeeding = 1
        self.graveyard = dict()

        # fluxes
        self.total_food_flux = 0

        # init actions
        self.pools.update({
            Water: Water(environment=self),
            POM: POM(environment=self),
            DOM: DOM(environment=self),
            Food: Food(environment=self),
            CO2: CO2(environment=self)
        })
        # self.calculate_feeding_amount()
        # self.organismrefs = weakref.WeakValueDictionary()

    def volume(self):
        return self.pools[Water].volume

    @process_function
    def chemical_decay(self):
        for pool_class, pool in self.pools.items():
            if isinstance(pool, Chemical):
                pot_decay = (
                    self.rates[pool_class]["decay"] * 
                    pool.concentration() * self.volume()
                )

                decay = pot_decay * self.correct_overshoot(pool)


                # here it would be easy to transfer the degraded material
                # to other pools for instance metabolite pool defined as an
                # degradation pool in the respective chemical e.g. 
                # pool_in=p.degradation_pool
                self.flux(decay, pool_out=pool, pool_in=DOM)


    # HISTORY ##################################################################
    def step(self):
        self.chemical_decay()
        # self.kinetic(Esfenvalerate)
        # self.get_eaten()
        # self.check_survival()
        # self.calculate_feeding_amount()

    def internal_events(self):
        pass

    def check_survival(self):
        self.mass_om += sum([a.mass for a in self.agents if (a.inside_environment and not a.alive)])
        survivors = [a for a in self.agents if (a.inside_environment and a.alive)]
        corpses = [a for a in self.agents if (a.inside_environment and not a.alive)]
        
        self.agents = survivors
        self.dead_agents.extend(corpses)
    
    
    # UPDATE STATE VARIABLES ###################################################
    # FOOD DENSITY -------------------------------------------------------------
    # def get_eaten(self):
    #     """
    #     each animal in world consumes food
    #     """
    #     self.total_food_flux = 0
    #     for a in self.agents:
    #         self.total_food_flux += a.flux_food

    #     self.mass_food = self.volume * self.food_density

    #     if self.mass_food >= self.total_food_flux:
    #         self.food_density = ((self.mass_food - self.total_food_flux) /
    #                              self.volume)
    #     else:
    #         # Warning("More food was consumed than available."
    #         #         "Setting mass_food = 0, consider decreasing step size"
    #         #         "This might be a serious problem, which is addressed in the future")
    #         print(self.mass_food, self.total_food_flux)
    #         self.food_density = 0
    #         self.mass_food = 0


    # def calculate_feeding_amount(self):
    #     """
    #     if there are many individuals in the world, problems emerge
    #     because of discretization. Since food is consumed for a defined
    #     period of time, it happens that more food is consumed than actually
    #     is available since food is calculated based on previous availability.

    #     Ideally this would be solved by adaptively decreasing timestep length,
    #     when food availability is not large enough.

    #     At this moment the problem is confronted by calculating a correction
    #     factor when overfeeding occurs. Individual food fluxes are then
    #     multiplied with correction factors to reduce feeding accordingly
    #     """
    #     flux_food_total = []
    #     self.correction_overfeeding = 1 # reset before calculating amount of overfeeding
    #     for a in self.agents:
    #         flux_food_total.append(a.feed_from_environment())

    #     required_food = np.sum(flux_food_total)

    #     if required_food == 0:
    #         self.correction_overfeeding = 1
    #     else:
    #         correction = round_decimals_down(self.mass_food / required_food, 3)
    #         self.correction_overfeeding = np.min((1, correction))


