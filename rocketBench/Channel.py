from typing import Union
from copy import deepcopy

# from .Port import Port
from .Fluid import Fluid
from .Utilities import counter

# from .PortSubclasses.Inlet import Inlet
genCompCounter = counter()

class Channel:
    """
    I'm rebuilding this to hold its output inside iself and to remove ports as a concept.
    I'll let the engine solver contain the flow weightings which it'll set up at build-time.

    The channel will only have one output mass-flow.
    I'll have subclasses of channel (which I might rename back to Component), source and sink, which I will add the option to register onto a 'power channel' which must be conserved.
        Sink will compute how much power it needs to do its job
        Source will compute how much flow it needs to do its job- probably having to back-cast along the tree to discover properties.
    I will have a class that is used to create channels, but provides an interface for helping the up-stream channel communicate the downstream
    """

    __buildFlag = False

    def __init__(self,\
                engineObject: any,\
                inputs: any = None,\
                name: str = 'Generic Component',\
                pressureDrop: Union[float, None] = 0.0,\
                absoluteOutletPressure: Union[float, None] = None,\
                startingFluid: Fluid = None) -> None:

        self.e = engineObject
        self.channelName = name ##--This uses the setter to ensure that 'Generic components are automatically numbered correctly.
        self.pressureDrop = pressureDrop
        self.absolutePressure = absoluteOutletPressure
        self.startingFluid = startingFluid

        if inputs:
            if type(inputs) == list[Channel]:
                self.inputConnections = inputs
            elif (type(inputs) == Channel) or issubclass(type(inputs), Channel):
                self.inputConnections = [ inputs ]
            else:
                raise ValueError(f"type {type(inputs)} is not valid for a channel input.")
        else:
            self.inputConnections = []
        
        self.mdot = None
        self.lockOutputFluid = False
        
        self.e._registerChannel(self)
        return None
        
    def compute(self, inputFluids):
        effectiveInputFluid = self.mergeInputs() ##--Some function to add a component 
        outputFluid = self.computeOutputFluid(effectiveInputFluid)
        return outputFluid

    def computeOutputFluid(self, effectiveInputFluid) -> Fluid:
        """
        This is going to be the function that returns the fluid property at the exit of the channel.
        It needs to be able to access the mass flows at ports throughout the same component.
        e.g., a pump needs to access the power (flow rate) in the power channel in order to define the fluid properties.
        """
        return
    
    def _atBuildMethod(self):
        """
        This is to be a method that will be overwritten by child classes that will allow them to modify the register at build-time.
        """
        if not self.__buildFlag:
            raise ValueError(f"{self.channelName}'s _atBuildMethod() has been called while the __buildFlag is False. This would cause the _atBuildMethod() to fail.")
        return None

    def _setBuildFlag(self):
        self.__buildFlag = True
    
    @property
    def componentName(self):
        return self.__componentName
    
    @componentName.setter
    def componentName(self, componentName):
        global genCompCounter
        self.__componentName = componentName
        self.__componentName += str(next(genCompCounter)) if self.__componentName == 'Generic Component' else ''