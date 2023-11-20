# created by Florian Schunck on 11.11.2019
# Project: timepath
# Short description of the feature: DEBkiss inspired model implementation in Python
# Resources:
# - Jager, Tjalling (2018): DEBkiss. A simple framework for animal energy budgets
#
# ------------------------------------------------------------------------------
# Open tasks:
#
#
# ------------------------------------------------------------------------------
import numpy as np
from itertools import count
from datetime import timedelta

from ibes.utils.config import CONSTANTS
from ibes.objects.base import Common, process_function, internal_event
from ibes.objects.pools import DerivedPool, RatePool, TimePool, Food, Biomass, POM
from ibes.objects.stressors import Esfenvalerate, Chemical
from ibes.objects.structures import Subsystem, PeripheralNS, Skin
from ibes.objects.housekeeping import Event, CLOCK, SCHEDULE, LOGGER

class Body(Biomass, Subsystem):
    _ids = count(0)
    elements = [Skin]


class Outlet(Biomass, Subsystem):
    def act(self):
        super().act()
        self.excrete()

    @internal_event
    def excrete(self):
        faeces = self.mass
        pom = self.environment.environment.pools[POM]
        # check if this works with internal event
        self.flux(faeces, pool_in=pom, pool_out=self)

    # def update(self, **kwargs):
    #     super().update(**kwargs)
    #     if self.mass < 0:
    #         print(self.mass)

class Assimilates(Biomass):
    pass


class Maintenance(Biomass):
    pass


class Age(TimePool):
    pass        

class Damage(Biomass):
    # def update(self, **kwargs):
    #     if self.balance(derivative=False) > 1e-10:
    #         print("damage")
    #     super().update(**kwargs)
    pass

class Hazard(DerivedPool):
    _dim = "rate"
    def compute(self):
        return self.environment.hazard()

class Repair(RatePool):
    def update(self, **kwargs):
        super().update(**kwargs)
        self.rate = np.max([0, self.rate])

