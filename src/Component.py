from typing import Union
from copy import deepcopy

from RocketBench.Port import Port
from RocketBench.Fluid import Fluid
# from RocketBench.Engine import Engine

from RocketBench.PortSubclasses.Inlet import Inlet

def counter(limit = 100):
    i = 1
    while 1 <= limit:
        yield i
        i += 1

genCompCounter = counter()

class Component:
    """
    Parent class for flow components.
    It is intended for the components to be indexed from 1, rather than from zero.
    """

    buildFlag = False

    def __init__(self,\
                engineObject: any = None,\
                componentName: str = 'Generic Component',\
                inputs: Union[dict[Port], list[Port], Port, int] = 1,\
                outputs: Union[dict[Port], list[Port], Port, int, list[float], dict[int, float]] = 1,\
                componentInputPressure = None) -> None:

        self.componentName = componentName ##--This uses the setter to ensure that 'Generic components are automatically numbered correctly.
        self.componentInputPressure = componentInputPressure

        if type(inputs) == dict[Port]:
            self.inputs = inputs
        elif type(inputs) == list[Port]:
            self.inputs = { i: inputs for i in range(1, len(inputs)+1 , 1) }
        elif type(inputs) == Port:
            self.inputs = {1: inputs}
        elif type(inputs) == int:
            self.inputs = { i: Inlet(1, i) for i in range(1,inputs+1,1) }
        else:
            raise TypeError('inputs to a component must be a Port object, a list of Port objects, or an int to initialise an Inlet object.')
        
        self.mDotTotal = 0
        for port in self.inputs.values():
                self.mDotTotal += port.mdot
                port.linkTail() ##--This provides protection to the setup, ensuring that ports are connected to too many items.
        
        if type(outputs) == dict[Port]:
            self.outputs = outputs
        elif type(outputs) == list[Port]:
            self.outputs = {i:outputs[i] for i in range(1,len(outputs)+1,1)}
        elif type(outputs) == Port:
            self.outputs = {1 : outputs}
        elif type(outputs) == int:
            self.outputs = { i: Port(i, 1/outputs, f'{self.componentName} Output {i}', self.mDotTotal, None) for i in range(1,outputs+1,1) }
        elif type(outputs) == list[float]:
            self.outputs = { i: Port(i, frac, f'{self.componentName} Output {i}', self.mDotTotal, None) for i, frac in zip(range(1,len(outputs)+1,1), outputs) }
        elif type(outputs) == dict[int, float]:
            self.outputs = { i: Port(i, outputs[i], f'{self.componentName} Output {i}', self.mDotTotal, None) for i in outputs }
        else:
            raise TypeError('outputs to a component must be a Port object, a list of Port objects, or an int to initialise Port objects.')
        
        for port in self.outputs.values():
            port.linkHead() ##--This provides protection to the setup, ensuring that ports are connected to too many items.
        
        self.registerNumber = engineObject._compRegIndex
        engineObject._registerComp(self)
        return None
        
    def compute(self):
        self.averageInputs()
        self.run()
        self.writeOutletPortFluids()
        return
    
    def mergeInputs(self) -> Fluid:
        """
        Refactor to do this at the build stage, just before it runs things, that way we can construct new components within the engine itself.
        """
        if len(self.inputs) == 1:
            self.mDotTotal = self.inputs[1].mdot
            self.enthalpyIn = self.inputs[1].mdot * self.inputs[1].fluid.h
            self.avgInputFluid = deepcopy(self.inputs[1].fluid)
            return self.avgInputFluid
        else:
            minP = self.componentInputPressure if self.componentInputPressure else min( [ port.fluid.p for port in self.inputs ] )
            self.mDotTotal, self.enthalpyIn = {}, 0
            for index in self.inputs:
                port = self.inputs[index]
                pft = port.fluid.fluidType.lower()
                self.mDotTotal[pft] = port.mdot + self.mDotTotal[pft] if pft in self.mDotTotal else port.mdot
                self.enthalpyIn += port.mdot * port.fluid.h

                if port.fluid.p != minP:
                    """
                    Make Injector component.
                    """
                    pass
                continue
    
    def writeOutletPortFluids(self):
        for port in self.outlets:
            port.fluid = deepcopy(self.outputFluid)
    
    def run(self):
        return
    
    @property
    def componentName(self):
        return self.__componentName
    
    @componentName.setter
    def componentName(self, componentName):
        global genCompCounter
        self.__componentName = componentName
        self.__componentName += str(next(genCompCounter)) if self.__componentName == 'Generic Component' else ''
        