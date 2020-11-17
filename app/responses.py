from abc import ABC, abstractmethod
from dataclasses import dataclass
from requests import Response


@dataclass
class ServiceResponse(object):
    success: bool
    message: str

    # prevent abstract class instantiation
    # https://stackoverflow.com/a/60669138/5874339
    # ---
    # def __new__(cls, *args, **kwargs): 
    #     if cls == ServiceResponse or cls.__bases__[0] == ServiceResponse: 
    #         raise TypeError("Cannot instantiate abstract class.") 
    #     return super().__new__(cls)

    @staticmethod
    def from_response(response: Response):
        # use raise_for_status with try
        success = response.status_code < 400
        return ServiceResponse(success=success, message=response.text)


# class IFTTTResponse(ServiceResponse):

#     @staticmethod
#     def from_response(response: Response):
#         """
#         Instantiate the object using a reponse from the Connect API.
#         https://platform.ifttt.com/docs/connect_api#http-status-codes
#         """
#         return super().from_response(response)
