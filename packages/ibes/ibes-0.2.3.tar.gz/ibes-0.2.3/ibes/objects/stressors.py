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
from scipy import constants
from itertools import count
import numpy as np

from ibes.objects.pools import Pool, DissolvedPool
from ibes.objects.structures import Structure, VGSodiumChannels, Skin, DNA

class Stressor(Pool):
    """
    the stressor class is constructed to build a generic stressor-object for 
    instance 'Esfenvalerate'. The concept is envisioned to interact in different
    environments with different targets. Environments are the outer environment
    where the stressor is applied (in this module it is going to be the world
    instance), or the body of an animal living in the world.
    """
    _stressor = True
    _ids = count(0)

    def __init__(
        self,
        name=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.name = name
    

class Chemical(Stressor, DissolvedPool):
    _ids = count(0)

    def __init__(
        self, 
        molar_mass,
        log_kow,
        dt50_water,
        solubility_water,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.molar_mass = molar_mass
        self.log_kow = log_kow
        self.dt50_water = dt50_water
        self.solubility_water = solubility_water
        self.action_sites = []

    def mol(self):
        # convert from g/mol to mg/mol because all units are in mg
        return self.mass / self.molar_mass / 1000

    def N(self):
        return self.mol() * constants.Avogadro

    def number_concentration(self):
        return self.N / self.environment.volume()

class Pyrethroid(Chemical):
    _ids = count(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action_sites = []

    def block_sodium_channels(self):
        """
        it is well known that Pyrethroids affects voltage gated sodium channels 
        in the peripheral nervous system, prolonging the time during which the
        channels are open.
        """
        pass

class Effect:
    def __init__(self, action, target, args=()):
        self.action = action
        self.target = target
        self.args = args
        self.effect = None

    def __call__(self):
        act = self.action
        self.effect = act(self.target, *self.args)

class Esfenvalerate(Pyrethroid):
    _ids = count(0)

    """
    It is possible to add interaction hooks with super classes 
    e.g. if isinstance(pool.environment, Invertebrata), will test
    if the environment where the pool is located is an invertebrate.
    Then this and that action can be carried out.
    """
    def __init__(
        self, 
        molar_mass=419.9, 
        log_kow=6.2,
        dt50_water=691200,
        solubility_water=0.002,
        **kwargs
        ):
        super().__init__(
            molar_mass=molar_mass,
            log_kow=log_kow,
            dt50_water=dt50_water,
            solubility_water=solubility_water, 
            **kwargs
            )
        self.action_sites = [VGSodiumChannels]

    def __call__(self, site: Structure):
        """
        implement effects on site. They are then executed, whenever the 
        respective site is called (i.e. sprung into action). This implementation
        follows the reason that there is never a direct effect. Only indirect
        effects resulting from a loss of function. A cut in the vessel system
        leads to a failure to transport blood to where it needs to go. A blockage
        of Nerves leads to loss of communication.
        """
        if isinstance(site, VGSodiumChannels):
            effect = Effect(self.block_sodium_channels, target=site)
            site.effects.update({self: effect})

    def block_sodium_channels(self, channel: VGSodiumChannels):
        """
        Esfenvalerate as a Type II pyrethroid produces stimulus-dependent nerve
        depolarization and blockage (Soderlund & Bloomquist, 1989)

        It would be nice to know, how the exact process of occupation
        of sodium channels works and how many sodium channels in a Daphnia
        exist
        """
        C_i = self.N() # internal concentration of active substance
        C_t = channel.N() # target site concentration
        return np.min([C_i / C_t, 1])

class Radiation(Stressor):
    _ids = count(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action_sites = [Skin, DNA]

    def __call__(self, site: Structure):
        if isinstance(site, Skin):
            self.burn_skin(site)

        if isinstance(site, DNA):
            self.damage_DNA(site)

    def burn_skin(self, site: Skin):
        # inflicts damage 
        pass

    def damage_DNA(self, site: DNA):
        # inflict damage that needs repair
        # induce long term damage
        pass

    @staticmethod
    def expose(energy_flux, t):
        return energy_flux * t
