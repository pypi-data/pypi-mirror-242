# created by Florian Schunck on 30.07.2020
# Project: timepath
# Short description of the feature:
# Simulation method and class

import os
import xarray as xr
import time
import numpy as np
import shutil
import pandas as pd
import warnings
from numpy.random import MT19937, RandomState, SeedSequence
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
from tqdm import tqdm
from itertools import count

from ibes.objects.housekeeping import CLOCK, BALANCE, SCHEDULE, LOGGER
from ibes.sim.experiment import Experiment, Observation
from ibes.objects import environments, organisms, pools, base
from ibes.utils.errors import errormsg
from ibes.utils.misc import check_time, save_dict_json

class Simulation:
    _n = count()
    def __init__(
        self, 
        simtime={"start":{"hours":0}, "stop":{"hours":1}, "step": {"seconds":1}}, 
        output="data/simulation/", 
        fixdir=False,
        environment_type=environments.World,
        agent_type=organisms.Organism,
        experiment_type=Experiment,
        observation_type=Observation,
        balance_type="Mass",
        posterior=None,
        package=None,
        plot_type="plot_life_history",
        display_plots=True,
        progressbar=True,
        fail_silently=False,
        timeout=np.inf,
        logging="DEBUG",
        logfile=False,
        seed=None
    ):
        # primary parameters of experiment setting
        CLOCK.set_stop(check_time(simtime["stop"]))
        CLOCK.set_time(check_time(simtime["start"]))
        CLOCK.dt_target = check_time(simtime["step"])
        CLOCK.set_timeout(timeout)
        
        # attributes of the simulation
        self.environment_type = environment_type
        self.agent_type = agent_type
        self.experiment_type = experiment_type
        self.observation_type = observation_type

        if not isinstance(balance_type, pools.Pool):
            try:
                balance_type = getattr(pools, balance_type)
            except:
                balance_type = getattr(pools, balance_type.title()+"Pool")
        
        self.balance_type = balance_type
        self.error_tol = 1e-15

        # simulated objects
        self.environment = None
        self.experiment = None

        # prepare posterior information for parameter input. Posterior here is
        # the posterior from a previous simulation that is used as prior input
        # for the current simulation, if posterior is not set (None, "").
        # still parameters have to be actively updated from the posterior, 
        # this is not done by default. For this use update_parameters()
        if posterior is not None and posterior != "":
            self.posterior = xr.load_dataarray(posterior)

        # other
        # TODO: remove package loading. This makes everything way more complicated
        # TODO: remove plotter. Also this is unnecessary
        # if package is not None:
        #     self.package = import_package(package_path=package)
        #     self.plotter = getattr(
        #         self.package.plot, plot_type, plot_nothing)

        self.sim_id = next(self._n)
        self.directory = self.generate_dirname(output, fixdir)
        self.progressbar = progressbar


        self.display_plots = display_plots
        self.fail_silently = fail_silently
        self.seed = seed
        self.create_directory()
        if logfile:
            LOGGER.setup(
                name=self.sim_id, 
                logfile=os.path.join(self.directory, "log.txt"),
                level=logging
            )
        LOGGER.log("info", f"Initialized simulation {self.sim_id}")
        self.error = None

    def create_environment(self, X0={}, structures={}, parameters={}):
        if not isinstance(self.environment_type, type):
            env_class = getattr(environments, self.environment_type)
        else:
            env_class = self.environment_type

        self.environment = env_class(
            X0 = X0,
            structure_params=structures,
            **parameters
        )

    def populate_environment(self, N=1, X0={}, structures={}, parameters={}):
        if not isinstance(self.agent_type, type):
            agent_class = getattr(organisms, self.agent_type)
        else:
            agent_class = self.agent_type
            
        for i in range(N):
            a = agent_class(
                environment=self.environment, 
                X0 = X0,
                structure_params=structures, 
                **parameters
            )

    @staticmethod
    def parse_events(eventfile):
            
        events = pd.read_csv(eventfile)

        timecols = []

        try:
            events = events.astype({"date": str})
            timecols.append("date")
        except KeyError:
            pass
        
        try:
            events = events.astype({"time": str})
            timecols.append("time")
        except KeyError:
            pass

        time = events[timecols[0]]

        for col in timecols[1:]:
            time = time + events[col]


        try:
            parsed_datetime = pd.to_datetime(time, format="%d.%m.%Y %H:%M:%S")
            datetime_error = False
        except ValueError:
            datetime_error = True
            datetime_msg = """
                For timestamp, e.g.: 01.01.2001 13:05:42
                https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html
                """

        try:
            parsed_timedelta = pd.to_timedelta(time)
            timedelta_error = False
        except ValueError:
            timedelta_error = True
            delta_msg = """
                For timedelta, e.g.: 0 days 
                https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_timedelta.html
                """

        if datetime_error and timedelta_error:
            raise ValueError(errormsg(
                """
                could not parse time column from experiment .csv file. Please
                provide an appropriate time format."""+
                datetime_msg +
                delta_msg
            ))

        if not datetime_error and not timedelta_error:
            raise ValueError(errormsg(
                """please provide an unambiguos time format in experiment 
                .csv file"""
            ))

        if not timedelta_error and datetime_error:
            parsed_time = parsed_timedelta

        if not datetime_error and timedelta_error:
            parsed_time = parsed_datetime


        events["time"] = parsed_time
        events = events.set_index("time", drop=False).drop(columns=timecols)
        events = events.sort_index()

        return events

    def setup_experiment(self, eventfile=None, actions=[], observations=[], 
        observation_interval="table"):

        if eventfile is None:
            return
            
        elif isinstance(eventfile, str):
            events = self.parse_events(eventfile)

        elif not isinstance(eventfile, pd.DataFrame):
            raise TypeError("events must be a filename or a pandas Dataframe.")

        self.experiment = self.experiment_type(
            environment=self.environment,
            observation_type=self.observation_type,
            events_df=events, 
            actions=actions, 
            observations=observations, 
            observation_interval=observation_interval
        )


    def run(self):
        """
        execute simulation. For a number of timesteps. The length of timesteps (dt)
        should only be specified during initialization of the simulation
        object, because rate parameters are computed according to dt

        runtime:    Range from 0 to n, specifies the number of time steps the 
                    simulation should be computed
        track_pool: the global variable BALANCE tracks all fluxes and states 
                    accross various pools. By default mass flows can be tracked,
                    but also other Pools like Time, Rate, ... can be tracked
                    although these cannot be treatet as Fluxes in the
                    conventional sense they may be interesting for debugging
                    Use any class from pools.py module as an argument
        """
        # set random seed
        rs = RandomState(MT19937(SeedSequence(self.seed)))
        LOGGER.log("info", f"set random state for simulation {rs} (seed: {self.seed})")
        LOGGER.log("info", f"started simulation. Target timestep: {CLOCK.dt_target}"+
            f" until {CLOCK.stop}")

        try:
            # reduce dt if the first event is earlier then t0 + dt
            CLOCK.adapt_dt(SCHEDULE)
        
            # execute initial events before starting runtime
            # SCHEDULE.execute(CLOCK.time)

            with tqdm(
                total=CLOCK.estimate_steps(SCHEDULE.events), 
                colour="#007AFB",
                ncols=80,
                leave=False,
                disable=not self.progressbar
            ) as pbar:

                while CLOCK.time <= CLOCK.stop:
                    if SCHEDULE.upcoming_event(CLOCK.time):
                        SCHEDULE.execute(CLOCK.time) 
                        BALANCE.sum_flux()
                        if self.step_test(n=0, error_tol=1e-13):
                            self.step_test(0)
                            raise ValueError()
                        BALANCE.update_pools()
                    
                    if CLOCK.dt > timedelta(0):
                        self.step()
                        if pbar is not None:
                            if CLOCK.time >= CLOCK.elapsed + CLOCK.dt_target:
                                CLOCK.elapsed += CLOCK.dt_target
                                pbar.update(1)
                    
                    # clock ticks ahead at the end of the loop and during the
                    # next iteration processes in this timestep are carried
                    # out and the recorded state corresponds to the end of 
                    # the timestep
                    CLOCK.adapt_dt(SCHEDULE)
                    CLOCK.tick() 
                    CLOCK.test_timeout()

            self.assert_mass_conservation_final()

        # catch error or raise exception
        except Exception as error:
            self.error = error

            if self.fail_silently:
                warnings.warn("Error in simulation occurred.")
                LOGGER.errors += 1
            else:
                raise error


    def step(self):
        SCHEDULE.freeze_events()
        self.calc_step()
        BALANCE.sum_flux()
        n = 0
        while self.step_test(n):
            SCHEDULE.reset_events()
            BALANCE.reset_flux()
            self.calc_step()
            BALANCE.sum_flux()
            n += 1

        BALANCE.reset_errors()
        BALANCE.update_pools()


    def calc_step(self):
        for agent in self.environment.agents:
            # factor 2 time increase
            agent.step()
            # factor 1.5 time increases
            agent.internal_events()

        self.environment.step()
        self.environment.internal_events()


    def step_test(self, n, error_tol=None):
        """
        tests return false if no error was raised
        """
        mass_ids = BALANCE.get_dim_index(dim=pools.MassPool)
        if error_tol is None:
            error_tol = self.error_tol
    
        test1 = BALANCE.test_conservation_of_mass(
            mass_ids=mass_ids, error_tol=error_tol)
        test2 = BALANCE.test_negative_mass(
            mass_ids=mass_ids, error_tol=error_tol, n=n)
        test3 = BALANCE.test_nans()

        return test1 or test2 or test3

    def wrap_up(self):
        self.environment.agents.extend(self.environment.__dict__.pop("dead_agents"))

    @staticmethod
    def generate_dirname(directory, fixdir):
        if fixdir:
            return os.path.normpath(os.path.abspath(directory))
        # assert directory[-1] == "/", ValueError("loc must end with '/'")
        t = datetime.now().strftime("%Y%m%d_%H%M%S")

        while os.path.exists(os.path.join(directory, t)):
            UserWarning("directory exists. Waiting a second")
            time.sleep(1)
            t = datetime.now().strftime("%Y%m%d_%H%M%S")

        return os.path.normpath(os.path.abspath(os.path.join(directory, t)))


    def dump(self, config):
        """ 
        stores results, balances, eventfile and config file to a folder
        and makes the folder self contained.
        """
        if isinstance(self.error, Exception):
            self.directory = os.path.join(self.directory, "errors")
            self.directory = self.generate_dirname(self.directory, fixdir=False)
            self.create_directory()
            LOGGER.logger.error(
                self.error, exc_info=True, extra={"simtime": CLOCK.time})
            LOGGER.stop()
            shutil.copy(LOGGER.logfile, os.path.join(self.directory, "log.txt"))

        new_loc_events = os.path.join(self.directory, "events.csv")
        shutil.copyfile(config["experiment"]["eventfile"], new_loc_events)

        # update paths in config file
        config["simulation"]["output"] = self.directory
        config["experiment"]["eventfile"] = new_loc_events
        save_dict_json(config, os.path.join(self.directory, "config.json"))
        
        self.store_observations_csv()
        try:
            self.store_balance()
        except ValueError:
            # catch a weird error
            pass




    def store_sim_results(self, store_keys=[]):
        """
        stores the output of each id in one csv file. This will be much better to
        handle for long and highly populated simulations with thousands of ids
        Storing data takes a long time and could be shortened if only every nth
        observation is taken
        TODO: only store every nth row of the df
        TODO: make zfill as long as there are data
        """

        for i, a in enumerate(self.environment.agents):
            data = pd.DataFrame.from_dict(a.history)
            data["id"] = i
            for k in store_keys:
                data[k] = getattr(a, k)
            f = os.path.join(self.directory, "simulation_" + str(i).zfill(5) + ".csv")
            data.to_csv(f, index=False)

        LOGGER.log("info", f"saved simulation results to {f}")

    def create_directory(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def store_observations_csv(self):
        history = self.experiment.get_obs_df()
        history.to_csv(self.directory + '/observations.csv')

    def store_balance(self, dim=pools.MassPool):
        typebal = dim.__name__
        BALANCE.state_to_df(dim).to_csv(self.directory + f"/{typebal}_state_balance.csv")
        BALANCE.fluxes_to_df(dim).to_csv(self.directory + f"/{typebal}_flux_balance.csv")
        LOGGER.log("info", f"Balances processed to {self.directory}")

    def plot_observations(self, store=True):     
        history = self.experiment.get_obs_df()
        fig = history.plot(subplots=True, figsize=(8,12))
        if store:
            plt.savefig(self.directory + "/observations.png")
            LOGGER.log("info", f"saved plot in {self.directory}/observations.png")

        if self.display_plots:
            plt.show()

        return fig
        
    def assert_mass_conservation_final(self, tolerance=1e-13):
        flux_mass = BALANCE.fluxes_to_df(dim=pools.MassPool)["∑"].sum()
        if abs(flux_mass) >= 1e-13:
            raise ValueError(errormsg(
                f"""Balance of fluxes did not sum to zero. 
                Instead sum fluxes = {flux_mass} Mass was not conserved."""
            ))

    def end(self):
        """delete sim directory if it is still empty"""
        logfile = LOGGER.logfile
        LOGGER.stop()
        if logfile is not None:
            if os.stat(logfile).st_size == 0:
                os.remove(logfile)

        if len(os.listdir(self.directory)) == 0:
            os.rmdir(self.directory)

 

def check_config(config):
    try: 
        config["simulation"]
    except KeyError:
        LOGGER.log("warning", errormsg("""
            no SIMULATION configuration found. Using defaults. Make sure you
            have spelled everything correctly in the config files and set the
            attributes as desired. Otherwise the simulation may not run as 
            expected            
            """))
        config["simulation"] = {}

    try: 
        config["environment"]
    except KeyError:
        LOGGER.log("warning", errormsg("""
            no ENVIRONMENT configuration found. Using defaults. Make sure you
            have spelled everything correctly in the config files and set the
            attributes as desired. Otherwise the simulation may not run as 
            expected            
            """))
        config["environment"] = {}

    try: 
        config["agents"]
    except KeyError:
        LOGGER.log("warning", errormsg("""
            no ENVIRONMENT configuration found. Using defaults. Make sure you
            have spelled everything correctly in the config files and set the
            attributes as desired. Otherwise the simulation may not run as 
            expected            
            """))
        config["agents"] = {}

    try: 
        config["experiment"]
    except KeyError:
        LOGGER.log("warning", errormsg("""
            no ENVIRONMENT configuration found. Using defaults. Make sure you
            have spelled everything correctly in the config files and set the
            attributes as desired. Otherwise the simulation may not run as 
            expected            
            """))
        config["experiment"] = {}

    return config

def reset_counters(cls):
    cls._ids = count(0)
    subclasses = cls.__subclasses__()
    while len(subclasses) > 0:
        subcls = subclasses.pop()
        reset_counters(cls=subcls)

def prepare_sim(config={}):
    config = check_config(config)

    reset_counters(base.Common)
    # Balance must be reset here so that pools created in the next step will be 
    # logged
    BALANCE.reset() 
    CLOCK.reset()
    SCHEDULE.reset()
    LOGGER.reset()

    return config

def setup_sim(config={}):
    config = prepare_sim(config)
    return Simulation(**config["simulation"])

def create_sim(config={}):
    s = setup_sim(config=config)

    # create environment
    s.create_environment(**config["environment"])

    # create agents in environment
    s.populate_environment(**config["agents"])
    

    s.setup_experiment(**config["experiment"])

    return s

def plot_nothing(sim):
    return