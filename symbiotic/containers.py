import logging.config

from dependency_injector import containers, providers
from event_bus import EventBus
from schedule import Scheduler

from .devices import LightBulb
from .services import IFTTT


class ServiceContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    event_bus = providers.Dependency(EventBus)
    scheduler = providers.Dependency(Scheduler)

    IFTTT = providers.Singleton(IFTTT, config=config.IFTTT)


class DeviceContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    event_bus = providers.Dependency(EventBus)
    scheduler = providers.Dependency(Scheduler)

    light_bulb = providers.Factory(
        LightBulb,
        event_bus=event_bus,
        scheduler=scheduler
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config.logging
    )

    event_bus = providers.Singleton(EventBus)

    scheduler = providers.Singleton(Scheduler)

    devices = providers.Container(
        DeviceContainer,
        event_bus=event_bus,
        scheduler=scheduler,
        config=config.devices,
    )

    services = providers.Container(
        ServiceContainer,
        event_bus=event_bus,
        scheduler=scheduler,
        config=config.services
    )
