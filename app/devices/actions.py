from __future__ import annotations

import atexit
import functools
import secrets
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Callable, List

from app import bus, scheduler
from app.core.interfaces import Loggable
from schedule import Job


class Action(Loggable, ABC):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.pop('name', secrets.token_hex(16))
        self.action = None
        atexit.register(self._unregister)

    def __eq__(self, other: Action):
        return self.name == other.name

    def __hash__(self):
        return hash((self.name))

    def __call__(self):
        return self.action()

    def do(self, action: Callable, **kwargs) -> Action:
        self.action = functools.partial(action, **kwargs)
        return self

    @abstractmethod
    def _register(self) -> Any:
        """ Override to register the action with its handler. """
        pass

    @abstractmethod
    def _unregister(self) -> None:
        """ Override to unregister the action from its handler. """
        pass


class ScheduledAction(Action):

    def __init__(self, action: Callable, **kwargs):
        super().__init__(**kwargs)
        self.do(action, **kwargs)

    @contextmanager
    def _register(self) -> Job:
        """Registers the action with the scheduler.

        Using contextmanager allows to yield an instance of Job and to
        set the scheduled job's job (i.e. this action) from within this
        method, which gives us more control.

        > with device.schedule(action) as schedule:
        >> schedule.day.at('08.30')
        """
        self.logger.debug(f'registered {self.name} on scheduler')
        scheduled_job = scheduler.every().tag(self.name)
        yield scheduled_job
        scheduled_job.do(self)

    def _unregister(self) -> None:
        """ Removes the action from the scheduler. """
        scheduler.clear(self.name)
        self.logger.debug(f'removed {self.name} from scheduler')


class EventedAction(Action):

    event: str

    def __init__(self, on: str, **kwargs):
        super().__init__(**kwargs)
        self.event = on

    def _register(self) -> EventedAction:
        """ Registers the action with the bus. """
        bus.add_event(self, self.event)
        self.logger.debug(f'{self.event} registered on bus')
        return self

    def _unregister(self) -> None:
        """ Removes the action from the bus. """
        # Dirty hack to make the bus remove events:
        # the bus method does comparison by using instance.__name__ == instance
        # but this fails because class instances of Action don't have __name__
        # Implementing __name__ wouldn't work as we override __eq__, so it
        # would try to compare an instance of Action to a string.
        # This could be solved in a better way, but the lazy one take less time.
        self.__name__ = self
        bus.remove_event(self, self.event)
        self.logger.debug(f'removed {self.event} from bus')


class Actionable(ABC):

    actions: List[Action]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = []

    def event(self, name: str, **kwargs) -> Action:
        action = EventedAction(name)
        self.actions.append(action)
        return action._register()

    def schedule(self, job: Callable, **kwargs) -> Job:
        action = ScheduledAction(job, **kwargs)
        self.actions.append(action)
        return action._register()
