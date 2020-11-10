import logging
import requests


class BaseService(object):

    def __init__(self) -> None:
        self.logger = logging.getLogger(
            f'{__name__}.{self.name}',
        )

    @property
    def name(self) -> str:
        return self.__class__.__name__


class IFTTTService(BaseService):

    def __init__(self, config):
        self._key = config.get('key')
        self._domain = config.get('domain')
        super().__init__()

    def trigger(self, event: str):
        url = "{domain}/trigger/{event}/with/key/{key}".format(
            domain=self._domain, event=event, key=self._key
        )
        response = requests.post(url)
        self.logger.debug(f"Response {response.status_code}:\n{response.text}")
        response.raise_for_status()
