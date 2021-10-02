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
        self.mDotControllers     = {}
        pass
    
    def _registerChannel(self, objToAdd) -> None:
        objToAdd.registerNumber = self._regIndex
        self.register[self._regIndex] = { 'channel' : objToAdd, 'fedBy': [], 'sendsTo': []  }
        self._regIndex += 1

    def build(self):

        def recursivePropagateFluid(connections, fluidToPropagate):
            for i in connections:
                ri = self.register[i]
                channelI = ri['channel']
                if not channelI.outputFluid:
                    channelI.outputFluid = fluidToPropagate
                    recursivePropagateFluid(ri['sendsTo'], fluidToPropagate)
                else:
                    recursivePropagateFluid(ri['sendsTo'], channelI.outputFluid)
            return True
        
        def writeMdot(self, i, mdot):
            self.register[i]['channel'].mdot = mdot
            return

        def betterMdotPropagate(self, i):
            ri = self.register[i]
            channelI = ri['channel']
            numIn, numOut = len(ri['fedBy']), len(ri['sendsTo'])
            numKnownIn, numKnownOut = sum( 1 if isinstance(self.register[j]['channel'].mdot, float) else 0 for j in ri['fedBy']), sum( 1 if isinstance(self.register[j]['channel'].mdot, float) else 0 for j in ri['sendsTo'])


            completelyUniqueFeeders   =  set( [ len(self.register[j]['sendsTo']) == 1 for j in ri['fedBy']] )
            completelyUniqueReceivers =  set( [ len(self.register[j]['fedBy']) == 1 for j in ri['sendsTo']] )
            completelyUniqueFeeders   = list(completelyUniqueFeeders)[0] if len(completelyUniqueFeeders) == 1 else False
            completelyUniqueReceivers = list(completelyUniqueReceivers)[0] if len(completelyUniqueReceivers) == 1 else False

            if channelI.mdot:
                ##--Split into up and down stream solutions - look for one unknown in each of up and down stream.
                if numIn - numKnownIn == 1 and completelyUniqueFeeders:
                    if numIn == 1:
                        missingChannel = ri['fedBy'][0]
                        missingMdot = channelI.mdot
                        print(f"i = {i}: notNone.1.1 -> cha = {missingChannel}")
                    else:
                        missingChannel = [j for j in ri['fedBy'] if self.register[j]['channel'].mdot == None][0]
                        missingMdot = channelI.mdot - sum( self.register[j]['channel'].mdot for j in ri['fedBy'] if j != missingChannel )
                        print(f"i = {i}: notNone.1.2 -> cha = {missingChannel}")
                    
                    writeMdot(self, missingChannel, missingMdot)
                    betterMdotPropagate(self, missingChannel)
                
                if numOut - numKnownOut == 1 and completelyUniqueReceivers:
                    if numOut == 1:
                        missingChannel = ri['sendsTo'][0]
                        missingMdot = channelI.mdot
                        print(f"i = {i}: notNone.2.1 -> i = {missingChannel}")
                    else:
                        missingChannel = [j for j in ri['sendsTo'] if self.register[j]['channel'].mdot == None][0]
                        missingMdot = channelI.mdot - sum( self.register[j]['channel'].mdot for j in ri['sendsTo'] if j != missingChannel )
                        print(f"i = {i}: notNone.2.2 -> i = {missingChannel}")
                    
                    writeMdot(self, missingChannel, missingMdot)
                    betterMdotPropagate(self, missingChannel)
                
                return
            
            else:
                ##--Look for a complete side to find mdot and then rerun the function to check to see if that can get us further.
                ##--Try to pull when only upstream is available:
                if not (numIn - numKnownIn) and numIn and (numOut - numKnownOut) and completelyUniqueFeeders:
                    mdotAtI = sum( self.register[j]['channel'].mdot for j in ri['fedBy'] )
                    writeMdot(self, i, mdotAtI)
                    betterMdotPropagate(self, i)
                    print("None.1")
                ##--Try to pull when only downstream is available:
                elif not (numOut - numKnownOut) and numOut and (numIn - numKnownIn) and completelyUniqueReceivers:
                    mdotAtI = sum( self.register[j]['channel'].mdot for j in ri['sendsTo'] )
                    writeMdot(self, i, mdotAtI)
                    betterMdotPropagate(self, i)
                    print("None.2")
                ##--If both are available, check if both input and output line up:
                elif (not (numIn - numKnownIn) and numIn and completelyUniqueFeeders) and (not (numOut - numKnownOut) and numOut and completelyUniqueReceivers):
                    mdotAtIupstream   = sum( self.register[j]['channel'].mdot for j in ri['fedBy'] )
                    mdotAtIdownstream = sum( self.register[j]['channel'].mdot for j in ri['sendsTo'] )
                    if not mdotAtIupstream - mdotAtIdownstream:
                        writeMdot(self, i, mdotAtIupstream)
                        print("None.3")
                    else:
                        raise ValueError(f"Problem encountered during mdot propagation at build: demanded flows converge to demand different mass flow rates up and downstream of {channelI.name}: {mdotAtIupstream} upstream and {mdotAtIdownstream} downstream. Remove or rectify demanded mdots that connect to this component to resolve this issue.")

                return
        
        if len(self.register) == 0:
            raise AttributeError("At least one component must be to the Engine before attempting to build.")
        for i in range(0,len(self.register),1):
            channelI = self.register[i]['channel']
            inputNumbers = [ inpuT.registerNumber for inpuT in channelI.inputConnections ] if len(channelI.inputConnections) else []
            self.register[i]['fedBy'] = inputNumbers
            for j in inputNumbers:
                self.register[j]['sendsTo'].append(i)
                continue
            # self.register[i]['mdot'] = channelI.mdot
            channelI._setBuildFlag()
            channelI._atBuildMethod()
            continue
        
        ##--Propagate starting fluids.
        for i in self.register:
            if self.register[i]['channel'].outputFluid:
                recursivePropagateFluid(self.register[i]['sendsTo'], self.register[i]['channel'].outputFluid)
            continue
        
        for i in self.register:
            betterMdotPropagate(self, i)
            for i in self.register:
                d = self.register[i]
                print(i, d['channel'].name, ":", {j:d[j] for j in d if j != 'channel'}, "mdot:", d['channel'].mdot)
            print()
        
        # for i in self.register:
        #     betterMdotPropagate(self, i)

        """
        See if you can find out why fuel plenum doesn't trigger on the first pass.
        """

        return True
    
    def __extractConversion(self, unitDict, unit):
        if unit.lower() in unitDict.keys():
            return unitDict[unit.lower()]
        elif (unit[1:].lower() in unitDict.keys()) and (unit[0].lower() in self.SIconversions.keys()):
            return lambda x: self.SIconversions[unit[0].lower()] * unitDict[unit[1:].lower()](x)
        else:
            raise ValueError(f"Unit '{unit}' not supported. The supported units are {list(unitDict.keys())} and the supported prefixes are {list(self.SIconversions.keys())}")
    
    def solveControl(self):

        return
    
    def run(self, maxIterations = 100):
        return
