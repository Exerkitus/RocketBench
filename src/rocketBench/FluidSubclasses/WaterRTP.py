# import numpy as np
from dataclasses import dataclass
from typing import Union
from copy import deepcopy
from ..Fluid import Fluid

class WaterRTP(Fluid):
    def __init__(self):
        super().__init__(cp = 4185.5, rho = 997)