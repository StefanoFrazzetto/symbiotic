from __future__ import annotations

import logging
import math
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

from symbiotic.services.base import BaseService
from symbiotic.services.responses import ServiceResponse

from .actions import Actionable
from .parameters import LightBulbParameters, Parameters


class SmartDevice(Actionable, ABC):
    """
    SmartDevice encapsulates the methods to control any smart device.

    Devices are controlled through a BaseService; using the facade pattern
    here allows to add more services in the future without refactoring,
    improves readability, and reduces code coupling.
    """

    UPDATES_THROTTLE: int = 5

    class State(Enum):
        ON = 'on'
        OFF = 'off'

        def __str__(self):
            return self.value

    def __init__(self, name: str, *args, **kwargs) -> None:
        self.name: str = name
        self._state: SmartDevice.State = kwargs.pop('state', None)
        self._service: BaseService = kwargs.pop('service', None)
        self._parameters: Parameters = self.default_parameters
        self._last_update = None
        super().__init__(*args, **kwargs)

    "Map device physical states to IFTTT service_event names."
    states_events_mapping: dict = {
        State.ON: 'bedroom_light_color',
        State.OFF: 'switch_off'
    }

    @staticmethod
    def _state_to_service_event(device_state: State):
        return SmartDevice.states_events_mapping[device_state]

    @property
    @abstractmethod
    def default_parameters(self) -> Parameters:
        raise NotImplementedError(
            "The subclass must override 'parameters'.")

    @property
    def parameters(self) -> Parameters:
        return self._parameters

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, state: SmartDevice.State) -> None:
        self._state = state

    def _change_state(self, state: SmartDevice.State, **kwargs) -> ServiceResponse:
        logging.debug(f"Invoked _change_state: '{state}' with '{kwargs}'")

        if not self._service:
            raise RuntimeError('You need to add a service to this device')

        # throttle requests to service
        if (last_update := self.last_update) < SmartDevice.UPDATES_THROTTLE:
            remaining = SmartDevice.UPDATES_THROTTLE - last_update
            message = f'Please wait {remaining} seconds...'
            logging.debug(message)
            return ServiceResponse(False, message)

        # create new parameters
        parameters = self.parameters.create(**kwargs)

        # map the event enum to its string
        service_event = self._state_to_service_event(state)

        # trigger the service
        response = self._service.trigger(
            event_name=service_event,
            parameters=parameters
        )

        # update the state and last-update timestamp
        if response.success:
            self.state = state
            self.update(parameters)

        return response

    @property
    def last_update(self) -> int:
        if self._last_update is None:
            return math.inf

        now = datetime.now()
        duration = now - self._last_update
        return int(duration.total_seconds())

    def update(self, parameters: Parameters) -> None:
        self._parameters = parameters
        self._last_update = datetime.now()


class LightBulb(SmartDevice):

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

    @property
    def default_parameters(self):
        return LightBulbParameters()

    def turn_on(self, **params) -> ServiceResponse:
        return self._change_state(SmartDevice.State.ON, **params)

    def turn_off(self, **params) -> ServiceResponse:
        return self._change_state(SmartDevice.State.OFF, **params)
