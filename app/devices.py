import logging

from enum import Enum
from .responses import ServiceResponse
from .device_parameters import DeviceParameters, KasaLightBulb


class DeviceState(Enum):
    ON = 'on'
    OFF = 'off'

    def __str__(self):
        return self.value


class SmartDevice(object):

    name: str
    state: DeviceState

    "Map device physical states to IFTTT service_event names."
    states_events_mapping: dict = {
        DeviceState.ON: 'bedroom_light_color',
        DeviceState.OFF: 'switch_off'
    }

    def __init__(self, name, *args, **kwargs) -> None:
        self.name = name
        self.state = kwargs.get('state', None)
        self.logger = logging.getLogger(
            f'{__name__}.{self.__class__.__name__}',
        )

    @staticmethod
    def _state_to_service_event(device_state: DeviceState):
        return SmartDevice.states_events_mapping[device_state]


class LightBulb(SmartDevice):

    def __init__(self, *args, **kwargs):
        name = "light bulb"
        self._service = kwargs.pop('service')
        super().__init__(name, *args, **kwargs)

    def _change_state(self, state: DeviceState, **kwargs) -> ServiceResponse:
        if state != self.state:
            service_event = self._state_to_service_event(state)
            params = kwargs.get('parameters')
            response = self._service.call(event=service_event, parameters=params)
            if response.success:
                self.state = state
            return response

        return ServiceResponse(True, f'{self.name} is already {self.state}')

    def switch_on(self, **kwargs) -> ServiceResponse:
        parameters: DeviceParameters = kwargs.get('parameters')
        if not parameters:
            parameters = KasaLightBulb()
        parameters = parameters.done()
        self.logger.debug(f'Invoked switch on with {parameters}')
        return self._change_state(DeviceState.ON, parameters=parameters)

    def switch_off(self) -> ServiceResponse:
        self.logger.debug("Invoked switch off")
        return self._change_state(DeviceState.OFF)
