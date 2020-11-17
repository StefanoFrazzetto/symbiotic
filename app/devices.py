import logging

from enum import Enum
from .responses import ServiceResponse


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
        DeviceState.ON: 'switch_on',
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

    def _change_state(self, new_state: DeviceState) -> ServiceResponse:
        if new_state != self.state:
            service_event = self._state_to_service_event(new_state)
            response = self._service.call(event=service_event)
            if response.success:
                self.state = new_state
            return response

        return ServiceResponse(True, f'{self.name} is already {self.state}')

    def switch_on(self) -> ServiceResponse:
        self.logger.debug("Invoked switch on")
        return self._change_state(DeviceState.ON)

    def switch_off(self) -> ServiceResponse:
        self.logger.debug("Invoked switch off")
        return self._change_state(DeviceState.OFF)
