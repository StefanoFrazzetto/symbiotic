from __future__ import annotations

import math
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

from app.core.interfaces import Loggable
from .actions import Actionable
from app.services.responses import ServiceResponse
from app.services import BaseService
from .parameters import LightBulbParameters, Parameters


class SmartDevice(Loggable, Actionable, ABC):
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

    _name: str  # name of the device
    _state: State  # on or off
    _parameters: Parameters  # colour, brightness, etc.
    _service: BaseService  # service used to control the device, e.g IFTTT

    def __init__(self, name: str, service: BaseService, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._name = name
        self._state = kwargs.get('state')
        self._service = service
        self._parameters = self.default_parameters
        self._last_update = None

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

    def _change_state(self, state: SmartDevice.State, **params) -> ServiceResponse:
        self.logger.debug(f"Invoked _change_state: '{state}' with '{params}'")

        # throttle requests to service
        if (last_update := self.last_update) < SmartDevice.UPDATES_THROTTLE:
            remaining = SmartDevice.UPDATES_THROTTLE - last_update
            message = f'Please wait {remaining} seconds...'
            self.logger.debug(message)
            return ServiceResponse(False, message)

        if type(params) is dict:
            # update current parameters with the ones passed
            self.parameters.update(**params)
        else:
            # unexpected type of params
            if params is not None or not issubclass(type(params), Parameters):
                raise ValueError(f'Invalid parameters type: {params}')

        # map the event enum to its string
        service_event = self._state_to_service_event(state)

        # trigger the service
        response = self._service.trigger(
            event_name=service_event,
            parameters=self.parameters
        )

        # update the state and last-update timestamp
        if response.success:
            self.state = state
            self.update()

        return response

    @property
    def last_update(self) -> int:
        if self._last_update is None:
            return math.inf

        now = datetime.now()
        duration = now - self._last_update
        return int(duration.total_seconds())

    def update(self) -> None:
        self._last_update = datetime.now()

    @property
    @abstractmethod
    def default_parameters(self) -> Parameters:
        """ Subclasses must provide their own type of parameters. """
        pass

    @property
    def parameters(self) -> Parameters:
        return self._parameters


class LightBulb(SmartDevice):

    def __init__(self, name: str, service: BaseService, *args, **kwargs):
        super().__init__(name, service, *args, **kwargs)

    @property
    def default_parameters(self) -> LightBulbParameters:
        return LightBulbParameters()

    def switch_on(self, **params) -> ServiceResponse:
        return self._change_state(SmartDevice.State.ON, **params)

    def switch_off(self, **params) -> ServiceResponse:
        return self._change_state(SmartDevice.State.OFF, **params)
