from abc import ABC

from symbiotic import bus
from symbiotic.core import interfaces
from gpiozero import MotionSensor as GPIOZeroMotionSensor


class MotionSensor(interfaces.Loggable, ABC):
    """
    MotionSensor provides an interface for motion sensors.

    When motion is detected, the sensor should call `active`;
    this will emit an event on the bus as `sensor_name:active`.

    Args:
        name (str): the name to associate with the motion sensor.
    """
    name: str

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    @property
    def active(self) -> str:
        return f'{self.name}:active'

    @property
    def inactive(self) -> str:
        return f'{self.name}:inactive'

    def active_hook(self):
        self.logger.debug(f'{self.name}: movement detected.')
        bus.emit(self.active)

    def inactive_hook(self):
        self.logger.debug(f'{self.name}: movement stopped.')
        bus.emit(self.inactive)


class GPIOMotionSensor(MotionSensor):

    def __init__(self, name: str, pin: int, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self._sensor = GPIOZeroMotionSensor(pin)
        self._sensor.when_motion = self.active_hook
        self._sensor.when_no_motion = self.inactive_hook
