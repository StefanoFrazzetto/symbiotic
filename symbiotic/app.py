from __future__ import annotations
import sys

from .core import Container


class Symbiotic(object):

    def __init__(self):
        self.container = None

    def create_app(self) -> Symbiotic:
        container = Container()
        container.config.logging.from_yaml('configs/logging.yaml')
        container.config.from_yaml('config.yaml')
        container.init_resources()
        container.wire(modules=[sys.modules[__name__]])

        app = Symbiotic()
        app.container = container
        return app

    @property
    def devices(self, *args, **kwargs):
        return self.container.devices

    @property
    def services(self, *args, **kwargs):
        return self.container.services
