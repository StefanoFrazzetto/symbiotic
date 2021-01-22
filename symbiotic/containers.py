import logging.config

from dependency_injector import containers, providers

from .devices import LightBulb
from .services import IFTTT


class ServiceContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    # It's not possible to pass the root config 'config.services'
    # because, if the configuration does not contain the service's
    # config (e.g. IFTTT), any object trying to call that service will
    # throw "AttributeError: 'NoneType' object has no attribute 'get'"
    IFTTT = providers.Singleton(IFTTT, config=config.IFTTT)


class DeviceContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    light_bulb: LightBulb = providers.Factory(LightBulb)




class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config.logging
    )

    devices: DeviceContainer = providers.Container(
        DeviceContainer,
        config=config.devices,
    )

    services: ServiceContainer = providers.Container(
        ServiceContainer,
        config=config.services,
    )
