from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QPushButton
from PyQt6.QtCore import Qt
import numpy as np

class Panel(QWidget):
    def __init__(self, rocket, position=(100, 100), pause_callback=None):
        super().__init__()

        self.setWindowTitle('Telemetry')
        self.setWindowFlag(Qt.WindowType.Window, True)
        self.move(*position)
        self.setFixedWidth(600)

        self.rocket = rocket
        self.pause_callback = pause_callback

        # -----------------------
        # Create Labels
        # -----------------------
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.on_pause_clicked)

        self.pos_label = QLabel()
        self.alt_label = QLabel()

        self.vel_label = QLabel()
        self.vel_components_label = QLabel()

        self.pitch_label = QLabel()
        self.roll_label = QLabel()
        self.yaw_label = QLabel()

        self.accel_label = QLabel()
        self.ang_vel_label = QLabel()

        self.mass_label = QLabel()
        self.fuel_label = QLabel()
        self.fuel_pct_label = QLabel()
        self.throttle_label = QLabel()
        self.thrust_label = QLabel()
        self.time_label = QLabel()

        # -----------------------
        # Layout Sections
        # -----------------------
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.pause_button)

        top_row = QHBoxLayout()
        middle_row = QHBoxLayout()
        bottom_row = QHBoxLayout()

        # Position group
        pos_group = QGroupBox("Position")
        pos_layout = QVBoxLayout()
        pos_layout.addWidget(self.pos_label)
        pos_layout.addWidget(self.alt_label)
        pos_group.setLayout(pos_layout)

        # Velocity group
        vel_group = QGroupBox("Velocity")
        vel_layout = QVBoxLayout()
        vel_layout.addWidget(self.vel_label)
        vel_layout.addWidget(self.vel_components_label)
        vel_group.setLayout(vel_layout)

        # Orientation group
        orient_group = QGroupBox("Orientation")
        orient_layout = QVBoxLayout()
        orient_layout.addWidget(self.pitch_label)
        orient_layout.addWidget(self.roll_label)
        orient_layout.addWidget(self.yaw_label)
        orient_group.setLayout(orient_layout)

        # Dynamics group
        dyn_group = QGroupBox("Dynamics")
        dyn_layout = QVBoxLayout()
        dyn_layout.addWidget(self.accel_label)
        dyn_layout.addWidget(self.ang_vel_label)
        dyn_group.setLayout(dyn_layout)

        # System group
        sys_group = QGroupBox("System")
        sys_layout = QVBoxLayout()
        sys_layout.addWidget(self.time_label)
        sys_layout.addWidget(self.mass_label)
        sys_layout.addWidget(self.fuel_label)
        sys_layout.addWidget(self.fuel_pct_label)
        sys_layout.addWidget(self.throttle_label)
        sys_layout.addWidget(self.thrust_label)
        sys_group.setLayout(sys_layout)

        top_row.addWidget(pos_group)
        top_row.addWidget(vel_group)

        middle_row.addWidget(orient_group)
        middle_row.addWidget(dyn_group)

        bottom_row.addWidget(sys_group)

        main_layout.addLayout(top_row)
        main_layout.addLayout(middle_row)
        main_layout.addLayout(bottom_row)

        self.setLayout(main_layout)

        # Initialize display
        self.update_display()

    def on_pause_clicked(self):
        if self.pause_callback is None:
            return
        paused = self.pause_callback()
        self.pause_button.setText("Resume" if paused else "Pause")

    # -----------------------
    # Update Method
    # -----------------------
    def update_display(self, sim_time: float = 0.0):
        state = self.rocket.state

        pos = state.truth_pos
        vel = state.truth_vel
        speed = np.linalg.norm(vel)
        accel = state.truth_accel
        accel_norm = np.linalg.norm(accel)
        ang_vel = state.truth_ang_vel

        # Orientation (Euler angles)
        euler = state.truth_orientation.as_euler('xyz', degrees=True)

        # Position
        self.pos_label.setText(
            f"X: {pos[0]:.2f} m\n"
            f"Y: {pos[1]:.2f} m\n"
            f"Z: {pos[2]:.2f} m"
        )
        self.alt_label.setText(f"Altitude: {pos[2]:.2f} m")

        # Velocity
        self.vel_label.setText(f"Speed: {speed:.2f} m/s")
        self.vel_components_label.setText(
            f"Vx: {vel[0]:.2f} m/s\n"
            f"Vy: {vel[1]:.2f} m/s\n"
            f"Vz: {vel[2]:.2f} m/s"
        )

        # Orientation
        self.pitch_label.setText(f"Pitch: {euler[0]:.1f}°")
        self.roll_label.setText(f"Roll:  {euler[1]:.1f}°")
        self.yaw_label.setText(f"Yaw:   {euler[2]:.1f}°")

        # Dynamics
        self.accel_label.setText(
            f"Accel: {accel_norm:.2f} m/s²\n"
            f"ax: {accel[0]:.2f}, ay: {accel[1]:.2f}, az: {accel[2]:.2f}"
        )
        self.ang_vel_label.setText(
            f"Ang Vel: {np.linalg.norm(ang_vel):.2f} rad/s\n"
            f"wx: {ang_vel[0]:.2f}, wy: {ang_vel[1]:.2f}, wz: {ang_vel[2]:.2f}"
        )

        # System
        self.mass_label.setText(f"Mass: {state.current_mass:.2f} kg")
        self.fuel_label.setText(f"Fuel: {state.current_fuel_mass:.2f} kg")
        self.time_label.setText(f"Time: {sim_time:.2f} s")
        if self.rocket.mass_props.initial_mass > 0:
            fuel_pct = 100.0 * state.current_fuel_mass / (self.rocket.mass_props.initial_mass * self.rocket.mass_props.percent_fuel)
        else:
            fuel_pct = 0.0
        self.fuel_pct_label.setText(f"Fuel %: {fuel_pct:.1f}%")
        self.throttle_label.setText(f"Throttle: {self.rocket.engine.throttle:.2f}")

        thrust_mag = np.linalg.norm(self.rocket.engine.thrust_vec * self.rocket.engine.throttle)
        self.thrust_label.setText(f"Thrust: {thrust_mag:.2f} N")