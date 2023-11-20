import pandas as pd
import numpy as np
import xarray as xr
import datetime as dt
import re
from collections import Counter
from ibes.utils.math_helpers import take_mean
from ibes.utils.errors import errormsg
from ibes.utils.misc import check_time
from ibes.objects.base import Common, external_environmental_event
from ibes.objects.stressors import Esfenvalerate
from ibes.objects.pools import Food, IO, POM, DOM
from ibes.objects.organisms import Repair, Damage, Body, Maintenance, Outlet, Reprobuffer
from ibes.objects.organisms import NervousSystem
from ibes.objects.housekeeping import Event, CLOCK, BALANCE, SCHEDULE, LOGGER

EMPTY_EXPERIMENT = pd.DataFrame(index=pd.to_timedelta([]))

class Experiment(Common):
    """
    This class implements discrete, instantaneous events in an otherwise 
    continuous simulation.
    """

    def __init__(
        self, 
        environment, 
        observation_type,
        events_df=EMPTY_EXPERIMENT, 
        actions=[],
        observations=[], 
        observation_interval="table",
        **kwargs
    ):  
        super().__init__(**kwargs)
        self.observation_type = observation_type
        assert isinstance(events_df.index, (pd.DatetimeIndex, pd.TimedeltaIndex))

        try:
            self.events = events_df.loc[:,actions] # only use needed columns
        except KeyError:
            missing_actions = [a for a in actions if a not in events_df.columns]
            raise KeyError(
                f"{missing_actions} were not found in the event table. " +
                "Make sure to include a column in scenarios/events.csv which " +
                "sets the parameters for the action."
            )
        
        self.env = environment
        # this constructs a list without duplicate entries
        self.obs = list(dict.fromkeys(["time"]+observations))
        self.observations = {
            "labels": self.obs,
            "values": []
        }
        self.current_time = None
        self.pools.update({IO: IO(environment=self)})
        
        # finalize events
        self.set_observation_interval(observation_interval)

        # set times from events
        try:
            CLOCK.set_time(self.events.index[0])
            CLOCK.set_stop(self.events.index[-1])
        except IndexError:
            # ignore in case an empty experiment is passed -  this will use the
            # times specified in the config i.e. initialization of Simulation
            pass
        
        # schedule events
        self.schedule_experiment()

    def vary_treatments(self, changes=[]):
        """
        supply a list of changes wich will modify the events data frame
        example: changes = [((time, column), value), ]

        the event dataframe is always built with: 
        - columns denominating actions
        - rows denominating time and 
        - value denominating the parameter supplied to the action

        each item of this list can be used as a index - value combination
        """
        for index, value in changes:
            self.events.loc[index] = value


    def __repr__(self):
        return type(self).__name__

    def schedule_experiment(self):
        for column, series in self.events.items():
            assert column in dir(self), errormsg(
                """
                action specified in config file was not found in Experiment
                methods. Make sure you have spelled it correctly or if
                needed specify your own method.
                """
            )
            for index, value in series.iteritems():
                assert isinstance(value, (float, int))

                # don't schedule an event if the value in the dataframe is 0 
                # or empty. Maybe this is bad (because sometimes null)
                # values serve a purpose (such as set x to zero, but I think
                # in this case it should be coded differently)
                if np.isnan(value):
                    continue

                e = Event(
                    time=index, 
                    instance=self, 
                    method=column, 
                    arguments=(value,)
                )
                SCHEDULE.add(e)

    def reindex_actions(self, interval):
        oi = check_time(interval)
        start = self.events.index.min()
        end = self.events.index.max()
        periods = (end - start) / oi + 1

        if isinstance(start, pd.Timedelta):
            return self.events.reindex(pd.timedelta_range(
                start=start,
                end=end,
                periods=int(periods)))
        
        if isinstance(start, pd.Timestamp):
            return self.events.reindex(pd.date_range(
                start=start,
                end=end,
                periods=int(periods)))


    def set_observation_interval(self, observation_interval):
        observation_interval = observation_interval.replace(" ", "").split("+")
        experimentobs = False
        for oi in observation_interval:
            regular_interval = re.match("^[0-9]+", oi)
            if regular_interval is not None:
                interval = oi[slice(*regular_interval.regs[0])]
                unit = [i for i in oi.split(interval) if len(i) > 0][0]
                regular = {unit: int(interval)}
                new_events = self.reindex_actions(regular)
                new_events["observation_new"] = 1
                new_events = self.events.merge(
                    new_events["observation_new"], 
                    how="outer", 
                    left_index=True, 
                    right_index=True
                )

            if "table" in oi or "experimentfile" in oi:
                experimentobs = True
        
        if regular_interval is None:
            # only record observations indicated in the experiment csv file
            # this is the default case and will also work if neither table
            # nor a frequency descriptor is in the observation_interval option
            return
        
        else:
            if experimentobs:
                # record observations at each time specified in the experiment
                # tabel and at regular intervals
                new_events["observation"] = np.logical_or(
                    new_events["observation"], 
                    new_events["observation_new"]
                ).astype(int)

            else:
                # ignore indicated observations in experiment file and only
                # record regular interval
                new_events["observation"] = new_events["observation_new"]

            new_events = new_events.drop(columns="observation_new")
            self.events = new_events
    
    @external_environmental_event
    def spike_esfenvalerate(self, param):
        if param == 0:
            pass
        elif param > 0:
            efv = self.env.get_or_create_pool(Esfenvalerate)
            self.flux(param, pool_in=efv, pool_out=IO)
            LOGGER.log("INFO", f"spiked {param}mg Esfenvalerate")

    @external_environmental_event
    def filter_neos(self, param):
        if param == 0:
            pass
        elif param == 1:
            # tag all agents which are not embryos or the original with inside_environment=False
            remaining_agents = [a for a in self.env.agents 
                if a.is_embryo() or a.name == "Testorganism"]

            # complement
            filtered_agents = [
                a for a in self.env.agents if a not in remaining_agents]

            self.env.agents = remaining_agents
            self.env.filtered_agents = filtered_agents

            if not hasattr(self.env, "filtered_notrecorded_agents"):
                self.env.filtered_notrecorded_agents = []

            self.env.filtered_agents.extend(
                self.env.filtered_notrecorded_agents)
            self.env.filtered_notrecorded_agents = []  # empty net

    @external_environmental_event
    def medium_change(self, param):
        if param == 0:
            pass
        elif param == 1:
            food = self.env.pools[Food]
            pom = self.env.pools[POM]
            dom = self.env.pools[DOM]
            self.flux(food.mass, pool_out=food, pool_in=IO)
            self.flux(pom.mass, pool_out=pom, pool_in=IO)
            self.flux(dom.mass, pool_out=dom, pool_in=IO)
            try:
                efv = self.env.pools[Esfenvalerate]
                self.flux(efv.mass, pool_out=efv, pool_in=IO)
                    
            except KeyError:
                pass
            # TODO: Future: have the pools food and Esfenvalerate and everything
            #       else in the pool Water. If water is replaced everything else
            #       is then fixed automatically

    @external_environmental_event
    def feed_mg_carbon(self, param):
        if param == 0:
            pass
        elif param > 0:
            self.flux(param, pool_in=self.env.pools[Food], pool_out=IO)


    def observation(self, param):
        if param == 0:
            pass
        elif param == 1:
            ob = self.observation_type(self.env, CLOCK.time, self.obs)
            ob.observe()
            self.observations["values"].append(ob.values)

    def get_obs_df(self):
        df = pd.DataFrame(
            data=self.observations["values"],
            columns=self.observations["labels"])

        df = df.set_index("time")

        return df

    def get_tensor(self, return_time=False, return_xarray=False):
        """
        return a tensor of observations with
        1st axis = time specify format: e.g. "timedelta64[h]"

        2nd axis = id (always length 1)
        3rd axis = values
        """
            

        time_fmt = self.events.index.values.dtype
        labels = self.observations["labels"]
        index_time = [i for i, l in enumerate(labels) if l == "time"]
        index_data = [i for i, l in enumerate(labels) if l != "time"]

        time = []
        data = []
        for obs in self.observations["values"]:
            time.append([obs[i] for i in index_time])
            data.append([obs[i] for i in index_data])

        
        data = np.array(data)
        time = np.array(time).astype(time_fmt)

        if return_xarray:
            if len(time) == 0:
                return xr.Dataset()
            xdata = xr.DataArray(
                data, 
                coords={
                    "time":time[:, 0], 
                    "labels": np.array(labels)[index_data]
                },
                name="simobs"
            ).to_dataset(dim="labels")
            return xdata

        if return_time:
            data = np.column_stack((time.astype(float), data))

        data = data.reshape((time.shape[0], 1, data.shape[1]))

        return data

