import logging
import requests

from abc import ABC, abstractmethod
from .responses import ServiceResponse
from ..core.exceptions import ConfigurationError


class BaseService(ABC):

    def __init__(self) -> None:
        self.logger = logging.getLogger(
            f'{__name__}.{self.name}',
        )

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def trigger(self, *args, **kwargs) -> ServiceResponse:
        pass


class IFTTT(BaseService):

    DEFAULT_URL = 'https://maker.ifttt.com/trigger/{event_name}/with/key/{key}'

    def __init__(self, config):
        super().__init__()
        try:
            self._url = config.get('url', IFTTT.DEFAULT_URL)
            self._key = config.pop('key')
        except (AttributeError, KeyError):
            raise ConfigurationError(
                'You must add your IFTTT parameters to your config.yaml file')

    def trigger(self, **kwargs) -> ServiceResponse:
        """Triggers the IFTTT webhook 'event_name' with 'parameters'.

        Parameters
        ----------
        event_name : str
            The name of the webhook to trigger, as defined in the "Event Name".

        parameters : dict, optional
            An optional dictionary containing the parameters to pass with the request.
            It can contain one to three parameters defined as follows:
            {
                'value1': '...',
                'value2': '...',
                'value3': '...'
            }

        """
        event_name: str = kwargs.pop('event_name')
        parameters: dict = kwargs.get('parameters')

        url = self._url.format(event_name=event_name, key=self._key)
        response = requests.post(url, parameters)
        self.logger.debug(response.text)

        return ServiceResponse.from_response(response)
