from functools import total_ordering
from itertools import count
from datetime import timedelta, datetime
from timeit import default_timer
import pandas as pd
import numpy as np
from prettytable import PrettyTable
from heapq import heappush, heappop, merge, nsmallest
from inspect import ismethod
import logging

from ibes.utils.errors import errormsg

class Clock:
    def __init__(self):
        self.dt_target = timedelta(seconds=60)
        self.dt = None
        self.rerun = False
        self.discrete_actions = 0
        self.time = timedelta(seconds=0)  # seconds
        self.stop = timedelta(seconds=86400)
        self.time_record = []
        self.step_record = []
        self.timeout = np.inf # never terminate a simulation by default

        # set timeout timer
        self.start_time = default_timer()
        self.runtime = 0
        
    def set_timeout(self, timeout):
        self.timeout = timeout
    
    def test_timeout(self):
        self.runtime = default_timer() - self.start_time
        if self.runtime > self.timeout:
            raise RuntimeError(errormsg(
                f"Interrupted simulation, because runtime was larger than {self.timeout}s."
            ))

    def reset(self):
        self.dt_target = timedelta(seconds=60)
        self.dt = None
        self.rerun = False
        self.discrete_actions = 0
        self.time = timedelta(seconds=0)  # seconds
        self.stop = timedelta(seconds=86400)
        self.elapsed = timedelta(seconds=0)
        self.time_record = []
        self.step_record = []
        self.timeout = np.inf  # never terminate a simulation by default

        # set timeout timer
        self.start_time = default_timer()
        self.runtime = 0

    def dt_to_seconds(self):
        """will return a float down to 1 microsecond accuracy"""
        return self.dt.total_seconds()

    def time_during_step(self):
        """
        returns the time in the middle of the current timestep. Important for
        scheduling internal events.
        """
        return self.time + self.dt / 2
    

    def adapt_dt(self, schedule):
        self.dt = self.dt_target
        ttne = schedule.time_to_next_event(self.time)
        if ttne < self.dt:
            self.dt = ttne
            # print("made small timestep to next event")
            
    
    def tick(self):
        assert isinstance(self.dt, (timedelta, datetime))      
        self.time += self.dt
        self.time_record.append(self.time)
        self.step_record.append(self.dt)

    def estimate_steps(self, events=[]):
        return (self.stop-self.time) / self.dt_target

    def set_time(self, time):
        assert isinstance(time, (timedelta, datetime))
        self.time = time
        self.elapsed = time

    def set_stop(self, stop):
        assert isinstance(stop, (timedelta, datetime))
        self.stop = stop

    def __repr__(self):
        return f"str(self.time)"

    def __str__(self):
        return "Clock at {} ticking with {} until {}"\
            .format(self.time, self.dt, self.stop)

    @staticmethod
    def period(delta):
        if isinstance(delta, np.timedelta64):
            delta = delta.astype("timedelta64[ms]").astype("float")
            delta = timedelta(microseconds=delta)
        """from stackoverflow by GooDeeJAY"""
        d = delta.days
        h, rem = divmod(delta.seconds, 3600)
        m, s = divmod(rem, 60)
        f = delta.microseconds
                
        return f"{d} days, time: {h:02d}:{m:02d}:{s:02d}.{f}"

@total_ordering
class Event:
    _ids = count(0)
    def __init__(self, time, instance, method, arguments=()):
        self.id = next(self._ids)
        self.time = time # when does the event occurr
        if ismethod(method):
            method = method.__name__
        self.instance = instance # who calls it (this is an object)
        self.method = method # what is the event (a method)
        assert isinstance(arguments, tuple)
        self.arguments = arguments # arguments passed to the method
        LOGGER.log("debug", f"scheduled {self}")

    def __repr__(self):
        return "Event:{}".format(self.id)

    def __str__(self):
        return "Event {0}: {1} invokes {2}{3} at {4}".format(
            self.id, self.instance, self.method, self.arguments, self.time)


    def __call__(self):
        func = getattr(self.instance, self.method)
        func(*self.arguments)

    def _is_valid_operand(self, other):
        return isinstance(other, type(self))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.time, self.id) == (other.time, other.id))

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.time, self.id) < (other.time, other.id))

