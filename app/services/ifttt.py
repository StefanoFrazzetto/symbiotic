import requests
from typing import Any

from app.devices.parameters import Parameters
from app.core.exceptions import ConfigurationError
from .base import BaseService
from .responses import ServiceResponse
from schema import Schema, Optional, And, Or


class IFTTT(BaseService):

    DEFAULT_URL = 'https://maker.ifttt.com/trigger/{event_name}/with/key/{key}'

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self._url = config.get('url', IFTTT.DEFAULT_URL)
            self._key = config.pop('key')
        except (AttributeError, KeyError):
            raise ConfigurationError(
                'You must add your IFTTT parameters to your config.yaml file')

    def _validate_parameters(self, parameters: Any = None) -> dict:
        if issubclass(type(parameters), Parameters):
            parameters = parameters.ifttt()

        schema = Schema({
            Optional('value1'): And(Or(int, float, str)),
            Optional('value2'): And(Or(int, float, str)),
            Optional('value3'): And(Or(int, float, str)),
        }, ignore_extra_keys=True)

        return schema.validate(parameters)

    def trigger(self, event_name: str, parameters: Any = None) -> ServiceResponse:
        """Triggers the IFTTT webhook 'event_name' with 'parameters'.

        Parameters
        ----------
        event_name : str
            The name of the webhook to trigger, as defined in the "Event Name".

        parameters : dict, optional
            An optional dictionary containing the parameters to pass with the request.
            It can contain one to three parameters defined as follows:
            {
                (optional)'value1': '...',
                'value2': '...',
                'value3': '...'
            }

        """
        parameters = self._validate_parameters(parameters)
        url = self._url.format(event_name=event_name, key=self._key)
        response = requests.post(url, parameters)

        self.logger.debug(f'Request body: {response.request.body}')
        self.logger.debug(f'Response: {response.text}')

        return ServiceResponse.from_response(response)
