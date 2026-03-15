from vehicle import Vehicle
from environment import Environment

class PhysicsEngine:
    def compute_forces(self, vehicle: Vehicle, env: Environment):
        # Placeholder: thrust + gravity
        thrust = vehicle.engine.get_thrust()
        gravity = env.get_gravity(vehicle.state.position) * vehicle.mass_props.mass
        total_force = thrust + gravity
        return total_force

    def step_linear(self, vehicle: Vehicle, env: Environment, dt: float):
        F_total = self.compute_forces(vehicle, env)
        acc = F_total / vehicle.mass_props.mass
        vehicle.state.acceleration = acc
        vehicle.state.velocity += acc * dt
        vehicle.state.position += vehicle.state.velocity * dt

    def step_rotational(self, vehicle: Vehicle, dt: float):
        # Placeholder: simple angular integration
        vehicle.state.angular_velocity += vehicle.state.angular_acceleration * dt
        # orientation update will come later (quaternion math)
