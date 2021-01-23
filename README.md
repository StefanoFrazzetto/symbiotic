# symbiotic

Symbiotic allows you to create a smart environment where 
you have full control of your IoT devices. Sensors can be 
paired to devices and services to create complex actions and schedules.

Some of the main features of symbiotic are

- Dependency-injection
- Event bus
- Fluent interface
- Job scheduling

## Usage

1. Create the application
```python
from gpiozero import Device
from symbiotic import Symbiotic

app = Symbiotic()
app.config.from_yaml('config.yaml')
```

2. Configure your devices and services
```python
light_bulb = app.devices.light_bulb(
    'bedroom', 
    service=app.services.IFTTT  # <--- service to control the device
)
```

3. Add custom schedules to your devices
```python
# set a daily schedule to *turn on* the device using parameters
with light_bulb.schedule(light_bulb.turn_on) as schedule:
    schedule.add(brightness=10).every().day.at('07:30')
    schedule.add(brightness=80, , transition_duration='30m').every().day.at('18:00')

# set a daily schedule to *turn off* the device using parameters (coming soon)
with light_bulb.schedule(light_bulb.turn_off) as schedule:
    schedule.add(color='red',transition_duration='60m').every().day.at('22:30')
```

4. Run the app
```python
app.run()
```

For a more exhaustive example, see [example.py](example.py).

## Sensors

Symbiotic allows your devices to react to events triggered by remote devices. The following shows how to turn on a light bulb when a motion sensor is triggered
```python
# control GPIO devices through pigpio (remote RaspberryPi controller)
pin_factory = app.sensors.pin_factory('pigpio', host='192.168.1.42')
Device.pin_factory = pin_factory

# configure motion sensor and light bulb
motion_sensor = app.sensors.gpio_motion_sensor('entrance', 12)
light_bulb = app.devices.light_bulb('entrance', service=app.services.IFTTT)

# turn on the device when motion is detected
light_bulb.event(motion_sensor.active).do(
    light_bulb.turn_on,
    color='white',
    brightness=85,
    transition_duration=5
)
```

## Services

### IFTTT

To learn how you can configure an IFTTT applet, please read the 
[documentation](./docs/IFTTT.md).
Once your applet is configured, make sure to add your configuration 
parameters in _config.yaml_.

### More services to come...

## Contributions

Contributions are welcome! Feel free fork the project and to open a pull request.