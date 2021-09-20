from dataclasses import dataclass
from typing import Union
from copy import deepcopy

class Fluid:
    """
    Look to refactor this as a base class for specific Liquid, Gas, Supercritical classes.
    """

    def __init__(self,\
                state: str      = 'subcooled',\
                fluidType: str  = 'Unknown',\
                p: float        = 1e5,\
                T: float        = 298.15,\
                **kwargs) -> None:
        self.state: str = state
        self.fluidType = fluidType
        self.p = p
        self.T: float = T
        self.__dict__.update(kwargs)
        self.getEnthalpy()
        return
    
    def getEnthalpy(self):
        if hasattr(self, 'h'):
            pass
        elif hasattr(self, 'cp'):
            self.h = self.cp * self.T
        else:
            raise AttributeError("Fluid must define sufficent variables to specify the fluid enthalpy.")

    @property
    def state(self):
        return self.__state
    
    @state.setter
    def state(self, state):
        self.__state = state if (state in ['subcooled', 'vapour', 'gaseous', 'supercritical', 'unknown']) else self.__state
        return None