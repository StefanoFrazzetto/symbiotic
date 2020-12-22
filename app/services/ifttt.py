import requests

from ..core.exceptions import ConfigurationError
from .base import BaseService
from app.devices.parameters import SmartDeviceParameters
from .responses import ServiceResponse


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

    def _validate_parameters(self, *args, **kwargs) -> dict:
        parameters = {}

        def validate_length(item):
            if len(params) > 3:
                raise ValueError(
                    f'The number of parameters must be three or less, got {item}.')

        def create_dict(items: iter):
            i = 1
            params = {}
            for value in items:
                params[f'value{i}'] = value
                i += 1
            return params

        # check kwargs for SmartDeviceParameters or dict
        if (params := kwargs.get('parameters')) is not None:
            if issubclass(type(params), SmartDeviceParameters):
                parameters = params.ifttt()
            elif type(params) is dict:
                validate_length(params)
                parameters = create_dict(params.values())
            else:
                raise ValueError(f'Invalid type for parameters: {params}.')
        # unpack parameters passed as args
        elif args is not None:
            validate_length(args)
            parameters = create_dict(args)
        else:
            if len(args) > 0 or len(kwargs) > 0:
                raise ValueError(f'Invalid parameters provided: args: {args}, kwargs: {kwargs}.')

        return parameters

    def trigger(self, event_name: str, *args, **kwargs) -> ServiceResponse:
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
        parameters = self._validate_parameters(*args, **kwargs)
        url = self._url.format(event_name=event_name, key=self._key)

        response = requests.post(url, parameters)
        self.logger.debug(response.text)

        return ServiceResponse.from_response(response)
