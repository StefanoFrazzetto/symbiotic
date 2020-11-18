import logging
import requests

from abc import ABC, abstractmethod
from .responses import ServiceResponse
from .exceptions import ConfigurationError


class BaseService(ABC):

    def __init__(self) -> None:
        self.logger = logging.getLogger(
            f'{__name__}.{self.name}',
        )

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def call(self, *args, **kwargs) -> ServiceResponse:
        pass


class IFTTT(BaseService):

    def __init__(self, config):
        try:
            self.domain = config.get('domain', 'https://maker.ifttt.com')
            self._key = config.pop('key')
        # print an error message if key is missing
        except (AttributeError, KeyError):
            raise ConfigurationError('You must add your IFTTT parameters to your config.yaml file')
        super().__init__()

    def call(self, *args, **kwargs) -> ServiceResponse:
        event: str = kwargs.pop('event')
        parameters: dict = kwargs.get('parameters')
        url = "{domain}/trigger/{event}/with/key/{key}".format(
            domain=self.domain, 
            event=event, 
            key=self._key
        )
        response = requests.post(url, parameters)
        self.logger.debug(response.text)
        return ServiceResponse.from_response(response)
