from __future__ import annotations

import atexit
import logging
import sys
import time

from cached_property import cached_property
from dependency_injector.providers import Configuration

from .core import _scheduler
from .containers import (
    Container,
    DeviceContainer,
    SensorContainer,
    ServiceContainer,
)


class Symbiotic(object):

    def __init__(self):
        self.container: Container = self.create_container()
        atexit.register(self.shutdown)

    def create_container(self) -> Container:
        container = Container()
        container.config.debug.from_env('SYMBIOTIC_DEBUG')
        container.init_resources()
        container.wire(modules=[sys.modules[__name__]])
        return container

    @property
    def config(self) -> Configuration:
        return self.container.config

    @property
    def debug(self) -> bool:
        debug = self.config.debug
        if debug is not None:
            return debug
        return False

    @property
    def name(self) -> str:
        return 'Symbiotic'

    @cached_property
    def logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)

        if self.debug and not logger.level:
            logger.setLevel(logging.DEBUG)

        return logger

    @property
    def devices(self, *args, **kwargs) -> DeviceContainer:
        return self.container.devices

    @property
    def sensors(self, *args, **kwargs) -> SensorContainer:
        return self.container.sensors

    @property
    def services(self) -> ServiceContainer:
        return self.container.services

    def run(self) -> None:
        try:
            self.logger.info(
                'The application is running... Press CTRL+C to terminate.')
            while True:
                _scheduler.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    def shutdown(self, *args) -> None:
        # sys.stderr.write("\r")  # suppress '^C' in terminal
        # https://stackoverflow.com/a/48726537/5874339
        self.logger.info('Shutdown initiated. Please wait...')
        # Handle application shutdown here...
        self.container.shutdown_resources()
        self.logger.info('Application successfully shutdown.')
        sys.exit(0)
