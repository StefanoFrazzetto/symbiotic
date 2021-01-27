import logging
from abc import ABC

from gpiozero import MotionSensor as GPIOZeroMotionSensor
from gpiozero.exc import BadPinFactory

from ..core import _event_bus, _scheduler
from ..core.exceptions import ConfigurationError


class MotionSensor(ABC):
    """
    MotionSensor provides an interface for motion sensors.

    When motion is detected, the sensor should call `active`;
    this will emit an event on the bus as `sensor_name:active`.

    Args:
        name (str): the name to associate with the motion sensor.
    """
    name: str
    bus = _event_bus
    scheduler = _scheduler

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
        logging.debug(f'{self.name}: movement detected.')
        self.bus.emit(self.active)

    def inactive_hook(self):
        logging.debug(f'{self.name}: movement stopped.')
        self.bus.emit(self.inactive)


class GPIOMotionSensor(MotionSensor):

    def __init__(self, name: str, pin: int, *args, **kwargs):

        try:
            pin_factory = kwargs.pop('pin_factory', None)
            self._sensor = GPIOZeroMotionSensor(pin, pin_factory=pin_factory)
        except BadPinFactory:
            err = f"Cannot instantiate {self.name} without a pin factory!"
            raise ConfigurationError(err)

        super().__init__(name, *args, **kwargs)

        self._sensor.when_motion = self.active_hook
        self._sensor.when_no_motion = self.inactive_hook
