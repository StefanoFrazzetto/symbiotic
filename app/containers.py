import sys
import yaml
import logging.config

from .services import IFTTTService
from .devices import LightBulb
from dependency_injector import providers, containers


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config.logging
    )

    ifttt = providers.Singleton(IFTTTService, config=config.ifttt)
    device = providers.Factory(LightBulb, service=ifttt)


class SmartDevice(containers.DeclarativeContainer):
    light_bulb = providers.Factory(LightBulb, service=Application.ifttt)
