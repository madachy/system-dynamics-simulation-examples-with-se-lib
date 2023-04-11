"""
Python model 'test.py'
Translated using PySD
"""

from pathlib import Path

from pysd.py_backend.functions import ramp, pulse
from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.9.1"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 10,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(name="INITIAL TIME", comp_type="Constant", comp_subtype="Normal")
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(name="FINAL TIME", comp_type="Constant", comp_subtype="Normal")
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(name="TIME STEP", comp_type="Constant", comp_subtype="Normal")
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


@component.add(
    name="SAVEPER",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The save time step for the simulation.
    """
    return __data["time"].saveper()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Pulse", comp_type="Auxiliary", comp_subtype="Normal", depends_on={"time": 1}
)
def pulse_1():
    """
    Pulse
    """
    return pulse(__data["time"], 2, magnitude=100)


@component.add(
    name="Ramp", comp_type="Auxiliary", comp_subtype="Normal", depends_on={"time": 1}
)
def ramp_1():
    """
    Ramp
    """
    return ramp(__data["time"], 3, 5)


@component.add(
    name="Level",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_level": 1},
    other_deps={"_integ_level": {"initial": {}, "step": {"pulse_1": 1, "ramp_1": 1}}},
)
def level():
    """
    Level
    """
    return _integ_level()


_integ_level = Integ(lambda: pulse_1() + ramp_1(), lambda: 0, "_integ_level")
