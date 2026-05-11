from dataclasses import dataclass, field
import numpy as np

@dataclass
class Stage:
    name: str

    # Geometry, body-frame coordinates
    base_z: float
    height: float
    radius: float

    # Mass
    dry_mass: float
    fuel_mass: float
    fuel_capacity: float

    # Aero approximation
    normal_force_coeff: float = 1.0
    aero_center_frac: float = 0.5  # 0 = base, 1 = top
    com: np.ndarray = field(init=False)
    aero_center: np.ndarray = field(init=False)

    def __post_init__(self):
        self.update_geometry_points()

    def update_geometry_points(self):
        self.com = np.array([0.0, 0.0, self.center_z])
        self.aero_center = np.array([
            0.0,
            0.0,
            self.base_z + self.aero_center_frac * self.height,
        ])

    @property
    def top_z(self):
        return self.base_z + self.height

    @property
    def center_z(self):
        return self.base_z + self.height / 2

    @property
    def mass(self):
        return self.dry_mass + self.fuel_mass

    def inertia_about_own_com(self):
        m = self.mass
        r = self.radius
        h = self.height

        Ixx = (1 / 12) * m * (3 * r**2 + h**2)
        Iyy = Ixx
        Izz = 0.5 * m * r**2

        return np.diag([Ixx, Iyy, Izz])
