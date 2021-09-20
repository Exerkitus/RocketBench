# import numpy as np
from dataclasses import dataclass
from typing import Union
from copy import deepcopy
from RocketBench.Fluid import Fluid
# from RocketBench.Engine import Engine

class Port:

    def __init__(self,\
                engineObject: any = None,\
                portNumber: int = 1,\
                fraction: float = 0.0,\
                name: str = 'Unnamed Port',\
                sourceMdot: float = 0.0,\
                fluid: Union[Fluid, None] = None) -> None:
        self.portNumber = portNumber
        self.fraction = fraction
        self.name = name
        self.sourceMdot = sourceMdot
        self.fluid = fluid
        self.headLinked, self.tailLinked = False, False
        ##-- I tried this with a dataclass, but it didn't work with the inheritance.
        self.registerNumber = engineObject._portRegIndex
        engineObject._registerPort(self)
        pass
    
    def linkHead(self) -> bool:
        if not self.headLinked:
            self.headLinked = True
        else:
            raise AttributeError(f"Head of Port {self.name} already linked. A port may only connect two components. Automatically generated Ports are automatically linked to the component that generated them.")
    
    def linkTail(self) -> bool:
        if not self.tailLinked:
            self.tailLinked = True
        else:
            raise AttributeError(f"Tail of Port {self.name} already linked. A port may only connect two components. Automatically generated Ports are automatically linked to the component that generated them.")

    @property
    def fraction(self):
        return self.__fraction
    
    @fraction.setter
    def fraction(self, fraction):
        self.__fraction = fraction
        return None
    
    @property
    def fluid(self):
        return self.__fluid
    
    @fluid.setter
    def fluid(self, fluid):
        if type(fluid) == Fluid:
            self.__fluid = fluid
        else:
            TypeError('Port.fluid must be a Fluid object.')
        return None
    
    @property
    def mdot(self):
        return self.sourceMdot * self.__fraction