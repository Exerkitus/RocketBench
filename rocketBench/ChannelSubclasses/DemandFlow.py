from ..Channel import Channel
from ..Utilities import counter

demFlowCounter = counter()

class DemandFlow(Channel):
    """
    This is a component that will force the solver to assign a specific mass flow rate at a point in the system.
    This is also used to initially introduce fluids to the engine.
    It is inadvisble to use this within the engine if it can be avoided.
    """

    def __init__(self, engineObject, inputs, name: str = 'Generic Demand Flow', mdot: float = 1.0, fluid: any = None, absolutePressure = None):
        name == name + ' ' + next(counter) if name == 'Generic Demand Flow' else name
        super().__init__(engineObject, inputs, name, pressureDrop = None, absoluteOutletPressure=absolutePressure, startingFluid=fluid)
        self.mdot = mdot
        self.lockOutputFluid = True
        self.outputFluid = fluid
    
    def _atBuildMethod(self):
        super()._atBuildMethod()
        return
    pass