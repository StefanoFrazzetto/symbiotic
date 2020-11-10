import logging
from enum import Enum


class DeviceState(Enum):
    ON = 'on'
    OFF = 'off'

    def __str__(self):
        return self.value

class SmartDevice(object):

    "Map device physical states to IFTTT service_event names."
    states_events_mapping: dict = {
        DeviceState.ON: 'switch_on',
        DeviceState.OFF: 'switch_off'
    }

    def __init__(self, device_name: str) -> None:
        self.device_name: str = device_name
        self._current_state: DeviceState = None
        self.logger = logging.getLogger(
            f'{__name__}.{self.__class__.__name__}',
        )

    @staticmethod
    def _state_to_service_event(device_state: DeviceState):
        return SmartDevice.states_events_mapping[device_state]

class LightBulb(SmartDevice):

    device_name: str = "light bulb"

    def __init__(self, service):
        self._service = service
        super().__init__(LightBulb.device_name)

    def _change_state(self, new_state: DeviceState):
        if new_state != self._current_state:
            try:
                service_event = self._state_to_service_event(new_state)
                self._service.trigger(service_event)
                self._current_state = new_state
            except Exception as e:
                message = 'Error while changing device state:\n'
                message += f'\texception: {str(e)}\n'
                message += f'\tservice event: {str(service_event)}\n'
                self.logger.error(message)
                raise e

    def switch_on(self):
        self.logger.debug("Invoked switch on")
        self._change_state(DeviceState.ON)

    def switch_off(self):
        self.logger.debug("Invoked switch off")
        self._change_state(DeviceState.OFF)
