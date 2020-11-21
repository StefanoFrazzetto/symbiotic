from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass

from .device_parameters import *
from .responses import ServiceResponse
from .services import BaseService


class SmartDevice(ABC):
    """
    SmartDevice encapsulates the methods to control any smart device.
    """
    class State(Enum):
        ON = 'on'
        OFF = 'off'

        def __str__(self):
            return self.value

    _name: str  # name of the device
    _state: State  # on or off
    _parameters: SmartDeviceParameters # colour, brightness, etc.
    _service: BaseService # service used to control the device, e.g IFTTT

    def __init__(self, service: BaseService, *args, **kwargs) -> None:
        self._name = kwargs.get('name', 'smart device')
        self._state = kwargs.get('state')
        self._service = service
        self._parameters = self._init_parameters(**kwargs)
        self.logger = logging.getLogger(
            f'{__name__}.{self.__class__.__name__}',
        )

    # @staticmethod
    # def factory(blueprint: dict, *args, **kwargs):
    #     """
    #     Creates a device given a dictionary of parameters, such as
    #     name, type, associated services (e.g. IFTTT), etc.
    #     """
    #     service = kwargs.get('service')

    #     if blueprint['type'] == 'LightBulb':
    #         return LightBulb(service=service)

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
    def _init_parameters(self, **kwargs) -> SmartDeviceParameters:
        pass

    @property
    def parameters(self) -> SmartDeviceParameters:
        return self._parameters


class LightBulb(SmartDevice):

    def __init__(self, service: BaseService, *args, **kwargs):
        super().__init__(service, *args, **kwargs)

    def _init_parameters(self, **kwargs) -> LightBulbParameters:
        """
        Override the abstract method, proving params for the concrete class.
        """
        parameters = kwargs.get('parameters')
        return LightBulbParameters(parameters)

    def _change_state(self, state: SmartDevice.State, **kwargs) -> ServiceResponse:
        self.logger.debug(f"Invoked _change_state with '{state}'")

        if state != self.state:
            service_event = self._state_to_service_event(state)
            params = kwargs.get('parameters')
            # get parameters from kwargs, if not None, else get the instance ones
            params = params if params else self.parameters
            response = self._service.trigger(
                event_name=service_event,
                parameters=params.to_dict()
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
