# import numpy as np
from dataclasses import dataclass
from typing import Union
from copy import deepcopy
# from .Component import Component
# from .Port import Port

class Engine:
    """
    Class to represent a rocket engine but not its tanks.
    This is just to package the data up a bit so that code is a bit more readable.
    The components of the engine will be initialised in the main() space and then the engine object will use a graph (linked list) and an iterator to solve parameters for steady state.
    """

    """

    I'll let the engine solver contain the flow weightings which it'll set up at build-time.
    The solver will have to characterise the power response of any changes to a branch wrt the mass it sends that way - There must be a point where it can distribute the mass to only one power channel upstream of it.

    Require that all components have a stated pressure drop! At least you'll have more to work on, then!
        You can largely solve the fluid properties, ignoring the mass flow rates, just with some statements about each of the processes (e.g. adiabatic, iso thermal, etc.)
        If you have a heat exchanger, you can seed starting temps to make it converge more quickly.
        Then, once everything in the power-channel has had that done, go back thorugh and re-compute until converged.
    """

    SIconversions           = {'Y': 1e24, 'Z':1e21, 'E': 1e18, 'P': 1e15, 'T': 1e12, 'G': 1e9, 'M': 1e6, 'k': 1000, 'd': 1e-1, 'c': 1e-2, 'm': 1e-3, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12, 'f': 1e-15, 'a': 1e-18, 'z': 1e-21, 'y': 1e-24}
    pressureConversions     = {'pa': lambda x: x, 'bar': lambda x: 100000*x, 'psi': lambda x: 6894.7572932*x, 'atm': lambda x: 101325*x, 'torr': lambda x: 133.32236842*x}
    temperatureConversions  = {'k': lambda x: x, 'degc': lambda x: x + 273.15, 'f': lambda x: ((x-32)*5/9) + 273.15}
    powerConversions        = {'w': lambda x: x, 'watt': lambda x: x, 'hp': lambda x: 745.6996715823*x, 'ftlbf/s': lambda x: 1.355817948331*x}

    register: dict[int, any] = {}
    _regIndex: int = 0
    
    def __init__(self,\
                pressureUnit: str = 'bar',\
                temperatureUnit: str = 'K',\
                powerUnit: str = 'W') -> None:
        
        self.pressureConv       = self.__extractConversion(self.pressureConversions, pressureUnit)
        self.temperatureUnit    = self.__extractConversion(self.temperatureConversions, temperatureUnit)
        self.powerUnit          = self.__extractConversion(self.powerConversions, powerUnit)
        self.powerChannels      = {}
        self.mDotController     = {}
        pass
    
    def _registerChannel(self, objToAdd) -> None:
        objToAdd.registerNumber = self._regIndex
        self.register[self._regIndex] = { 'channel' : objToAdd, 'outputFluid': None, 'sendsTo': {}  }
        self._regIndex += 1

    def build(self):

        def recursivePropagate(connections, fluidToPropagate):
            for i in connections:
                if not self.register[i]['channel'].startingFluid:
                    self.register[i]['channel'].startingFluid = fluidToPropagate
                    self.register[i]['outputFluid'] = fluidToPropagate
                    recursivePropagate(self.register[i]['sendsTo'], fluidToPropagate)
                else:
                    self.register[i]['outputFluid'] = self.register[i]['channel'].startingFluid
                    recursivePropagate(self.register[i]['sendsTo'], self.register[i]['channel'].startingFluid)
            return True

        if len(self.register) == 0:
            raise AttributeError("At least one component must be to the Engine before attempting to build.")
        for i in range(0,len(self.register),1):
            channel = self.register[i]['channel']
            channel._setBuildFlag()##--refactor below here.
            print(channel.inputConnections)
            inputNumbers = [ inpuT.registerNumber for inpuT in channel.inputConnections ] if len(channel.inputConnections) else []
            for j in inputNumbers:
                self.register[j]['sendsTo'][i] = None
                continue
            channel._atBuildMethod()
            continue

        ##--Propagate starting fluids
        for i in self.register:
            if self.register[i]['channel'].startingFluid:
                recursivePropagate(self.register[i]['sendsTo'], self.register[i]['channel'].startingFluid)
            else:
                pass

        return True
    
    def __extractConversion(self, unitDict, unit):
        if unit.lower() in unitDict.keys():
            return unitDict[unit.lower()]
        elif (unit[1:].lower() in unitDict.keys()) and (unit[0].lower() in self.SIconversions.keys()):
            return lambda x: self.SIconversions[unit[0].lower()] * unitDict[unit[1:].lower()](x)
        else:
            raise ValueError(f"Unit '{unit}' not supported. The supported units are {list(unitDict.keys())} and the supported prefixes are {list(self.SIconversions.keys())}")