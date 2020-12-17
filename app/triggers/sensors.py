from abc import ABC

from app import bus
from app.core.interfaces import Loggable
from gpiozero import MotionSensor as GPIOZeroMotionSensor


class MotionSensor(Loggable):

    name: str
    sensor: GPIOZeroMotionSensor

    def __init__(self, name: str, pin: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.sensor = GPIOZeroMotionSensor(pin)
        self.sensor.when_motion = self.active
        self.sensor.when_no_motion = self.inactive

    def active(self):
        self.logger.debug(f'emitting {self.name} switch_on')
        bus.emit(f'{self.name}:active')

    def inactive(self):
        self.logger.debug(f'emitting {self.name} switch_on')
        bus.emit(f'{self.name}:inactive')
