# import numpy as np
from dataclasses import dataclass
from typing import Union
from copy import deepcopy
from .Fluid import Fluid
from .Engine import Engine
from .Power import Power

class Port:

    headLinked, tailLinked = False, False

    def __init__(self,\
                engineObject: Union[Engine, None] = None,\
                portNumber: int = 1,\
                mdot: Union[float, None] = None,\
                fraction: Union[float, None] = None,\
                name: str = 'Unnamed Port',\
                sourceMdot: Union[float, None] = None,\
                transfered: Union[Fluid, Power, None] = None) -> None:
        self.portNumber = portNumber
        self.name = name
        self.type
        self.mdot = mdot
        self.sourceMdot = sourceMdot
        self.fluid = fluid

        if (not mdot) and (fraction and sourceMdot):
            self.mdot = fraction * sourceMdot
        elif (not sourceMdot) and (fraction and mdot):
            self.sourceMdot = mdot / fraction
        
        self.toSolveMdot = not mdot
        engineObject._registerPort(self)
        pass
    
    def linkHead(self, sourceMdot) -> bool:
        if not self.headLinked:
            self.headLinked = True
            if (self.mdot and sourceMdot) and (self.mdot > sourceMdot):
                raise ValueError(f"Cannot link Port {self.name} as the mass flow rate set for it {self.mdot} is greater than that of the component that it is being linked to.")
            self.sourceMdot = sourceMdot
        else:
            raise AttributeError(f"Head of Port {self.name} already linked. A port may only connect two components. Automatically generated Ports are automatically linked to the component that generated them.")
        return True
    
    def linkTail(self) -> bool:
        if not self.tailLinked:
            self.tailLinked = True
        else:
            raise AttributeError(f"Tail of Port {self.name} already linked. A port may only connect two components. Automatically generated Ports are automatically linked to the component that generated them.")
        return True

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
    def fraction(self):
        """
        This means that the fraction is not stored directly, only the mass flow into the component and the sourceMdot.
        """
        return self.sourceMdot