# structures are classes to model subsystems of organisms or isolated aspects
from itertools import count   
from functools import total_ordering
import numpy as np

from ibes.utils.errors import errormsg
from ibes.objects.base import Common
from ibes.objects.pools import Food

@total_ordering
class Structure(Common):
    _structure = True
    _ids = count(0)

    elements = []

    def __init__(
        self,
        supersystem,
        container=None,
        level=1,
        params={},
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # structures always have a functionality attribute that determines the
        # rate of all implemented functions
        self.level = level
        self.effects = {}
        self.supersystem = supersystem
        self.components = {}
        self.container = container
        self.get_and_set_params()
        if self.supersystem != self:
            self.supersystem.index.update({type(self): self})

        # create the next lower entities of the structure
        self.create_structure(supersystem, params)

    def _is_valid_operand(self, other):
        share_supersystem = type(self.supersystem) == type(other.supersystem)
        return (isinstance(self, Structure) and isinstance(other, Structure) 
                and share_supersystem)

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.level == other.level)

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.level < other.level)

    def __call__(self):
        """
        see how in principle an effect cascade can be implemented here
        the __call__ method of a standard container invoked by 
        self.container() is pass meaning that unless a __call__ method
        is explicitely defined for a structure class, the effect cascade
        stops 
        """
        for dose, action in self.effects.items():
            action()

    def create_structure(self, supersystem, params):
        for element in self.elements:
            self.components.update({
                element: element(
                    supersystem=supersystem,
                    container=self,
                    level = self.level + 1,
                    params=params
                )
            })

    def get_and_set_params(self):
        try:
            host = self.supersystem.environment
            pars = host.structure_params[type(self).__name__]
            for key, value in pars.items():
                setattr(self, key, value)

        except KeyError:
            pass


class Subsystem(Structure):
    _subsystem = True
    """implements lower level system functions that should be modelled"""
    def __init__(self, **kwargs):
        self.index = {}
        super().__init__(supersystem=self, **kwargs)
        self.effect_cascade = sorted(self.index.values(), reverse=True)
        self.influences = {}

    def __call__(self):
        """
        subsystems as a subclass of common, also have pools and all necessary
        functions to also do fluxes. So the presence of subpools is no problem
        and can be modelled. Then act and react functions don't have to be based
        on the environmental pool, but can instead be based on the pool in the
        enviroment. This would resolve the problem that I need a huge concentration
        of e.g. VGSCs to handle the toxic effect of Esfenvalerate. This number
        includes not only the actual number, but also the fact that indeed much
        less Esfenvalerate arrives at the nervous system.
        """
        self.effect_setup()
        self.react()
        self.act()

    def effect_setup(self):
        """
        effect_setup method iterates over pool that have action sites. If the
        action site is in the subsystem, pool instance is called (see changes to
        stressors.py for what happens) explicitely escalate assertion if pool is
        callable to point the user to missing interaction method for the pool
        """
        for pool_class, pool in self.environment.pools.items():
            if hasattr(pool, "action_sites"):
                assert callable(pool), errormsg(
                    f"""
                    {pool_class} is not callable but has the action sites
                    {pool.action_sites}. Make sure there is an appropriate
                    __call__ method for the pool/stressor. See Esfenvalerate
                    class in stressors.py for an example
                    """
                )
                for action_site in pool.action_sites:
                    if action_site in self.index.keys():
                        # this sets up effects in the subsystem cascade
                        pool(self.index[action_site])
    
    def cascade_effects(self):
        """
        cascade_effect method makes calls to structure_elements thus triggering
        effects. The total effect is tracked as the sum of the individual
        effects. !! There are plenty assumptions related to (concentration
        addition, independent action here) cascade_effects can be viewed as the
        impairment of the normal functioning of the subsystem function.
        Therefore it can be called anywhere in the react method of the subsystem
        (or elsewhere). It only depends on state variables and fixed parameters.
        
        To make the power of this method clear: A subsystem may carry out a
        function of an organism (gut --> assimilate) for instance. If now a
        normal act method would involve assimilation of ingested food and there
        is the assumption that the gut has an interaction with esfenvalerate
        affecting the assimilation. This could be realized very easily with the
        cascade_effects method.

        This is also a step into the direction of realizing organism functions
        in subsystems instead of the organism itself.
        """
        total_effect = 0
        for structure_element in self.effect_cascade:
            structure_element()
            # HYPOTHESIS ABOUT INTERACTIONS OF EFFECTS.
            total_effect += self.same_target_addition(structure_element.effects)
        return total_effect

    @staticmethod
    def same_target_addition(effects):
        return np.sum([response.effect for response in list(effects.values())])

    def act(self):
        """
        system actions to stimuli in the external environemnt. Under act,
        regular subsystem actions can be scheduled. (e.g. blood circulation,
        water mixing, digestion, excretion)
        """
        pass

    def react(self):
        """reactions to stimuli in internal pools"""
        pass

    def interact(self):
        """
        functions that are relevant for interactions with other Subsystems or
        higher level functions. This method should aggregate the combined 
        affects of its substructures to determine the level of "functioning"
        """
        return getattr(self, "_status")

class Protein(Structure):
    _ids = count(0)
    pass

class AminoAcids(Structure):
    _ids = count(0)
    pass

class Nucelotides(Structure):
    _ids = count(0)
    pass

class DNA(Structure):
    _ids = count(0)
    elements = [Nucelotides]

class Lipids(Structure):
    _ids = count(0)
    pass

class SodiumChannels(Protein):
    _ids = count(0)
    pass

class VGSodiumChannels(SodiumChannels):
    """Voltage Gated Sodium Channels"""
    _ids = count(0)
    # typical neuron has a surface area of 1000 µm² and 3-4 sodium channels
    # per µm². I don't know how many neurons a Daphnia has there are about
    # 900 cells in the pcdc complex. However there should be plenty of sodium
    # channels in synapses between neurons. 
    # In this number many more information are contained.
    # it is for instance unlikely that all molecules will cover the target 
    # sites, it will surely be only a fraction of it
    volumetric_channel_concentration = 0



    def N(self):
        return (self.volumetric_channel_concentration * 
                self.supersystem.environment.volume())

    def transmit(self):
        self.container.transmission = 1.0 - self.blockage # has no effect in this model
        # fast forward the signal in this case because we have no interest 
        # at this point in the effect cascade
        self.container.container.container.container.transmission = 1.0 - self.blockage

class Membrane(Structure):
    _ids = count(0)
    elements = [Lipids]

class Cell(Structure):
    _ids = count(0)
    elements = [Membrane, DNA]

class Neuron(Cell):
    _ids = count(0)
    """Nerve cells"""
    elements = [Membrane, VGSodiumChannels]

class Ganglion(Structure):
    _ids = count(0)
    """Nerve cell bundle"""
    elements = [Neuron]

class PeripheralNS(Structure):
    _ids = count(0)
    elements = [Ganglion]
    
class Skin(Structure):
    _ids = count(0)
    elements = [Cell]

