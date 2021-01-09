import logging.config

from dependency_injector import containers, providers

from app.services import IFTTT


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.logging.from_yaml('configs/logging.yaml')

    logging = providers.Resource(
        logging.config.dictConfig,
        config.logging
    )

    ifttt = providers.Singleton(IFTTT, config=config.services.IFTTT)
