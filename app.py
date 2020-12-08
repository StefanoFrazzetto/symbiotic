import requests
import time
import yaml
import logging
import sys

from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import MotionSensor
from gpiozero import Device, LED

from dependency_injector.wiring import Provide

from app.containers import Application
from app.services import IFTTT
from app.devices import LightBulb
from app.triggers.sensors import MotionSensor
# use pigpio for security (network daemon instead of root owner /dev/gpiomem)
Device.pin_factory = PiGPIOFactory()


def main(
    light_bulb: LightBulb = Provide[Application.light_bulb]
):
    logging.info("Application started.")

    sensor = MotionSensor('bedroom', 4)


if __name__ == '__main__':
    application = Application()
    application.init_resources()
    application.config.from_yaml('config.yaml')
    application.wire(modules=[sys.modules[__name__]])
    
    main(*sys.argv[1:])
