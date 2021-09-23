# from .Channel import Channel
from .Fluid import Fluid

def counter(limit = 100):
    i = 1
    while 1 <= limit:
        yield i
        i += 1

genCompCounter = counter()

class Component:
    """
    A component is a holder for multi-channel elements.
    At this stage, it is just a convenience should I need something in the future.
    """
    buildFlag = False

    def __init__(self,\
                engineObject: any = None,\
                componentName: str = 'Generic Component',\
                inputs: any = 1,\
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
            self.inputs = { i: Inlet(engineObject, 1, i) for i in range(1,inputs+1,1) }
        else:
            raise TypeError('Inputs to a component must be a Port object, a list of Port objects, or an int to initialise an Inlet object for a single conservation channel component.')
        
        if type(outputs) == dict[Port]:
            self.outputs = outputs
        elif type(outputs) == list[Port]:
            self.outputs = {i:outputs[i] for i in range(1,len(outputs)+1,1)}
        elif type(outputs) == Port:
            self.outputs = {1 : outputs}
        elif type(outputs) == int:
            self.outputs = { i: Port(engineObject, i, fraction= None, f'{self.componentName} Output {i}') for i in range(1,outputs+1,1) }
        elif type(outputs) == list[float]:
            self.outputs = { i: Port(engineObject, i, frac, f'{self.componentName} Output {i}', self.mDotTotal, None) for i, frac in zip(range(1,len(outputs)+1,1), outputs) }
        elif type(outputs) == dict[int, float]:
            self.outputs = { i: Port(engineObject, i, outputs[i], f'{self.componentName} Output {i}', self.mDotTotal, None) for i in outputs }
        else:
            raise TypeError('outputs to a component must be a Port object, a list of Port objects, or an int to initialise Port objects.')
        
        for port in self.outputs.values():
            port.linkHead(self.mDotTotal) ##--This provides protection to the setup, ensuring that ports are connected to too many items.
        
        engineObject._registerComp(self)
        engineObject._registerConservation(self)
        return None