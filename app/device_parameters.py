from __future__ import annotations
from abc import ABC, abstractmethod


class SmartDeviceParameters(ABC):

    @abstractmethod
    def finalize(self) -> dict:
        pass


class LightBulbParameters(SmartDeviceParameters):

    DEFAULT_COLOR: str = '#ffffff'
    DEFAULT_BRIGHTNESS: int = 100
    DEFAULT_TRANSITION_DURATION = 0

    def __init__(self, *args, **kwargs):
        self._color = kwargs.get(
            'color', 
            LightBulbParameters.DEFAULT_COLOR
        )
        self._brightness = kwargs.get(
            'brightness',
            LightBulbParameters.DEFAULT_BRIGHTNESS
        )
        self._transition_duration = kwargs.get(
            'transition_duration', 
            LightBulbParameters.DEFAULT_TRANSITION_DURATION
        )

    def finalize(self) -> dict:
        return {
            'value1': self._brightness,
            'value2': self._color,
            'value3': self._transition_duration
        }

    @staticmethod
    def _rgb_to_hex(rgb: tuple) -> str:
        return '#%02x%02x%02x' % rgb

    def color(self, *args) -> LightBulbParameters:
        if len(args) != 3:
            raise Exception(
                'You must provide the color as a tuple of RGB values')
        self._color = self._rgb_to_hex((args[0], args[1], args[2]))
        return self

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
