import logging.config

from ..web.services import IFTTT
from ..devices.base import LightBulb
from ..triggers.sensors import MotionSensor

from event_bus import EventBus
from dependency_injector import providers, containers


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.logging.from_yaml('configs/logging.yaml')

    logging = providers.Resource(
        logging.config.dictConfig,
        config.logging
    )

    bus = providers.Singleton(EventBus)

    ifttt = providers.Singleton(IFTTT, config=config.services.IFTTT)
    light_bulb = providers.Factory(LightBulb, service=ifttt, bus=bus)

    sensor = providers.Factory(MotionSensor, name='bedroom', pin=4, bus=bus)
