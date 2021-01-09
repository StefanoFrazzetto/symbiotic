import logging
import sys
import time

from dependency_injector.wiring import Provide
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory

from symbiotic import scheduler
from symbiotic.core.containers import Application
from symbiotic.devices.base import LightBulb
from symbiotic.devices.sensors import GPIOMotionSensor
from symbiotic.services import IFTTT


def main(ifttt: IFTTT = Provide[Application.ifttt]):
    logging.info("Application started.")
    # use pigpio for security (network daemon instead of root owner /dev/gpiomem)
    Device.pin_factory = PiGPIOFactory('ubuntu', 8888)
    motion_sensor = GPIOMotionSensor('bedroom', 4)

    light_bulb = LightBulb('bedroom', ifttt)
    light_bulb.event(motion_sensor.active).do(light_bulb.switch_on, color='orange', transition_duration=5)
    with light_bulb.schedule(light_bulb.switch_on) as schedule:
        schedule.add(color='red', brightness=90).every().day.at('21:20')
        schedule.add(color='orange', brightness=70).every().day.at('21:35')
        schedule.add(color='pink', brightness=50).every().day.at('21:50')

    while True:
        scheduler.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    application = Application()
    application.init_resources()
    application.config.from_yaml('config.yaml')
    application.wire(modules=[sys.modules[__name__]])
    main(*sys.argv[1:])