class Schedule:
    """
    Schedule is generated from events and can be added to by triggers inside
    the simulation. It is helpful for the updating process to always know when the
    next scheduled event is going to take place

    Consider the schedule to be the trigger for an event.
    Basically it is a table consisting of 

    time        function        function parameters
    .           .               .
    .           .               .
    .           .               .

    it should be manage with a heap
    """
    def __eq__(self, __o: object) -> bool:
        return self.events == __o.events

    def __init__(self):
        self.events = []
        self.event_history = []

    def reset_events(self):
        errors = [fe for fe in self.frozen_events if fe not in self.events]
        if len(errors) > 0:
            raise RuntimeError(f"Events {errors} were wrongly removed")
        removed_events = [e for e in self.events if e not in self.frozen_events]
        LOGGER.log("debug", f"restoring frozen events: removing {removed_events}")
        self.events = self.frozen_events.copy()

    def freeze_events(self):
        self.frozen_events = self.events.copy()

    def reset(self):
        self.events = []
        self.event_history = []

    def add(self, event):
        assert isinstance(event, Event)
        heappush(self.events, event)
    
    def remove(self, key):
        pass                

    def time_to_next_event(self, time):
        if len(self.events) == 0:
            # largest possible time difference 
            # TODO: find a better solution
            return timedelta(days=9.999999999999999e8)
        return self.events[0].time - time

    def upcoming_event(self, time):
        return self.time_to_next_event(time) <= timedelta(seconds=0)

    def show_next_event(self):
        """
        should only be one, because heap only guarantees that heap[0]
        is the smallest element (in that case next event)
        """
        print(self.events[0])

    def show_last_events(self, n=5):
        for i in range(1, n+1):
            print(self.event_history[-i])

    def execute(self, time):
        if len(self.events) > 0:
            while self.events[0].time <= time:
                event = heappop(self.events)
                LOGGER.log("debug", str(event))
                event()
                self.event_history.append(event)
                if len(self.events) == 0:
                    LOGGER.log("debug", "no events left")
                    break

