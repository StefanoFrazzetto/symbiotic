from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from enum import Enum

from .device_parameters import SmartDeviceParameters, LightBulbParameters
from .responses import ServiceResponse


class SmartDevice(ABC):
    class State(Enum):
        ON = 'on'
        OFF = 'off'

        def __str__(self):
            return self.value

    _name: str # name of the device
    _state: State # on or off
    _parameters: SmartDeviceParameters # colour, brightness, etc.

    def __init__(self, name, *args, **kwargs) -> None:
        self._name = name
        self._state = kwargs.get('state')
        self._parameters = self._default_parameters()
        self.logger = logging.getLogger(
            f'{__name__}.{self.__class__.__name__}',
    )

    "Map device physical states to IFTTT service_event names."
    states_events_mapping: dict = {
        State.ON: 'bedroom_light_color',
        State.OFF: 'switch_off'
    }

    @staticmethod
    def _state_to_service_event(device_state: State):
        return SmartDevice.states_events_mapping[device_state]

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, state: SmartDevice.State):
        self._state = state

    @abstractmethod
    def _default_parameters(self) -> SmartDeviceParameters:
        """
        Force subclasses to implement this method, so that the
        parameters field is always defined with the proper class type.
        """
        self.logger.error(
            "You need to implement 'default_parameters' in your subclass")
        pass

    @property
    def parameters(self) -> SmartDeviceParameters:
        return self._parameters


class LightBulb(SmartDevice):

    def __init__(self, *args, **kwargs):
        name = "light bulb"
        self._service = kwargs.pop('service')
        super().__init__(name, *args, **kwargs)

    def _default_parameters(self):
        return LightBulbParameters()

    def _change_state(self, state: SmartDevice.State, **kwargs) -> ServiceResponse:
        self.logger.debug(f"Invoked _change_state with '{state}'")

        if state != self.state:
            service_event = self._state_to_service_event(state)
            params = kwargs.get('parameters')
            # get parameters from kwargs, if not None, else get the instance ones
            params = params.finalize() if params else self.parameters.finalize()
            self.logger.debug(f'Calling {service_event} with parameters: {params}')

            response = self._service.trigger(
                event_name=service_event,
                parameters=params
            )

            if response.success:
                self.state = state

            return response

        return ServiceResponse(True, f'{self.name} is already {self.state}')

    def switch_on(self, **kwargs) -> ServiceResponse:
        params = kwargs.get('parameters')
        return self._change_state(SmartDevice.State.ON, parameters=params)

    def switch_off(self, **kwargs) -> ServiceResponse:
        params = kwargs.get('parameters')
        return self._change_state(SmartDevice.State.OFF, parameters=params)