class Observation:
    def __init__(self, env, time, obs=["time"]):
        self.env = env
        self.current_time = time
        self.values = []
        self.observations = obs
        
    def observe(self):
        for obs in self.observations:
            try:
                make_observation = getattr(self, obs)
            except AttributeError:
                raise AttributeError(errormsg(
                    """
                    You are trying to observe some variable or aggregate for
                    which no observation method exists yet. Luckily it is very
                    easy to design a new observation. Simply add a new method to
                    the class Observation in the Module events.py in the same
                    style all other methods are designed. These methods can be
                    as simple or as complicated as you like and they have access
                    to all current values of the simulation: self.env contains
                    environmental attributes, self.env.agents contains a list of
                    all active agents in the simulation
                    """
                ))
            make_observation()

        lod = {o:v for o, v in zip(self.observations, self.values) if o != "time"}
        LOGGER.log("INFO", f"observed {lod}")
    
    def time(self):
        self.values.append(self.current_time)

    def food_density(self):
        o = self.env.pools[Food].mass / self.env.volume()
        self.values.append(o)

    def efv_external(self):
        try:
            o = self.env.pools[Esfenvalerate].concentration()
        except KeyError:
            o = np.nan
        self.values.append(o)

    # TODO: Probably i can remove the life switch soon. Once I have a good method
    #       to remove dead ids
    def n_embryos(self):
        o = [i for i in self.env.agents if i.is_embryo()]
        o = len(o)
        self.values.append(o)

    def n_juveniles(self):
        o = [i for i in self.env.agents if i.is_juvenile()]

        o = len(o)
        self.values.append(o)

    def n_adults(self):
        o = [i for i in self.env.agents if i.is_adult()]
        o = len(o)
        self.values.append(o)

    def size_adults(self):
        o = [i.length() for i in self.env.agents if i.is_adult()]
        o = take_mean(o)
        self.values.append(o)

    def size_juveniles(self):
        o = [i.length() for i in self.env.agents if i.is_juvenile()]
        o = take_mean(o)
        self.values.append(o)

    def size_embryos(self):
        o = [i.length() for i in self.env.agents if i.is_embryo()]

        o = take_mean(o)
        self.values.append(o)

    def death_starvation(self):
        o = Counter(self.env.graveyard.values())["starvation"]
        self.values.append(o)

    def death_esfenvalerate(self):
        o = Counter(self.env.graveyard.values())["Esfenvalerate"]
        self.values.append(o)

    def death_old_age(self):
        o = Counter(self.env.graveyard.values())["old_age"]
        self.values.append(o)

    # indy experiment observations
    def indy(obs_func):
        def decorated_obs_func(self):
            try:
                o = obs_func(self)
            except IndexError:
                o = np.nan
            self.values.append(o)
        return decorated_obs_func

    @indy
    def survival(self):
        return len([a for a in self.env.agents if a.name == "Testorganism"])

    @indy
    def hazard_rate(self):
        return [a.hazard() 
                for a in self.env.agents if a.name == "Testorganism"][0]

    @indy
    def max_repair_rate(self):
        return [a.pools[Repair].rate 
                for a in self.env.agents if a.name == "Testorganism"][0]
    
    @indy
    def repair(self):
        return [a.pools[Damage].balance(direction="outflux", previous_flux=True) 
                for a in self.env.agents if a.name == "Testorganism"][0]

    @indy
    def incoming_damage_rate(self):
        return [a.pools[Damage].balance(from_pools=[Body], direction="influx", previous_flux=True) 
                for a in self.env.agents if a.name == "Testorganism"][0]

    @indy
    def damage(self):
        return [a.pools[Damage].mass 
                for a in self.env.agents if a.name == "Testorganism"][0]

    # slightly changed indy method (does not use index error)
    def offspring(self):
        try:
            o = len(self.env.filtered_agents)
            self.env.filtered_agents = []  # empty net
            # delete attributes observations return zeros
        except AttributeError:
            o = np.nan
        self.values.append(o)

    @indy
    def size(self):
        return [a.length() 
                for a in self.env.agents if a.name == "Testorganism"][0]

    @indy
    def mass(self):
        return [a.pools[Body].mass 
                for a in self.env.agents if a.name == "Testorganism"][0]

    @indy
    def mass_reprobuffer(self):
        return [a.pools[Reprobuffer].mass 
                for a in self.env.agents if a.name == "Testorganism"][0]


    @indy
    def maintenance(self):
        return [a.pools[Maintenance].balance(direction="influx", previous_flux=True) 
                for a in self.env.agents if a.name == "Testorganism"][0]

    @indy
    def efv_internal(self):
        try:
            o = [a.pools[Esfenvalerate].concentration()
                 for a in self.env.agents if a.name == "Testorganism"][0]
        except KeyError:
            o = np.nan
        return o

    @indy
    def ns_disturbance(self):
        return [a.pools[NervousSystem].cascade_effects()
                for a in self.env.agents if a.name == "Testorganism"][0]

    @indy
    def nerve_damage(self):
        return [a.pools[NervousSystem].cascade_effects() * a.pools[Body].mass
                for a in self.env.agents if a.name == "Testorganism"][0]
