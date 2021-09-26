from .DemandFlow import DemandFlow
from ..FluidSubclasses.WaterRTP import WaterRTP
from ..Utilities import counter

globalInletCounter = counter()


class GlobalInlet(DemandFlow):

    def __init__(self, engineObject, inputs, name: str = 'Generic Global Input', mdot: float = 1, fluid: any = WaterRTP(), absolutePressure=None):
        name == name + ' ' + next(counter) if name == 'Generic Global Input' else name
        super().__init__(engineObject, inputs, name=name, mdot=mdot, fluid=fluid, absolutePressure=absolutePressure)
