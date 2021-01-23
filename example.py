from gpiozero import Device
from symbiotic import Symbiotic


if __name__ == '__main__':
    app = Symbiotic()
    app.config.from_yaml('config.yaml')

    # control GPIO devices through pigpio (remote RaspberryPi controller)
    pin_factory = app.sensors.pin_factory('pigpio')
    Device.pin_factory = pin_factory

    # configure motion sensor and light bulb
    motion_sensor = app.sensors.gpio_motion_sensor('bedroom', 26)
    light_bulb = app.devices.light_bulb('bedroom', service=app.services.IFTTT)

    # turn on with precise parameters
    light_bulb.turn_on(brightness=95, transition_duration='1m', color='blue')

    # turn on only when motion is detected
    light_bulb.event(motion_sensor.active).do(
        light_bulb.turn_on,
        color='white',
        brightness=85,
        transition_duration=5
    )

    # set a daily schedule to *turn on*
    with light_bulb.schedule(light_bulb.turn_on) as schedule:
        schedule.add(brightness=10, transition_duration='60m').every().day.at('23:00')

    # set a daily schedule to *turn off* with different parameters (coming soon)
    with light_bulb.schedule(light_bulb.turn_off) as schedule:
        schedule.add(color='red', transition_duration='30m').every().day.at('23:59')

    app.run()
