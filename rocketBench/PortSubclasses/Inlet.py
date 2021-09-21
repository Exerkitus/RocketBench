# import numpy as np
from dataclasses import dataclass
from typing import Union
from copy import deepcopy
from ..Port import Port
from rocketBench.FluidSubclasses.WaterRTP import WaterRTP

class Inlet(Port):

    def __init__(self, mdot, portNumber: int = 1, fluid = WaterRTP()):
        super().__init__(portNumber, 1.0, f'Inlet {portNumber}', mdot, fluid)