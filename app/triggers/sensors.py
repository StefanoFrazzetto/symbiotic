from event_bus import EventBus
from gpiozero import MotionSensor as GPIOZeroMotionSensor


class MotionSensor(object):
    
    name: str
    sensor: GPIOZeroMotionSensor
    
    def __init__(self, name: str, pin: int, *args, **kwargs):
        self.name = name
        self.sensor = GPIOZeroMotionSensor(pin)
        self.bus = kwargs.pop('bus')
        self.sensor.when_motion = self.active
        self.sensor.when_no_motion = self.inactive
    
    def active(self):
        print(f'emitting {self.name} switch_on')
        self.bus.emit_only(self.name, 'switch_on')
    
    def inactive(self):
        print(f'emitting {self.name} switch_on')
        self.bus.emit_only(self.name, 'switch_off')
