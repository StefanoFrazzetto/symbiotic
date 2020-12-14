import logging
import time
import sys

from dependency_injector.wiring import Provide
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device

from app.core.containers import Application
from app.devices.base import LightBulb
from app.triggers.sensors import MotionSensor
from app import scheduler


def main(light_bulb: LightBulb = Provide[Application.light_bulb], sensor: MotionSensor = Provide[Application.sensor]):
    logging.info("Application started.")
    # use pigpio for security (network daemon instead of root owner /dev/gpiomem)
    Device.pin_factory = PiGPIOFactory()
    light_bulb.action(on='bedroom:active', do=light_bulb.switch_on)
    light_bulb.action(on='bedroom:inactive', do=light_bulb.switch_on)

    while True:
        scheduler.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    application = Application()
    application.init_resources()
    application.config.from_yaml('config.yaml')
    application.wire(modules=[sys.modules[__name__]])
    main(*sys.argv[1:])
