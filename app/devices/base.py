from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Callable, List

from app import bus, scheduler
from app.core.interfaces import Loggable

from ..web.responses import ServiceResponse
from ..web.services import BaseService
from .parameters import LightBulbParameters, SmartDeviceParameters


@dataclass
class Action(Loggable, ABC):
    name: str
    job: Callable

    def __init__(self, *args, **kwargs):
        self.name = 'not-unique-at-all'
        self.job = kwargs.pop('do', None)
        print(kwargs)
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.job(*args, **kwargs)

    def do(self, job: Callable):
        self.job = job

    @abstractmethod
    def register(self) -> Action:
        pass

    @abstractmethod
    def deregister(self) -> None:
        pass


class SchedulableAction(Action):

    at: datetime.date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def register(self) -> SchedulableAction:
        """ Registeres the action in the scheduler. """
        # TODO: This should probably generate a unique id.
        return scheduler.every().tag(self.name)
        self.logger.debug(f'registered {self.name} on scheduler')

    def deregister(self) -> None:
        """ Removes an action from the scheduler. """
        # Should probably use the tag to remove it. Unique id?
        scheduler.clear(self.name)
        self.logger.debug(f'removed {self.name} from scheduler')


class EventableAction(Action):

    event: str

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('on')
        super().__init__(*args, **kwargs)

    def register(self) -> EventableAction:
        """ Registers the action with the bus. """
        self.logger.debug(f'{self.event} registered on bus')
        return self

    def deregister(self) -> None:
        """ Removes the action from the bus. """
        self.logger.debug(f'removed {self.event} from bus')


class Actionable(ABC):

    actions: List[Action]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = []

    def event(self, *args, **kwargs) -> Action:
        # TODO: add checking for different types, e.g. tuples or kwargs
        action = EventableAction(**kwargs)
        self.actions.append(action)
        return action.register()

    def schedule(self, *args, **kwargs) -> Action:
        action = SchedulableAction(**kwargs)
        self.actions.append(action)
        return action.register()


class SmartDevice(Loggable, Actionable, ABC):
    """
    SmartDevice encapsulates the methods to control any smart device.
    """

    UPDATES_THROTTLE: int = 5

    class State(Enum):
        ON = 'on'
        OFF = 'off'

        def __str__(self):
            return self.value

    _name: str  # name of the device
    _state: State  # on or off
    _parameters: SmartDeviceParameters  # colour, brightness, etc.
    _service: BaseService  # service used to control the device, e.g IFTTT

    def __init__(self, service: BaseService, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._name = kwargs.pop('name', 'smart device')
        self._state = kwargs.get('state')
        self._service = service
        self._parameters = self._init_parameters(**kwargs)
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

    @property
    def last_update(self) -> int:
        if self._last_update is None:
            return math.inf

        now = datetime.now()
        duration = now - self._last_update
        return int(duration.total_seconds())

    def update(self) -> None:
        self._last_update = datetime.now()

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

        # throttle requests to service
        if (last_update := self.last_update) < SmartDevice.UPDATES_THROTTLE:
            remaining = SmartDevice.UPDATES_THROTTLE - last_update
            message = f'Please wait {remaining} seconds...'
            self.logger.debug(message)
            return ServiceResponse(False, message)

        service_event = self._state_to_service_event(state)

        # get parameters from kwargs, if not None, else get the instance ones
        params = kwargs.get('parameters')
        params = params if params else self.parameters
        response = self._service.trigger(
            event_name=service_event,
            parameters=params.to_dict()
        )

        if response.success:
            self.state = state
            self.update()

        return response

    def switch_on(self, **kwargs) -> ServiceResponse:
        params = kwargs.get('parameters')
        return self._change_state(SmartDevice.State.ON, parameters=params)

    def switch_off(self, **kwargs) -> ServiceResponse:
        params = kwargs.get('parameters')
        return self._change_state(SmartDevice.State.OFF, parameters=params)
