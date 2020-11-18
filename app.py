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
from app.devices import SmartDevice
from app.device_parameters import LightBulbParameters
# use pigpio for security (network daemon instead of root owner /dev/gpiomem)
# Device.pin_factory = PiGPIOFactory()


def main(
    light_bulb: SmartDevice = Provide[Application.light_bulb]
    ):
    logging.info("Application started.")

    # pir = MotionSensor(4)  # pin 4
    # pir.when_motion = light_bulb.switch_on
    # pir.when_no_motion = light_bulb.switch_off

    light_bulb.parameters.color(255, 255, 255).brightness(70).transition_duration(10)
    light_bulb.switch_on()
    # while True:
        # pir.wait_for_motion()
        # logging.debug("Motion started.")
        # time.sleep(5)


if __name__ == '__main__':
    application = Application()
    application.init_resources()
    application.config.from_yaml('config.yaml')
    application.wire(modules=[sys.modules[__name__]])
    main(*sys.argv[1:])
