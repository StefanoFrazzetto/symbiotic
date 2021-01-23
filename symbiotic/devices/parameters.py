from __future__ import annotations
from abc import ABC, abstractmethod

from colour import Color


class Parameters(ABC):

    @property
    @abstractmethod
    def default_values(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def ifttt(self) -> dict:
        pass

    def update(self, **kwargs):
        # check keys
        bad_keys = [k for k in kwargs.keys() if k not in self.default_values]
        if bad_keys:
            raise TypeError(
                f'Invalid arguments for {self.__class__}: %r' % bad_keys)

        kwargs_copy = kwargs.copy()

        # try using setters to set values
        for key, value in kwargs_copy.items():
            if (setter := getattr(self, key)) is not None:
                setter(value)
                kwargs.pop(key)

        # set the remaining attributes from kwargs
        self.__dict__.update(kwargs)


class LightBulbParameters(Parameters):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._color = None
        self._brightness = None
        self._transition_duration = None

        # set values using kwargs, or fall back to default ones
        self.update(**{**self.default_values, **kwargs})

    @property
    def default_values(self):
        return {'color': '#ffffff', 'brightness': 100, 'transition_duration': 1000}

    def ifttt(self) -> dict:
        return {
            'value1': self._brightness,
            'value2': self._color,
            'value3': self._transition_duration
        }

    def color(self, color) -> LightBulbParameters:
        def rgb_to_hex(rgb: tuple) -> str:
            return '#%02x%02x%02x' % rgb

        if type(color) is str:
            self._color = Color(color).hex
            return self

        if type(color) is tuple:
            self._color = rgb_to_hex((color[0], color[1], color[2]))
            return self

        raise TypeError(
            f'Color must be either a string or a tuple of RGB values, got {color}')

    def brightness(self, value: int) -> LightBulbParameters:
        if value < 0 or value > 100:
            raise ValueError(
                'Brightness must be a positive number less than 100')
        self._brightness = value
        return self

    @staticmethod
    def convert_duration_string(duration: str):
        value = duration.rstrip('smh')
        unit = duration[len(value):]

        if not value.isnumeric and not int(value):
            raise ValueError('Invalid type for transition duration value.')

        unit = unit.lower()
        value = int(value)
        if unit == 'm':
            value = value * 60
        elif unit == 'h':
            value = value * 3600
        elif unit != 's' and unit != '':
            raise ValueError('Invalid type for transition duration unit.')

        return value

    def transition_duration(self, duration: Union[int, str] = 0) -> LightBulbParameters:
        if type(duration) is str:
            seconds = self.convert_duration_string(duration)
        else:
            seconds = duration

        if seconds < 0:
            raise ValueError('Transition duration must be a positive number')

        self._transition_duration = seconds * 1000
        return self
