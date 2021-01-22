from __future__ import annotations

import atexit
import logging
import sys
import time

from cached_property import cached_property

from .core import _scheduler


class Symbiotic(object):

    container: Container
    devices: DeviceContainer
    services: ServiceContainer

    def __init__(self):
        self.container = self.create_container()
        self.logger = logging.getLogger(self.__class__.__name__)
        atexit.register(self.shutdown)

    def create_container(self) -> Symbiotic:
        container = Container()
        container.init_resources()
        container.wire(modules=[sys.modules[__name__]])
        return container

    @property
    def config(self):
        return self.container.config

    @property
    def debug(self) -> bool:
        if (debug := self.config.debug) is not None:
            return debug
        return False

    @property
    def name(self) -> str:
        return 'Symbiotic'

    @cached_property
    def logger(self):
        logger = logging.getLogger(self.name)

        if self.debug and not logger.level:
            logger.setLevel(logging.DEBUG)

        return logger

    @property
    def devices(self, *args, **kwargs):
        return self.container.devices

    @property
    def sensors(self, *args, **kwargs):
        return self.container.sensors

    @property
    def services(self):
        return self.container.services

    def run(self):
        try:
            self.logger.info(
                'The application is running... Press CTRL+C to terminate.')
            while True:
                _scheduler.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    def shutdown(self, *args):
        # sys.stderr.write("\r")  # suppress '^C' in terminal
        # https://stackoverflow.com/a/48726537/5874339
        self.logger.info('Shutdown initiated. Please wait...')
        # Handle application shutdown here...
        self.container.shutdown_resources()
        self.logger.info('Application successfully shutdown.')
        sys.exit(0)
