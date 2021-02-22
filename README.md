# symbiotic

[![PyPI version](https://badge.fury.io/py/symbiotic.svg)](https://badge.fury.io/py/symbiotic)
![Python package tests](https://github.com/StefanoFrazzetto/symbiotic/workflows/Python%20package%20tests/badge.svg)

Symbiotic allows you to create a smart environment where 
you have full control of your IoT devices. Sensors can be 
paired to devices and services to create complex actions and schedules.

Some of the main features are

- Dependency-injection
- Event bus
- Fluent interface
- Job scheduling

## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/)
```
pip install symbiotic[yaml]
```

## Simple app

```python
from symbiotic import Symbiotic
from symbiotic.schedule import Schedule

app = Symbiotic()
app.config.from_yaml('config.yaml')

ifttt = app.services.IFTTT()  # <-- the service to control your device
light_bulb = app.devices.light_bulb('bedroom', service=ifttt)

# create custom schedules
weekdays_morning = Schedule().weekdays().at('08:00')
every_evening = Schedule().every_day().at('19:00')

# tell the app how to use your schedules
with app.scheduler(weekdays_morning) as scheduler:
    scheduler.add(light_bulb.on, brightness=80, transition_duration='30m')

with app.scheduler(weekdays_morning) as scheduler:
    scheduler.add(light_bulb.on, color='red', transition_duration='60m')

app.run()
```
```
* The application is running... (Press CTRL+C to terminate)
```

See [example.py](example.py) to learn how to configure devices like motion sensors.

## Services

To learn how to configure an IFTTT applet, please read the 
[documentation](./docs/IFTTT.md).
Once your applet is configured, make sure to add your configuration 
parameters in _config.yaml_.

## Contributions

Contributions are welcome! Feel free fork the project and to open a pull request.
