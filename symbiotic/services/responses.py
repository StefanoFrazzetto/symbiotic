from dataclasses import dataclass
from requests import Response


@dataclass
class ServiceResponse(object):
    success: bool
    message: str

    @staticmethod
    def from_response(response: Response):
        # use raise_for_status with try
        success = response.ok
        return ServiceResponse(success=success, message=response.text)
