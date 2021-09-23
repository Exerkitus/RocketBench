from typing import Union

from .Fluid import Fluid


class Mixture:
    
    def __init__(self,\
                mixtureComponents: Union[list[Fluid], dict[str, Fluid]]) -> None:
        self.mixtureComponents = mixtureComponents if type(mixtureComponents) == list[Fluid] else [ *mixtureComponents.values() ]