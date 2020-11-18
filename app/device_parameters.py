from abc import ABC, abstractmethod

class DeviceParameters(ABC):

    @abstractmethod
    def done(self) -> dict:
        pass


class KasaLightBulb(object):

    DEFAULT_COLOR: str = '#ffffff'
    DEFAULT_BRIGHTNESS: int = 70
    DEFAULT_TRANSITION_DURATION = 3000

    def __init__(self, *args, **kwargs):
        self._color = kwargs.get('color', KasaLightBulb.DEFAULT_COLOR)
        self._brightness = kwargs.get(
            'brightness', KasaLightBulb.DEFAULT_BRIGHTNESS)
        self._transition_duration = kwargs.get(
            'transition_duration', KasaLightBulb.DEFAULT_TRANSITION_DURATION)

    def done(self):
        return {
            'value1': self._brightness,
            'value2': self._color,
            'value3': self._transition_duration
        }

    @staticmethod
    def _rgb_to_hex(rgb: tuple):
        return '#%02x%02x%02x' % rgb

    def color(self, *args):
        if len(args) != 3:
            raise Exception(
                'You must provide the color as a tuple of RGB values')
        self._color = self._rgb_to_hex((args[0], args[1], args[2]))
        return self

    def brightness(self, value: int):
        if value < 0 or value > 100:
            raise Exception(
                'Brightness must be a positive number less than 100')
        self._brightness = value
        return self

    def transition_duration(self, duration: int):
        if duration < 0:
            raise Exception('Transition duration must be a positive number')
        self._transition_duration = duration
        return self
