import sys
import yaml
import logging.config

from .services import *
from .devices import *

from dependency_injector import providers, containers


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.logging.from_yaml('configs/logging.yaml')

    logging = providers.Resource(
        logging.config.dictConfig,
        config.logging
    )

    ifttt = providers.Singleton(IFTTT, config=config.services.IFTTT)
    light_bulb = providers.Factory(LightBulb, service=ifttt)


class DeviceProvider(containers.DynamicContainer):
    pass    
