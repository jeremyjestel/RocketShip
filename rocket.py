from dataclasses import dataclass, field
import numpy as np
from state import State
from engine import Engine
from mass_properties import MassProperties

@dataclass
class Rocket:
    name: str = "JEREMYS AWESOME FREAKING ROCKET"
    state: State = field(default_factory=State)
    mass_props: MassProperties = field(default_factory=MassProperties)
    engine: Engine = field(default_factory=Engine)
