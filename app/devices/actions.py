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


class Action(Loggable):

    def __init__(self, func: Callable = None, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.pop('name', secrets.token_hex(16))
        self.func = functools.partial(func, **kwargs) if func else None
        atexit.register(self.unregister)

    def __eq__(self, other: Action):
        return self.name == other.name

    def __hash__(self):
        return hash((self.name))

    def __call__(self):
        return self.func()

    def do(self, func: Callable, **kwargs) -> Action:
        self.func = functools.partial(func, **kwargs)
        return self

    def unregister(self) -> None:
        """ Override to unregister the action from its handler. """
        pass


class EventedAction(Action):

    event: str

    def __init__(self, on: str, **kwargs):
        super().__init__(**kwargs)
        self.event = on
        bus.add_event(self, self.event)
        self.logger.debug(f'{self.event} registered on bus')

    def unregister(self) -> None:
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


class ActionScheduler(Loggable):

    def __init__(self, func: Callable, tag: str = None, **kwargs):
        super().__init__(**kwargs)
        self.action = Action(func, **kwargs)
        self.tag = tag
        self.scheduler_jobs = []
        atexit.register(self.clear)

    @property
    def every(self):
        job = scheduler.every().tag(self.tag)
        self.scheduler_jobs.append(job)
        return job

    def finalize(self):
        for job in self.scheduler_jobs:
            job.do(self.action)

    def clear(self):
        for job in self.scheduler_jobs:
            scheduler.cancel_job(job)
            self.logger.debug(f'removed scheduled job for action {job.job_func.name}')


class Actionable(ABC):

    actions: List[Action]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = []

    def event(self, name: str, **kwargs) -> Action:
        action = EventedAction(name)
        self.actions.append(action)
        return action

    @contextmanager
    def schedule(self, job: Callable, **kwargs) -> ActionScheduler:
        """ Registers the action with the scheduler.

        Using contextmanager allows to yield an instance of ActionScheduler
        and to set the scheduled job's job (i.e. this action) from within
        this method, which gives us more control.

        > with device.schedule(action) as schedule:
        >> schedule.day.at('08.30')
        >> schedule.day.at('11.30')
        """
        scheduler = ActionScheduler(job, **kwargs)
        yield scheduler
        scheduler.finalize()
