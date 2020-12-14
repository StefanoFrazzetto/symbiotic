from abc import ABC

from app import bus
from gpiozero import MotionSensor as GPIOZeroMotionSensor


class MotionSensor(object):

    name: str
    sensor: GPIOZeroMotionSensor

    def __init__(self, name: str, pin: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.sensor = GPIOZeroMotionSensor(pin)
        self.sensor.when_motion = self.active
        self.sensor.when_no_motion = self.inactive

    def active(self):
        print(f'emitting {self.name} switch_on')
        bus.emit(f'{self.name}:active')

    def inactive(self):
        print(f'emitting {self.name} switch_on')
        bus.emit(f'{self.name}:inactive')
