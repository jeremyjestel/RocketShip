from dataclasses import dataclass, field
import numpy as np
from scipy.spatial.transform import Rotation as R
from guts.Stage import Stage
from guts.compute_COM import compute_COM
from guts.compute_CP import compute_CP
from guts.compute_inertia import compute_inertia
import params


def create_default_stages(percent_fuel: float = 0.33) -> list[Stage]:
    total_mass = sum(stage["mass"] for stage in params.stage_configs)
    fuel_mass = total_mass * percent_fuel
    fuel_unassigned = fuel_mass
    stages = []

    for config in params.stage_configs:
        capacity = config["fuel_capacity"]
        if capacity is None:
            stage_fuel = fuel_unassigned
        else:
            stage_fuel = min(float(capacity), fuel_unassigned)

        fuel_unassigned -= stage_fuel
        dry_mass = config["mass"] - stage_fuel

        stages.append(
            Stage(
                name=config["name"],
                base_z=config["base_z"],
                height=config["height"],
                radius=config["radius"],
                dry_mass=dry_mass,
                fuel_mass=stage_fuel,
                fuel_capacity=stage_fuel,
                normal_force_coeff=config["normal_force_coeff"],
                aero_center_frac=config["aero_center_frac"],
            )
        )

    return stages

@dataclass
class State:
    #these are in world coordinates
    truth_pos: np.ndarray = field(default_factory=lambda: np.zeros(3))           # x, y, z
    truth_vel: np.ndarray = field(default_factory=lambda: np.zeros(3))           # vx, vy, vz
    truth_accel: np.ndarray = field(default_factory=lambda: np.zeros(3))       # ax, ay, az

    #this is in body frame reference
    truth_ang_vel: np.ndarray = field(default_factory=lambda: np.zeros(3))   # wx, wy, wz
    truth_ang_accel: np.ndarray = field(default_factory=lambda: np.zeros(3))#leaving zeroes for now, hardcoded and doesn't change yet

    #The orientation encodes the rotation needed to get from body → world
    truth_orientation: R = field(default_factory=R.identity)   # scipy rotaion, updated with angular velocity

    #the state the rocket believes it is in
    belief_pos: np.ndarray = field(default_factory=lambda: np.zeros(3))           # x, y, z
    belief_vel: np.ndarray = field(default_factory=lambda: np.zeros(3))           # vx, vy, vz
    belief_accel: np.ndarray = field(default_factory=lambda: np.zeros(3))       # ax, ay, az
    belief_ang_vel: np.ndarray = field(default_factory=lambda: np.zeros(3))   # wx, wy, wz
    belief_ang_accel: np.ndarray = field(default_factory=lambda: np.zeros(3))#leaving zeroes for now, hardcoded and doesn't change yet
    belief_orientation: R = field(default_factory=R.identity)   # scipy rotaion, updated with angular velocity
    stages: list[Stage] = field(default_factory=create_default_stages)
    COM: np.ndarray = field(default_factory=lambda: np.zeros(3))
    CP: np.ndarray = field(default_factory=lambda: np.zeros(3))
    I_sum: np.ndarray = field(default_factory=lambda: np.eye(3))
    engine_pos: np.ndarray = field(default_factory=lambda: np.zeros(3))

    current_mass: float = 1000
    current_fuel_mass: float = 1000
    in_flight: bool = False

    def __post_init__(self):
        self.update_mass_properties()

    def update_mass_properties(self):
        self.current_mass = sum(stage.mass for stage in self.stages)
        self.current_fuel_mass = sum(stage.fuel_mass for stage in self.stages)
        self.COM = compute_COM(self.stages)
        self.CP = compute_CP(self.stages)
        self.I_sum = compute_inertia(self.stages, self.COM)

    def burn_fuel(self, burn_amount):
        remaining = max(burn_amount, 0.0)
        for stage in self.stages:
            if remaining <= 0:
                break
            if stage.fuel_mass <= 0:
                continue

            burned = min(stage.fuel_mass, remaining)
            stage.fuel_mass -= burned
            remaining -= burned

        self.update_mass_properties()

    def update_truth_state(self, dt, burn_rate, throttle):
        self.truth_vel += self.truth_accel * dt
        self.truth_pos += self.truth_vel * dt
        self.truth_pos[2] = max(0, self.truth_pos[2])
        if self.truth_pos[2] == 0 and self.truth_vel[2] < 0:
            self.truth_vel[2] = 0

        if self.truth_pos[2] > 0:
            self.in_flight = True

        self.truth_ang_vel += self.truth_ang_accel * dt  # rad/s
        
        # update orientation
        delta_orientation = R.from_rotvec(self.truth_ang_vel * dt)
        self.truth_orientation = self.truth_orientation * delta_orientation

        self.burn_fuel(throttle * burn_rate * dt)

    def update_belief_state(self, dt):
        self.belief_vel += self.belief_accel * dt
        self.belief_pos += self.belief_vel * dt

        self.belief_ang_vel += self.belief_ang_accel * dt  # rad/s
        
        # update orientation
        delta_orientation = R.from_rotvec(self.belief_ang_vel * dt)
        self.belief_orientation = self.belief_orientation * delta_orientation
