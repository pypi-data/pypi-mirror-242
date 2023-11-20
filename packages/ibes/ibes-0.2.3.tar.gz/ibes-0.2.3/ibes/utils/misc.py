import json
import textwrap
from datetime import timedelta
from .errors import errormsg

def check_time(timearg):
    if isinstance(timearg, timedelta):
        t = timearg
    elif isinstance(timearg, dict):
        t = timedelta(**timearg)

    else:
        raise ValueError(errormsg(
            """
            Provide timestep as dict of form e.g. {'seconds': 1} or use a
            datetime.timedelta object, to be unambiguous. For questions
            refer to timedelta documentation
            https://docs.python.org/3.8/library/datetime.html#datetime.timedelta
            """
        ))

    return t


def save_dict_json(obj, fname):
    with open(fname, "w") as fp:
        json.dump(obj, fp, indent=2)