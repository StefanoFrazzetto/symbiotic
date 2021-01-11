import logging.config

from dependency_injector import containers, providers

from .services import IFTTT
from .devices import LightBulb


class ServiceContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    IFTTT = providers.Singleton(IFTTT, config=config.IFTTT)


class DeviceContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    factory = providers.FactoryAggregate(
        light_bulb=providers.Factory(LightBulb)
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config.logging
    )

    devices = providers.Container(
        DeviceContainer,
        config=config.devices,
    )

    services = providers.Container(
        ServiceContainer,
        config=config.services
    )