class Organism(Common):
    _ids = count(0)

    _dynamic = True
    # creates a class wide variable which shows the count of daphnia
    def __init__(
        self,
        # state variables
        rate_damage_baseline=0, # mass specific (increases with dry mass (cell mass) of the organism)
        rate_repair_decay=0,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # fundamentals 
        self.alive = True
        self.cause_of_death = ""
        
        self.rate_damage_baseline = rate_damage_baseline
        self.rate_repair_decay = rate_repair_decay

        # init actions 
        self.pools.update({
            Body: Body(environment=self),
            Maintenance: Maintenance(environment=self),
            Assimilates: Assimilates(environment=self),
            Damage: Damage(environment=self),
            Repair: Repair(environment=self),
            Outlet: Outlet(environment=self),
            Age: Age(environment=self),
            Hazard: Hazard(environment=self)
        })


    def volume(self):
        """
        assumption: volume is determined by body mass divided by density
        """
        return self.pools[Body].mass / self.pools[Body].density

    @process_function
    def distribute_assimilates(self):
        pass

    @process_function
    def somatic_maintenance(self):
        pass

    @process_function
    def feed_assimilate_digest(self):
        pass
       
    @process_function
    def get_older(self):
        self.flux(1, pool_in=Age)

    @process_function
    def take_up(self):
        """
        Chemical uptake, elimination and environmental decay is split up accross
        three functions (take_up, elimination in Organism and decay in World)

        simplified toxicant uptake kinetics with a dominat uptake/elimination rate
        additional environmental decay after Kooijman 2000 p.190/191

        multiplied by structural body volume the equation returns fluxes.

        rate: 1/t (dimensionless time-1)
        decay_env: environmental decay rate (1 / t - dimensionless time)
        X[0]: environmental concentration (M / V)
        X[1]: internal concentration (M / V)

        -- update 08.05.2021 --
        if in doubt once more. Read pages 190-193 of Kooijman 2000 and ideally read
        own notes from 08. May 2021

        the simplest model will just fit three parameters:
         - for the uptake rate for esfenvalerate
         - elimination rate for esfenvalerate
         - environmental decay.

        Since this model at the moment must only capture Esfenvalerate this is
        enough. However, as I know that Octanol Water Partitioning Coefficient
        for Esfenvalerate is 10^6.2 (log Pow = 6.2), this is very high. It means
        the compund is extremely lipophillic and has a large strucutre. Hence,
        uptake will be slow and the partitioning will be hugely favoured towards
        the organism. Although the relations regarding partition ~ Pow are
        said they do not hold for values > log Pow of 6. It would be interesting
        to know more about this.

        For the model results it implies that I should expect a slow uptake rate
        and an extremely slow elimination rate to achive this scenario.

        This model was formulated in Hawker and Connell 1985 but is a very simple
        ordinary system of ODEs which have the special case for the classical
        diffusion or conduction model where elimination and uptake are equal

        TODO: Note, that at the moment steady state concentration is equal in
              all individuals, because uptake is coupled to volume. This
              is actually the smallest assumption and therefore I like it a lot
              because it incorporates one facet of the timing
        """
        for pool_class, ext_pool in self.environment.pools.items():
            if isinstance(ext_pool, Chemical):
                pot_uptake = (
                    self.rates[pool_class]["uptake"] *
                    ext_pool.concentration() * self.volume()
                )

                uptake = pot_uptake * self.correct_overshoot(ext_pool)
                # here it would be easy to transfer the degraded material
                # to other pools for instance metabolite pool defined as an
                # degradation pool in the respective chemical e.g.
                # pool_in=p.degradation_pool
                int_pool = self.get_or_create_pool(pool_class)
                self.flux(uptake, pool_out=ext_pool, pool_in=int_pool)

    @process_function
    def eliminate(self):
        for pool_class, int_pool in self.pools.items():
            if isinstance(int_pool, Chemical):
                pot_elimination = (
                    self.rates[pool_class]["elimination"] *
                    int_pool.concentration() * self.volume()
                )

                max_elimination = int_pool.mass / CLOCK.dt_to_seconds()
                elimination = np.min([pot_elimination, max_elimination])

                # here it would be easy to transfer the degraded material
                # to other pools for instance metabolite pool defined as an
                # degradation pool in the respective chemical e.g.
                # pool_in=p.degradation_pool
                self.flux(elimination, pool_out=int_pool, pool_in=Outlet)


    @process_function
    def reduce_repair_rate(self):
        """
        this is exponential decay. Not sure if this is a good assumption
        alternative models are:
        this would be a 2nd order ode
        - linear decrease
        - logistic decrease (favoured because it could be interpreted with 
          cells of an multicellular organism that have a normally distributed
          life expectancy (as the number of cell divisions- relating to 
          telomeres although it is unclear whether this concept really applies))
        - inverted exponential 
        """
        # linear
        rate_flux = self.rate_repair_decay
        self.flux(rate_flux, pool_out=Repair)
        
        # exponential decay 

    @process_function
    def take_damage(self):
        baseline_damage = self.rate_damage_baseline * self.pools[Body].mass
        # self.damage.increase(baseline_damage)
        self.flux(baseline_damage, pool_in=Damage, pool_out=Body)

    def bodymass_dependent_repair(self):
        # usage of leftover here is very important. If only balance() is used
        # accumulated damage cannot be reduced. If only mass is used, the
        # equation becomes a time dependent pool
        damage = self.pools[Damage].mass / \
            CLOCK.dt_to_seconds() + self.pools[Damage].balance()
        # damage = self.pools[Damage].balance()
        max_repair = self.pools[Repair].rate * self.pools[Body].mass

        # if damage > max_repair:
        #     print("max repair")

        return np.min([damage, max_repair])

    def damage_dependent_repair(self):
        return self.pools[Damage].mass * self.pools[Repair].rate

    @process_function
    def repair(self):
        """
        here I repair damage proportional to mass. It might be interesting
        to select another scaling here (or in damage base rate) to see
        if the proportion alone determines a reasonable life expectancy
        Repair is linked to maintenance rate and thus indirect to growth
        and reproduction because damage increases the repair rate of an organism
        and by increasing maintenance rate reduces resources available for 
        growth and reproduction
        """
        repair = self.bodymass_dependent_repair()
        # repair = self.damage_dependent_repair()

        # mobilize assimilates for repair via maintenance
        self.flux(repair, pool_out=Assimilates, pool_in=Maintenance)
        # repair body tissue
        self.flux(repair, pool_out=Maintenance, pool_in=Body)
        # eject replaced damaged cells
        self.flux(repair, pool_out=Damage, pool_in=Outlet)

        # TODO: here dissipation fluxes could also play a role

    def hazard(self):
        """
        # FIXME: this is a derived quantity from state variables (step 3)
        damaged tissue has very little influence on repair, and thus on
        maintenance if mass_damaged is directly proprotional to hazard.
        Why? Because the damaged mass has to be very very low, so survival
        times are reasonable. This in turn means, that almost nothing 
        has to be repaired.
        And this! is the beauty of actually working with numbers, because
        now I know that either what I learned now is true - or that the
        damage only produces proportional damage, downscaled by some factor

        This has to be evaluated systematically and written down!
        """
        if self.pools[Body].mass == 0:
            return 0.0
        # with .balance() hazard fluxes should correspond to increment 
        # reduction of hazard rates
        return self.pools[Damage].mass 
        # frac_damaged /= 100000000000 # scaling constant. Should only be used

    def will_reproduce(self):
        pass

    def will_survive(self):
        # TODO: Make sure there are no numeric issues with the hazard estimation
        # see nebo graph for the problem of large timestep in hazard overestimation
        # in general the hazard will be overestimated by ΔH * Δt / 2
        # so a potential fix would be 
        # p_overest = self.pools[Hazard].balance(previous_flux=True) / 2
        # p = self.pools[Hazard].rate * CLOCK.dt_to_seconds() - p_overest
        p = self.hazard() * CLOCK.dt_to_seconds()
        p = np.clip(p, 0, 1)
        # this is a bernoulli trial (due to n=1)
        death = np.random.binomial(size=1, n=1, p=p)[0]
        if death == 1:
            D = Event(CLOCK.time, self, self.death)
            SCHEDULE.add(D)

    @internal_event
    def death(self):
        self.become_pom()
        self.remove_self_from_environment()

    @internal_event
    def become_pom(self):
        for pool_class, pool in self.pools.items():
            if issubclass(pool_class, Biomass):
                self.flux(pool.leftover(), self.environment.pools[POM], pool)
  

    def model_subsystems(self):
        """
        interact with pool environment (World, Daphnids, ...) based on 
        the pool concentration
        """
        # import of organism classes in this module is not possible due to
        # circular reference error. I have to handle this differently
        
        for name, system in self.pools.items():
            if issubclass(name, Subsystem):
                # TODO: pool should also be removed from affected, once
                # pool.concentration drops to zero again
                system()

    def step(self):
        """
        if repair takes place after d_damage_dt, hazard will be zero always
        as long as damage mass < max repair. This is numerically more 
        stable, but will also lead to the problem that early death, before
        repair has decayed sufficiently is impossible.
        """
        self.take_up()
        self.eliminate()
        self.model_subsystems()
        self.feed_assimilate_digest()
        self.somatic_maintenance()
        self.take_damage()
        self.repair()
        self.distribute_assimilates()
        # self.hazard()
        self.reduce_repair_rate()
        self.get_older()

    def internal_events(self):
        self.will_reproduce()
        self.will_survive()

class Guts(Biomass):
    pass

class Reprobuffer(Biomass):
    pass

class Eggbuffer(Biomass):
    pass

class Eggclutch(Biomass):
    pass

class ReproClock(TimePool):
    pass

class NervousSystem(Subsystem, Biomass):
    _status = "transmission"
    _ids = count(0)
    elements = [PeripheralNS]
    transmission = 1.0

    def react(self):
        """reactions to stimuli in internal pools"""
        super().react()
        # hypothesis 1:
        # influence on damage
        self.nerve_damage()

    @process_function
    def nerve_damage(self):
        # relate state to damage
        signal_disturbance = self.cascade_effects()
        damage = signal_disturbance * self.environment.pools[Body].mass

        if damage > 0:
            damage_pool = self.environment.pools[Damage]
            body_pool = self.environment.pools[Body]
            self.flux(damage, pool_in=damage_pool, pool_out=body_pool)

    def reduce_efficiency(self):
        pass

class Invertebrata(Organism):
    _ids = count(0)

    def __init__(
        self,
        # invertebrate parameters
        distribution,
        search_rate_max,
        assimilation_rate_max,
        maintenance_rate_max,
        mass_puberty_threshold,
        spawning_interval,
        egg_dry_mass,  # mg
        birth_success=1.0,
        assimilation_yield=float(CONSTANTS["DEB-invertebrata"]["assimilation_yield"]),
        # maintenance_yield = 0.8,
        growth_yield=float(CONSTANTS["DEB-invertebrata"]["growth_yield"]),
        structure_yield=float(CONSTANTS["DEB-invertebrata"]["structure_yield"]),
        egg_yield=float(CONSTANTS["DEB-invertebrata"]["egg_yield"]),
        shape_correction_factor=float(CONSTANTS["DEB-invertebrata"]["shape_correction_factor"]),
        name="offspring",
        mother=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        # state variables ------------------------------------------------------
        self.stage = None
        self.inside_environment = True
        self.name = name
        self.mother = mother

        # parameters -----------------------------------------------------------

        # rate parameters dt by default is 1 
        self.search_rate_max = search_rate_max
        self.assimilation_rate_max = assimilation_rate_max
        self.maintenance_rate_max = maintenance_rate_max
        self.spawning_interval = spawning_interval

        # static parameters
        self.distribution = distribution
        self.mass_puberty_threshold = mass_puberty_threshold
        self.assimilation_yield = assimilation_yield
        self.growth_yield = growth_yield
        self.structure_yield = structure_yield
        self.egg_yield = egg_yield
        self.egg_dry_mass = egg_dry_mass
        self.shape_correction_factor = shape_correction_factor
        self.birth_success = birth_success

        # init actions ---------------------------------------------------------
        self.pools.update({
            Reprobuffer: Reprobuffer(environment=self),
            ReproClock: ReproClock(environment=self),
            Eggbuffer: Eggbuffer(environment=self),
            Guts: Guts(environment=self),
            Eggclutch: Eggclutch(environment=self),
            NervousSystem: NervousSystem(environment=self)
        })
        
    @process_function
    def will_reproduce(self):
        if self.spawn_trigger():
            R = Event(CLOCK.time, self, self.reproduce)
            B = Event(CLOCK.time, self, self.give_birth)

            # ORDER HERE IS VERY IMPORTANT!! the event which is added first 
            # will also be executed first
            SCHEDULE.add(R)
            SCHEDULE.add(B)

        # advances reproclock by 1 timestep
        self.flux(1, pool_in=ReproClock)


    def step(self):
        """
        chains methods, which are available to agents. Default method, which
        can be replaced
        """
        super().step()

    @process_function
    def assimilate_from_egg(self):
        """
        Food flux from egg, if the eggbuffer is sufficiently large
        see equation 2.7: The assimilation is f * JAm * L^2. Together with
        equation 2.5, we see though that this is just Jx * yAX. Namely, The
        food flux multiplied by the assimilation yield. Embryos assimilate
        their egg buffer at the maximum rate for their structural size
        """
        f = 1  # because when feeding from egg -> f = 1
        volume = self.volume()
        pot_flux_egg = f * self.assimilation_rate_max * volume ** (2 / 3)
        assimilation_flux = np.min([
            pot_flux_egg, 
            self.pools[Eggbuffer].mass / CLOCK.dt_to_seconds()
        ])

        self.flux(assimilation_flux, pool_in=Assimilates, pool_out=Eggbuffer)

    def functional_response(self, food_density):
        """
        scaled functional response is a value between [0,1] and relates food
        (hyperbolic function of food density) concentration in the environment
        with maximum feeding and searching rates
        
        half_saturation_food_density is only determined by fixed parameters
        """
        feeding_rate = self.assimilation_rate_max / self.assimilation_yield 
        half_saturation_food_density = feeding_rate / self.search_rate_max
        f = food_density / (food_density + half_saturation_food_density)
        return f, feeding_rate


    def food_mass_to_flux(self, food_mass):
        food_density = food_mass / self.environment.volume()
        f, feeding_rate = self.functional_response(food_density)
        volume = self.volume()
        return f * feeding_rate * volume ** (2 / 3)
                  

    @process_function
    def feed_assimilate_digest(self):
        """
        Food flux from the environment determines the outflow of food from
        the environment. It is determined by the size of the individual,
        the specific feeding rate and the functional response curve
        J_X [mg s-1]
        """
        if self.pools[Eggbuffer].mass > 0:
            self.assimilate_from_egg()
            return

        pools, fluxes = self.process_multiple_pools(self.food_mass_to_flux, Food)
        food_flux = np.sum(fluxes)
        
        assimilation_flux = food_flux * self.assimilation_yield
        excretion_flux = food_flux * (1 - self.assimilation_yield)

        for p, f in zip(pools, fluxes):
            self.flux(f, pool_in=Guts, pool_out=p)
        self.flux(assimilation_flux, pool_in=Assimilates, pool_out=Guts)
        self.flux(excretion_flux, pool_in=Outlet, pool_out=Guts)

    @process_function
    def somatic_maintenance(self):
        """
        In this model everything is always maintained even at high age. I doubt
        that this is a realistic assumption
        
        Interesting note: repair only contributes to low amounts 
        to maintenance if hazard is directly proportional
        to mass_damage / mass
        """
        volume = self.volume()
        maintenance = self.maintenance_rate_max * volume
        self.flux(maintenance, pool_in=Maintenance, pool_out=Assimilates)
        self.flux(maintenance, pool_out=Maintenance, pool_in=Outlet)

    @process_function
    def distribute_assimilates(self):
        """
        Equation 2.8 and Equation 2.2: Mass of Dpahnia structure is initialized
        as Wv(0) = 0 and is increased by the flux of assimilates channeled to
        structure
        # TODO: Now this is not a problem, but it is not a good form that 
        # some fluxes are calculated based on previous fluxes. This could 
        # lead to differences if the methods are not calculated in the correct
        # order, which is bad because in theory everything should happen at the
        # same time. Right now it is no problem, but keep an eye out for it
        # A solution could be to find a way to analyze the function if pools 
        # are accessed in the right order (no filling after values were retrieved)
        """
        J_A = self.pools[Assimilates].balance(direction="influx")
        J_M = self.pools[Maintenance].balance(direction="influx")
        J_D = J_M - J_A # can be negative 
        k = self.distribution

        # consider this as the maximum possible mass flux from the reprobuffer
        # given its current mass and the respective timestep
        W_R = self.pools[Reprobuffer].mass / CLOCK.dt_to_seconds()

        if 0 < J_D < W_R or k * J_A < J_M < J_A:
            growth_flux = 0
            dissipation_flux = 0
            reproduction_flux = J_A - J_M # neg

        elif W_R <= J_D:
            growth_flux = (J_A + W_R - J_M)  # neg
            dissipation_flux = - growth_flux * (1 / self.structure_yield - 1) 
            reproduction_flux = - W_R
        
        else:
            growth_flux = (k * J_A - J_M)
            dissipation_flux = (1 - self.growth_yield) * (k * J_A - J_M)
            reproduction_flux = (1 - k) * J_A
            assert growth_flux > 0
            assert reproduction_flux > 0

        assert dissipation_flux >= 0

        self.flux(growth_flux, pool_in=Body, pool_out=Assimilates)
        self.flux(dissipation_flux, pool_in=Outlet, pool_out=Body)
        self.flux(reproduction_flux, pool_in=Reprobuffer, pool_out=Assimilates)
        if self.pools[Body].mass <= self.mass_puberty_threshold:
            self.flux(reproduction_flux, pool_in=Outlet, pool_out=Reprobuffer) 
  
    def spawn_trigger(self):
        pass
    
    @internal_event
    def reproduce(self):
        """
        #FIXME: step 3
        Equation 2.10. See that the // operator returns the floor of the division
        """
        self.pools[ReproClock].time = 0 # reset time

        # Trigger for spawning
            # EQ: 2.10
        W_R = self.pools[Reprobuffer]
        clutch_size = int(np.floor_divide(
            np.max([0, self.egg_yield * W_R.mass]),
            self.egg_dry_mass
        ))
        reprobuffer_flux = clutch_size * self.egg_dry_mass 
        dissipation_flux = reprobuffer_flux * (1 / self.egg_yield - 1)
        self.flux(reprobuffer_flux, pool_out=Reprobuffer, pool_in=Eggclutch)
        self.flux(dissipation_flux, pool_out=Reprobuffer, pool_in=Outlet)

    @internal_event
    def give_birth(self):
        """
        Surviving birth is assumed to be a probabilistic process. This is 
        motivated by the fact that sometimes unhatched eggs are observed in 
        daphnia individuals. So this process can easily be randomized. Also doing 
        it at this section, the energy is still spent by the mother, which is 
        desirable.
        Also this matches the observations of the experiments because here 
        eggs are not counted

        by default birth_sucess = 1, which is the same as 100% success
        with this giving birth becomes deterministic.
        This ends up being a binomial survival trial for each birth
        with n being the number of eggs and p the probability of survival

        """
        clutch = self.pools[Eggclutch]
        clutch_size = int(clutch.balance() / self.egg_dry_mass)
        # TODO: calculate repair rate for organism at birth
        X0={
            "Body":{"mass":0}, 
            "Repair": self.X0["Repair"]
        }

        LOGGER.log("info", f"{self} is spawning a clutch of {clutch_size} eggs.")
        for _ in range(clutch_size):
            if self.birth_success > np.random.rand():
                ind = type(self)(
                    # Daphnia keywords
                    rate_uptake_esfenvalerate=self.rates[Esfenvalerate]["uptake"],
                    rate_elimination_esfenvalerate=self.rates[Esfenvalerate]["elimination"],

                    # Invertebrata keywords
                    distribution=self.distribution,
                    search_rate_max=self.search_rate_max,
                    assimilation_rate_max=self.assimilation_rate_max,
                    maintenance_rate_max=self.maintenance_rate_max,
                    mass_puberty_threshold=self.mass_puberty_threshold,
                    spawning_interval=self.spawning_interval,
                    egg_dry_mass=self.egg_dry_mass,
                    birth_success=self.birth_success,
                    mother=self.id,
                    # this would draw life expectancy based on the mothers LE
                    # this ensures all D reach the same age as their mothers (fewer assumptions)
                    # Organism keywords
                    rate_repair_decay=self.rate_repair_decay,
                    rate_damage_baseline=self.rate_damage_baseline,
                    
                    # Common keywords
                    environment=self.environment,
                    structure_params=self.structure_params,
                    X0=X0
                )
                self.flux(self.egg_dry_mass, pool_in=ind.pools[Eggbuffer], 
                          pool_out=clutch)
                # make initial mass transfer in new Organism doesn't really
                # play a role, but makes the mass balance correct
                # TODO: treat mass of the eggcell as a parameter
                ind.start_ontogenesis()
            else:
                LOGGER.log("info", "One egg was not viable and died.")
                self.flux(self.egg_dry_mass, pool_in=Outlet, pool_out=clutch)

    @internal_event
    def start_ontogenesis(self):
        self.flux(1e-100, pool_in=Body, pool_out=Eggbuffer)

    def death_triggers(self):
        super().death_triggers()
        self.flux_food = 0
        self.environment.graveyard.update({self.id: self.cause_of_death})

    def length(self):
        """Converts the body volume to length along the longest axis"""
        volume = self.volume()
        return volume ** (1 / 3) / self.shape_correction_factor

    def is_embryo(self):
        return self.pools[Eggbuffer].mass > 0

    def is_juvenile(self):
        return (self.pools[Body].mass <= self.mass_puberty_threshold and
                self.pools[Eggbuffer].mass == 0)

    def is_adult(self):
        return (self.pools[Body].mass > self.mass_puberty_threshold and
                self.pools[Eggbuffer].mass == 0)

class Daphnia(Invertebrata):
    _ids = count(0)

    def __init__(
        self, 
        rate_uptake_esfenvalerate=0, 
        rate_elimination_esfenvalerate=0,
        **kwargs
        ):  
        super().__init__(**kwargs)
        # TODO: bring calculate_rate to the ODEs of uptake and elimination
        #       in base.py by multiplying with self.dt there
        self.rates[Esfenvalerate] = {
            "uptake": rate_uptake_esfenvalerate,
            "elimination": rate_elimination_esfenvalerate
        }

    def spawn_trigger(self):
        """
        For Daphnia reproduction takes place roughly every two days. This may
        be different in other species.

        Reproclock is designed so that it is incremented each time no
        reproduction takes place. Only as soon as the organism is adult
        Reproclock is reset and the Buffer begins filling and on the next
        completed spawning interval cycle offspring is spawned.
        """
        spawning_time = self.pools[ReproClock].time > self.spawning_interval
        return spawning_time and self.is_adult()

    def death_triggers(self):
        """
        extends class method of invertebrate
        """
        super().death_triggers()
        # TODO: neos die themselves, because they are in brooding pouch.
        self.environment.agents = [a for a in self.environment.agents if not (
            a.mother == self.id and a.stage == "embryo")]
