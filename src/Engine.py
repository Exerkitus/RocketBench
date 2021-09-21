# import numpy as np
from dataclasses import dataclass
from typing import Union
from copy import deepcopy
from RocketBench.Component import Component
from RocketBench.Port import Port

class Engine:
    """
    Class to represent a rocket engine but not its tanks.
    This is just to package the data up a bit so that code is a bit more readable.
    The components of the engine will be initialised in the main() space and then the engine object will use a graph (linked list) and an iterator to solve parameters for steady state.
    """

    # flowGraph: dict[int, dict[int, Component]] = {}
    # __portNumber: int = 0

    # _compRegister: dict[int, Component] = {}
    # _portRegister: dict[int, Port] = {}
    _compRegister: dict[int, any] = {}
    _portRegister: dict[int, any] = {}
    _compRegIndex: int = 0
    _portRegIndex: int = 0
    associationDict: dict[int, dict[str, Union[list[int], int]]] = {} ##--first int is the port key. keys will be 'otherComponentDependencies', 'component' (for the downstream component), 'componentOutputs' (for the outputs of the component that will share the same Fluid as the output of the component)
    def __init__(self) -> None:
        # print(self.flowGraph)
        pass
    
    def _registerComp(self, objToAdd) -> None:
        self._compRegister[self._compRegIndex] = objToAdd

    def _registerPort(self, objToAdd) -> None:
        self._portRegister[self._portRegIndex] = objToAdd

    def build(self):
        if len(self._register) == 0:
            raise AttributeError("At least one component must be to the Engine before attempting to build.")
        for i in range(0,len(self._compRegister),1):
            comp = self._compRegister[i]
            simplifiedInputs = [ output.registerNumber for output in comp.inputs.values() ]
            simplifiedOutputs = [ output.registerNumber for output in comp.outputs.values() ]
            self.associationDict[i] = {}
            for i in simplifiedInputs:
                self.associationDict[i]['otherComponentDependencies'] = deepcopy(simplifiedInputs).remove(i)
                self.associationDict[i]['component'] = i
                self.associationDict[i]['componentOutputs'] = deepcopy(simplifiedOutputs)
                continue
            continue
