from gpiozero import Device
from symbiotic import Symbiotic


if __name__ == '__main__':
    app = Symbiotic()
    app.config.from_yaml('config.yaml')

    # set static pin factory for all GPIO devices
    pin_factory = app.sensors.pin_factory('pigpio')
    Device.pin_factory = pin_factory

    # configure a sensor and a light bulb
    motion_sensor = app.sensors.gpio_motion_sensor('bedroom', 26)
    bedroom_light = app.devices.light_bulb('bedroom', service=app.services.IFTTT)

    bedroom_light.event(motion_sensor.active).do(bedroom_light.switch_on, color='white', brightness=85, transition_duration=5)

    with bedroom_light.schedule() as schedule:
        schedule.add(bedroom_light.switch_on, brightness=50).every().day.at('20:30')

    app.run()
