import numpy as np

class MassProperties:
    def __init__(self, init_mass=1000.0, percent_fuel=0.33, burn_rate=5.0):
        self.initial_mass = init_mass          # kg, total mass at start
        self.percent_fuel = percent_fuel
        self.burn_rate = burn_rate                # kg/s
        
        # Derived fields
        self.fuel_mass = self.initial_mass * self.percent_fuel
        self.dry_mass = self.initial_mass - self.fuel_mass
        self.current_mass = self.initial_mass
        
        self.center_of_mass = np.zeros(3)