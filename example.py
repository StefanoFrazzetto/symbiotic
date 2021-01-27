from gpiozero import Device

from symbiotic import Symbiotic

if __name__ == '__main__':
    app = Symbiotic()
    app.config.from_yaml('config.yaml')

    # use remote motion sensor using pigpio
    pin_factory = app.sensors.pin_factory('pigpio')
    Device.pin_factory = pin_factory
    motion_sensor = app.sensors.gpio_motion_sensor('bedroom', 26)

    # configure light bulb to use IFTTT webhooks
    ifttt = app.services.IFTTT()
    light_bulb = app.devices.light_bulb('bedroom', service=ifttt)

    # turn on light with precise parameters
    red = '#ff0000'
    light_bulb.turn_on(brightness=95, transition_duration='1m', color=red)

    # turn on light only when motion is detected
    light_bulb.event(motion_sensor.active).do(
        light_bulb.turn_on,
        color=(255, 255, 255),
        brightness=85,
        transition_duration=5
    )

    # set a daily schedule to *turn on*
    with light_bulb.schedule(light_bulb.turn_on) as schedule:
        schedule.add(
            brightness=10, transition_duration='60m').every().day.at('23:00')

    # set a daily schedule to *turn off* with different parameters (coming soon)
    with light_bulb.schedule(light_bulb.turn_off) as schedule:
        schedule.add(
            color=red, transition_duration='30m').every().day.at('23:59')

    app.run()