class Balance:
    def __init__(self):
        self.current_flux = None
        self.current_state = None
        self.pools = []
        self.record = []
        self.state_record = []
        self.time_record = []
        
    def __str__(self):
        return self.flux_table().get_string()

    def reset(self):
        self.current_flux = None
        self.current_state = None
        self.pools = []
        self.record = []
        self.state_record = []
        self.time_record = []

    def reset_flux(self):
        [pool.reset_flux() for pool in self.pools]

    def reset_errors(self):
        for pool in self.pools:
            pool.negative_state = False

    def get_flux(self):
        self.current_flux = np.array([p.calc_flux() for p in self.pools])

    def get_state(self):
        self.current_state = np.array([getattr(p, p._dim) for p in self.pools])

    def sum_flux(self):
        self.get_flux()
        self.get_state()     

    def update_pools(self):
        [pool.update() for pool in self.pools]
        self.record.append(self.current_flux)
        self.state_record.append(self.current_state)
        self.time_record.append(CLOCK.time)

    def test_negative_mass(self, mass_ids, error_tol, n):
        new_state = self.current_state + self.current_flux
        mass = new_state[mass_ids]

        if n <= 1: 
            err = - error_tol
        else:
            err = - error_tol * 10 ** (n - 1)

        negative_pools = np.array(mass_ids)[np.where(mass < err)[0]]

        negpools = []
        for negpool in negative_pools:
            pool = self.pools[negpool]
            if type(pool).__name__ == "IO":
                continue
            
            pool.negative_state = True
            negpools.append(pool)

        if len(negpools) > 0:
            if n > 3:
                raise ValueError(
                    f"Pools: {[type(p).__name__ for p in negpools]} were negative.")                
            LOGGER.log("warning", f"Overshoot encountered in {negpools}. " +
                "Recalculating fluxes, restoring events.")
            return True

        return False

    def test_nans(self):
        nan_fluxes = np.isnan(self.current_flux)
        if any(nan_fluxes):
            raise ValueError(
                f"""
                these pools had nan values in their fluxes. Make sure there 
                are no zero division errors or similar in the equations
                {[p for p, nan in zip(self.pools, np.where(nan_fluxes)[0]) if nan]}
                """
                # [print(p) for p, nan in zip(self.pools, np.where(nan_fluxes)[0]) if nan]
                # [p.print_previous_flux() for p, nan in zip(self.pools, np.where(nan_fluxes)[0]) if nan]
            )
        return False

    def test_conservation_of_mass(self, mass_ids, error_tol):
        mass_fluxes = self.current_flux[mass_ids]
        sum_fluxes = np.abs(np.sum(mass_fluxes))
        if sum_fluxes <= -error_tol:
            raise ValueError(errormsg(
                f"""Mass was not conserved. During a step, fluxes did not sum to
                zero."""
            ))
        
        return False


    def get_dim_index(self, dim="all"):
        if dim == "all":
            return [i for i, _ in enumerate(self.pools)]
        return [i for i, p in enumerate(self.pools) if isinstance(p, dim)]
    
    def get_pool_names(self, tuples=False):
        if tuples:
            return [(p.environment.__repr__(), type(p).__name__) for p in self.pools]
        return [f"{type(p).__name__} {p.environment.__repr__()}" for p in self.pools]
    
    def state_to_df(self, dim="all"):
        return self.to_df(self.state_record, dim)

    def fluxes_to_df(self, dim="all"):
        return self.to_df(self.record, dim)

    def to_df(self, record, dim="all"):
        idx = self.get_dim_index(dim)
        df = pd.DataFrame.from_records(
            record,
            columns=pd.MultiIndex.from_tuples(self.get_pool_names(tuples=True))
        )
        df = df.iloc[:, idx]
        df = df.sort_index(axis=1)
        df = df.fillna(0)
        df["∑"] = df.sum(axis=1)
        df["Time"] = self.time_record
        return df

    def flux_table(self, dim):
        name = type(self).__name__
        tbl = PrettyTable()
        tbl.field_names = ["Process", "Pool", "influx", "outflux", "from to"]
        inflow = 0
        outflow = 0
        for p in self.pools:
            if isinstance(p, dim):
                tbl, inflow, outflow = p.five_col_style(
                    p.fluxes, tbl, inflow, outflow)
        tbl.add_row(["===", "===", "===", "===", "==="])
        tbl.add_row(["", "Sum", inflow, outflow, ""])
        tbl.align = "r"
        return tbl

    def print_fluxes(self):
        tbl = PrettyTable()
        names = [type(p).__name__ for p in self.pools]
        header = ["time"] + names + ["∑"]
        tbl.field_names = header
        n = len(CLOCK.time_record)
        for i, (time, record) in enumerate(zip(CLOCK.time_record, self.record)):
            if i == int(n / 2):
                pass
                tbl.add_row(["..."]*len(header))
            if i < 25 or i > n-25:
                tbl.add_row(
                    [time] + [f"{val: .2e}" for val in record] +
                    [f"{np.sum(record): .2e}"]
                )
        return tbl.get_string()

    def print_states(self):
        tbl = PrettyTable()
        header = ["time"] + [type(p).__name__ for p in self.pools] + ["∑"]
        tbl.field_names = header
        n = len(CLOCK.time_record)
        for i, (time, record) in enumerate(zip(CLOCK.time_record, self.state_record)):
            if i == int(n / 2):
                pass
                tbl.add_row(["..."] * len(header))
            if i < 25 or i > n-25:
                tbl.add_row(
                    [time] + [f"{flux: .2e}" for flux in record] +
                    [f"{np.sum(record): .2e}"]
                )
        print(tbl.get_string())


class Logger:
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    def __init__(self):
        self.logger = None
        self.default()
        self.errors = 0

    def reset(self):
        self.logger = None
        self.default()
        self.errors = 0

    @property
    def handle(self):
        return self.logger.handlers[0]

    @property
    def logfile(self):
        try:
            logfile = self.handle.baseFilename
        except AttributeError:
            logfile = None
        return logfile

    def stop(self):
        LOGGER.handle.close()

    def default(self, level="DEBUG"):
        loglev = getattr(logging, level)
        logger = logging.getLogger(f"default")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(loglev)
        logger.addHandler(handler)
        self.logger = logger

    def setup(self, name, logfile, level):
        logger = logging.getLogger(f"sim_{name}")
        logger.setLevel(logging.DEBUG)

        # create a file handler
        file_handler = logging.FileHandler(
            logfile, mode='w')
        file_handler.setLevel(getattr(logging, level))
        # create a logging format
        # we're limiting the levelname to 1 char: I=INFO, D=DEBUG and so on
        formatter = logging.Formatter(
            '%(simtime)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)

        # add the handler to the logger
        logger.addHandler(file_handler)
        self.logger = logger

    def log(self, level, msg):
        extra = {"simtime": CLOCK.time}
        logger = getattr(self.logger, level.lower())
        logger(msg, extra=extra)


BALANCE = Balance()
CLOCK = Clock()
SCHEDULE = Schedule()
LOGGER = Logger()
