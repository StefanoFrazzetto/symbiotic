import logging
from abc import ABC


class Loggable(ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(
            f'{__name__}.{self.__class__.__name__}',
        )
