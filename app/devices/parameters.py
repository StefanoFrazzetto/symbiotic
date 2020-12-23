from __future__ import annotations
from abc import ABC, abstractmethod
import re


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

    @staticmethod
    def _rgb_to_hex(rgb: tuple) -> str:
        return '#%02x%02x%02x' % rgb

    def color(self, color) -> LightBulbParameters:
        if type(color) is str:
            match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)
            if match:
                self._color = color
            return self

        if type(color) is tuple:
            self._color = self._rgb_to_hex((color[0], color[1], color[2]))
            return self

        raise ValueError(
            f'Color must be either a string or a tuple of RGB values, got {color}')

    def brightness(self, value: int) -> LightBulbParameters:
        if value < 0 or value > 100:
            raise Exception(
                'Brightness must be a positive number less than 100')
        self._brightness = value
        return self

    def transition_duration(self, seconds: int) -> LightBulbParameters:
        if seconds < 0:
            raise Exception('Transition duration must be a positive number')
        self._transition_duration = seconds * 1000
        return self
