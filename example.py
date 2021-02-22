from gpiozero import Device

from symbiotic import Symbiotic
from symbiotic.schedule import Schedule, Day
from symbiotic.colours import Colour

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
    light_bulb.turn_on(brightness=95, transition_duration='1m', color=Colour.RED)

    # turn on light only when motion is detected
    with app.events(motion_sensor.active) as events:
        events.do(light_bulb.turn_on, color=Colour.WHITE, brightness=85, transition_duration=5)

    # use schedules to perform control devices
    morning_weekdays = Schedule().weekdays().at('08:00')
    with app.scheduler(morning_weekdays) as scheduler:
        scheduler.add(light_bulb.turn_on, brightness=10, transition_duration='60m')

    evening_schedule = Schedule().every(Day.MONDAY, Day.WEDNESDAY).at('22:00')
    with app.scheduler(evening_schedule) as scheduler:
        scheduler.add(light_bulb.turn_off, transition_duration='90m')

    app.run()
