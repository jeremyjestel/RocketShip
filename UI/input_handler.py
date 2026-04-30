from typing import Dict
import params

class InputHandler:
    def __init__(self, rocket):
        self.rocket = rocket
        self.key_state: Dict[str, bool] = {
            'q': False,
            'w': False,
            'e': False,
            'a': False,
            's': False,
            'd': False,
            'up': False,
            'down': False,
        }

    def _normalize_key(self, key_name: str | None) -> str | None:
        if not key_name:
            return None
        key_name = key_name.lower()
        if key_name.startswith('arrow_'):
            return key_name.split('_', 1)[1]
        if key_name.startswith('arrow'):
            return key_name.replace('arrow', '')
        return key_name

    def _event_key(self, event) -> str | None:
        key = getattr(event, 'key', None)
        key_name = getattr(key, 'name', None)
        return self._normalize_key(key_name)

    def on_key_press(self, event):
        if getattr(event, 'is_repeat', False):
            return
        key = self._event_key(event)
        if key in self.key_state and not self.key_state[key]:
            self.key_state[key] = True

    def on_key_release(self, event):
        key = self._event_key(event)
        if key in self.key_state and self.key_state[key]:
            self.key_state[key] = False

    def apply_controls(self):
        roll_rate = 0.0
        pitch_rate = 0.0
        yaw_rate = 0.0

        if self.key_state['q']:
            roll_rate -= params.control_sensitivity
        if self.key_state['e']:
            roll_rate += params.control_sensitivity
        if self.key_state['w']:
            pitch_rate -= params.control_sensitivity
        if self.key_state['s']:
            pitch_rate += params.control_sensitivity
        if self.key_state['a']:
            yaw_rate -= params.control_sensitivity
        if self.key_state['d']:
            yaw_rate += params.control_sensitivity

        self.rocket.state.truth_ang_vel[0] = pitch_rate
        self.rocket.state.truth_ang_vel[1] = yaw_rate
        self.rocket.state.truth_ang_vel[2] = roll_rate

        if self.key_state['up']:
            self.rocket.engine.throttle = min(1.0, self.rocket.engine.throttle + params.throttle_sensitivity)
        if self.key_state['down']:
            self.rocket.engine.throttle = max(0.0, self.rocket.engine.throttle - params.throttle_sensitivity)
