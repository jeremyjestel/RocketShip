from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QMessageBox,
    QScrollArea,
)
from PyQt6.QtCore import Qt
import numpy as np
from scipy.spatial.transform import Rotation as R
import params


class InputPanel(QWidget):
    def __init__(self, run_callback=None, position=(100, 100)):
        super().__init__()

        self.setWindowTitle('Simulation Inputs')
        self.setWindowFlag(Qt.WindowType.Window, True)
        self.move(*position)
        self.setMinimumSize(800, 600)
        self.run_callback = run_callback
        self.fields = {}

        self._build_ui()
        self.showMaximized()

    def _build_ui(self):
        layout = QVBoxLayout()
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        content = QWidget()
        form_layout = QFormLayout(content)

        self._add_scalar_field(form_layout, 'init_mass', params.init_mass, unit='kg')
        self._add_scalar_field(form_layout, 'percent_fuel', params.percent_fuel, unit='unitless')
        self._add_vector_field(form_layout, 'wind', params.wind, unit='m/s')
        self._add_vector_field(form_layout, 'starting_pos', params.starting_pos, unit='m')
        self._add_vector_field(form_layout, 'starting_vel', params.starting_vel, unit='m/s')
        self._add_vector_field(form_layout, 'starting_ang_vel', params.starting_ang_vel, unit='rad/s')
        self._add_scalar_field(form_layout, 'burn_rate', params.burn_rate, unit='kg/s')
        self._add_scalar_field(form_layout, 'max_thrust', params.max_thrust, unit='N')
        self._add_scalar_field(form_layout, 'dt', params.dt, unit='s')
        self._add_scalar_field(form_layout, 'max_time', params.max_time, unit='s')
        self._add_scalar_field(form_layout, 'drag_coefficient', params.drag_coefficient, unit='unitless')
        self._add_scalar_field(form_layout, 'A', params.A, unit='m^2')
        self._add_scalar_field(form_layout, 'accelerometer_std', params.accelerometer_std, unit='m/s^2')
        self._add_scalar_field(form_layout, 'gyro_noise_std', params.gyro_noise_std, unit='rad/s')
        self._add_scalar_field(form_layout, 'quadrants', params.quadrants, unit='unitless')
        self._add_scalar_field(form_layout, 'throttle', params.throttle, unit='unitless')
        self._add_scalar_field(form_layout, 'control_sensitivity', params.control_sensitivity, unit='rad/s')
        self._add_scalar_field(form_layout, 'throttle_sensitivity', params.throttle_sensitivity, unit='unitless')

        self.scroll.setWidget(content)
        layout.addWidget(self.scroll)

        controls = QHBoxLayout()
        self.run_button = QPushButton('Run Simulation')
        self.run_button.clicked.connect(self.on_run_clicked)
        self.reset_button = QPushButton('Reset Defaults')
        self.reset_button.clicked.connect(self.on_reset_clicked)

        controls.addWidget(self.reset_button)
        controls.addWidget(self.run_button)
        layout.addLayout(controls)

        self.setLayout(layout)

    def _add_scalar_field(self, layout, name, value, unit=None):
        label_text = f'{name} ({unit})' if unit else name
        field = QLineEdit(str(value))
        layout.addRow(QLabel(label_text), field)
        self.fields[name] = ('scalar', field)

    def _add_vector_field(self, layout, name, value, unit=None):
        label_text = f'{name} ({unit})' if unit else name
        text = ', '.join(str(v) for v in np.asarray(value).ravel())
        field = QLineEdit(text)
        layout.addRow(QLabel(label_text), field)
        self.fields[name] = ('vector', field)

    def on_reset_clicked(self):
        for name, (field_type, field) in self.fields.items():
            current_value = getattr(params, name)
            if field_type == 'scalar':
                field.setText(str(current_value))
            else:
                field.setText(', '.join(str(v) for v in np.asarray(current_value).ravel()))

    def on_run_clicked(self):
        try:
            self.apply_fields()
        except ValueError as error:
            QMessageBox.warning(self, 'Invalid input', str(error))
            return

        if self.run_callback is not None:
            self.run_callback()
        self.close()

    def apply_fields(self):
        for name, (field_type, field) in self.fields.items():
            raw = field.text().strip()
            if field_type == 'scalar':
                try:
                    value = float(raw)
                except ValueError:
                    raise ValueError(f'Invalid numeric value for {name}: {raw}')
                if name in ('quadrants',):
                    params.__dict__[name] = int(value)
                else:
                    params.__dict__[name] = value
            else:
                vector = self._parse_vector(raw, name)
                params.__dict__[name] = vector

        self._recompute_starting_orientation()

    def _parse_vector(self, raw, name):
        parts = [p.strip() for p in raw.replace('[', '').replace(']', '').split(',') if p.strip()]
        if len(parts) != 3:
            raise ValueError(f'{name} must contain 3 values separated by commas')
        try:
            return np.array([float(p) for p in parts], dtype=float)
        except ValueError as err:
            raise ValueError(f'Invalid vector values for {name}: {raw}') from err

    def _recompute_starting_orientation(self):
        velocity = np.asarray(params.starting_vel, dtype=float)
        if np.linalg.norm(velocity) < 1e-8:
            params.starting_orientation = R.identity()
        else:
            v_dir = velocity / np.linalg.norm(velocity)
            body_forward = np.array([0, 0, 1], dtype=float)
            alignment_result = R.align_vectors([v_dir], [body_forward])
            params.starting_orientation = alignment_result[0]
