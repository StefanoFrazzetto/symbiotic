import requests
import time
import yaml
import logging
import sys

from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import MotionSensor
from gpiozero import Device, LED

from app.containers import Application, SmartDevice
from dependency_injector.wiring import Provide

# use pigpio for security (network daemon instead of root owner /dev/gpiomem)
Device.pin_factory = PiGPIOFactory()


def main(device: SmartDevice = Provide[Application.device]):
    logging.info("Application started.")

    pir = MotionSensor(4)  # pin 4
    pir.when_motion = device.switch_on
    pir.when_no_motion = device.switch_off

    while True:
        pir.wait_for_motion()
        logging.debug("Motion started.")
        time.sleep(5)


if __name__ == '__main__':
    application = Application()
    application.config.from_yaml('config.yaml')
    application.config.logging.from_yaml('configs/logging.yaml')
    application.init_resources()
    application.wire(modules=[sys.modules[__name__]])
    main(*sys.argv[1:])
