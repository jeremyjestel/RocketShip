from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt
import numpy as np

class Panel(QWidget):
    def __init__(self, rocket, position=(1450, 100), pause_callback=None):
        super().__init__()

        self.setWindowTitle('Telemetry')
        self.setWindowFlag(Qt.WindowType.Window, True)
        self.move(*position)
        self.setMinimumWidth(380)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.rocket = rocket
        self.pause_callback = pause_callback

        # -----------------------
        # Create Labels
        # -----------------------
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.on_pause_clicked)

        self.pos_label = QLabel()

        self.vel_label = QLabel()

        self.orientation_label = QLabel()

        self.dynamics_label = QLabel()

        self.system_label = QLabel()

        for label in (
            self.pos_label,
            self.vel_label,
            self.orientation_label,
            self.dynamics_label,
            self.system_label,
        ):
            label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        # -----------------------
        # Layout Sections
        # -----------------------
        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.addWidget(self.pause_button)

        top_row = QHBoxLayout()
        top_row.setSpacing(8)
        middle_row = QHBoxLayout()
        middle_row.setSpacing(8)
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(8)

        # Position group
        pos_group = QGroupBox("Position")
        pos_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        pos_group.setMinimumWidth(170)
        pos_group.setMaximumWidth(180)
        pos_layout = QVBoxLayout()
        pos_layout.setSpacing(2)
        pos_layout.setContentsMargins(2, 2, 2, 2)
        pos_layout.addWidget(self.pos_label)
        pos_group.setLayout(pos_layout)

        # Velocity group
        vel_group = QGroupBox("Velocity")
        vel_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        vel_group.setMinimumWidth(170)
        vel_group.setMaximumWidth(180)
        vel_layout = QVBoxLayout()
        vel_layout.setSpacing(2)
        vel_layout.setContentsMargins(2, 2, 2, 2)
        vel_layout.addWidget(self.vel_label)
        vel_group.setLayout(vel_layout)

        # Orientation group
        orient_group = QGroupBox("Orientation")
        orient_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        orient_group.setMinimumWidth(170)
        orient_group.setMaximumWidth(180)
        orient_layout = QVBoxLayout()
        orient_layout.setSpacing(2)
        orient_layout.setContentsMargins(2, 2, 2, 2)
        orient_layout.addWidget(self.orientation_label)
        orient_group.setLayout(orient_layout)

        # Dynamics group
        dyn_group = QGroupBox("Dynamics")
        dyn_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        dyn_group.setMinimumWidth(170)
        dyn_group.setMaximumWidth(180)
        dyn_layout = QVBoxLayout()
        dyn_layout.setSpacing(2)
        dyn_layout.setContentsMargins(2, 2, 2, 2)
        dyn_layout.addWidget(self.dynamics_label)
        dyn_group.setLayout(dyn_layout)

        # System group
        sys_group = QGroupBox("System")
        sys_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sys_group.setMinimumWidth(360)
        sys_layout = QVBoxLayout()
        sys_layout.setSpacing(2)
        sys_layout.setContentsMargins(2, 2, 2, 2)
        sys_layout.addWidget(self.system_label)
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

        # Velocity
        self.vel_label.setText(
            f"Speed: {speed:.2f} m/s\n"
            f"Vx: {vel[0]:.2f} m/s\n"
            f"Vy: {vel[1]:.2f} m/s\n"
            f"Vz: {vel[2]:.2f} m/s"
        )

        # Orientation
        self.orientation_label.setText(
            f"Pitch: {euler[0]:.1f}°\n"
            f"Roll: {euler[1]:.1f}°\n"
            f"Yaw: {euler[2]:.1f}°"
        )

        # Dynamics
        self.dynamics_label.setText(
            f"Accel: {accel_norm:.2f} m/s²\n"
            f"ax: {accel[0]:.2f}, ay: {accel[1]:.2f}, az: {accel[2]:.2f}\n"
            f"Ang Vel: {np.linalg.norm(ang_vel):.2f} rad/s\n"
            f"wx: {ang_vel[0]:.2f}, wy: {ang_vel[1]:.2f}, wz: {ang_vel[2]:.2f}"
        )


        thrust_mag = np.linalg.norm(self.rocket.engine.thrust_vec * self.rocket.engine.throttle)
        self.system_label.setText(
            f"Time: {sim_time:.2f} s\n"
            f"Mass: {state.current_mass:.2f} kg\n"
            f"Fuel: {state.current_fuel_mass:.2f} kg\n"
            f"Throttle: {self.rocket.engine.throttle:.2f}\n"
            f"Thrust: {thrust_mag:.2f} N"
        )