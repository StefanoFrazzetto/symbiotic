from __future__ import annotations
import sys

from .containers import Container


class Symbiotic(object):

    def __init__(self):
        self.container = self.create_container()

    def create_container(self) -> Symbiotic:
        container = Container()
        container.config.logging.from_yaml('configs/logging.yaml')
        container.config.from_yaml('config.yaml')
        container.init_resources()
        container.wire(modules=[sys.modules[__name__]])
        return container

    @property
    def devices(self, *args, **kwargs):
        return self.container.devices

    @property
    def services(self, *args, **kwargs):
        return self.container.services
