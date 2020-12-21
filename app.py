import logging
import sys
import time

from dependency_injector.wiring import Provide
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory

from app import scheduler
from app.core.containers import Application
from app.devices.base import LightBulb
from app.devices.sensors import GPIOMotionSensor
from app.web.services import IFTTT


def main(ifttt: IFTTT = Provide[Application.ifttt]):
    logging.info("Application started.")
    # use pigpio for security (network daemon instead of root owner /dev/gpiomem)
    Device.pin_factory = PiGPIOFactory('ubuntu', 8888)
    motion_sensor = GPIOMotionSensor('bedroom', 4)

    light_bulb = LightBulb('bedroom', ifttt)
    light_bulb.event('bedroom:active').do(light_bulb.switch_on)
    with light_bulb.schedule(light_bulb.switch_off) as schedule:
        schedule.day.at('19:00')

    while True:
        scheduler.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    application = Application()
    application.init_resources()
    application.config.from_yaml('config.yaml')
    application.wire(modules=[sys.modules[__name__]])
    main(*sys.argv[1:])
