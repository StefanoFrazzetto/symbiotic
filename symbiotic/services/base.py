import logging

from abc import ABC, abstractmethod
from symbiotic.services.responses import ServiceResponse


class BaseService(ABC):

    def __init__(self, *args, **kwargs) -> None:
        self.logger = logging.getLogger(
            f'{__name__}.{self.name}',
        )

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def trigger(self, *args, **kwargs) -> ServiceResponse:
        pass
