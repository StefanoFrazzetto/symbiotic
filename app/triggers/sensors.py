from event_bus import EventBus
from gpiozero import MotionSensor as GPIOZeroMotionSensor


class MotionSensor(object):
    
    name: str
    sensor: GPIOZeroMotionSensor
    bus = EventBus()
    
    def __init__(self, name: str, pin: int):
        self.name = name
        self.sensor = GPIOZeroMotionSensor(pin)
        self.sensor.when_motion = self.active
        self.sensor.when_no_motion = self.inactive
    
    def active(self):
        MotionSensor.bus.emit(self.name, 'switch_on')
    
    def inactive(self):
        MotionSensor.bus.emit(self.name, 'switch_off')
