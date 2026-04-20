from dataclasses import dataclass, field
import numpy as np
from guts.state import State
from guts.engine import Engine
import params

@dataclass
class Rocket:
    name: str = "JEREMYS AWESOME FREAKING ROCKET"
    state: State = field(default_factory=State)
    engine: Engine = field(default_factory=lambda: Engine(params.throttle, params.burn_rate))