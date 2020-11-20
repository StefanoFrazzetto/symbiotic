from __future__ import annotations

import unittest
from enum import Enum

import pytest
from pytest_mock import mock

from context import responses, services


class StatusCodes(Enum):
    # pylint: disable=unsubscriptable-object
    # the above to suppress errors for the instance methods
    # https://github.com/PyCQA/pylint/issues/2063

    OK = (200, 'ok')
    NO_CONTENT = (204, 'no_content')
    BAD_REQUEST = (400, 'bad_request')
    UNAUTHORIZED = (401, 'unauthorized')
    FORBIDDEN = (403, 'forbidden')
    NOT_FOUND = (404, 'not_found')
    INVALID_PARAMETERS = (422, 'invalid_parameters')
    INTERNAL_SERVER_ERROR = (500, 'internal_server_error')
    BAD_GATEWAY = (502, 'bad_gateway')

    @staticmethod
    def by_reason(reason: str) -> StatusCodes:
        for item in StatusCodes:
            if reason == item.value[1]:
                return item
        raise Exception(f'Reason not found in status codes: {reason}')

    @staticmethod
    def has_reason(reason: str) -> str:
        values = set(item.value[1] for item in StatusCodes)
        return reason in values

    @property
    def code(self) -> int:
        return self.value[0]

    @property
    def reason(self) -> str:
        return self.value[1]


def ifttt_service_valid_key() -> services.IFTTT:
    config = {'key': 'clearly_a_valid_key'}
    return services.IFTTT(config=config)


def ifttt_service_invalid_key() -> services.IFTTT:
    config = {'key': 'clearly_an_invalid_key'}
    return services.IFTTT(config=config)


# This method will be used by the mock to replace requests.post
# Source: https://stackoverflow.com/questions/15753390/how-can-i-mock-requests-and-the-response
def mocked_requests_post(*args, **kwargs):
    from urllib.parse import urlparse

    class MockResponse:
        def __init__(self, status_code, *args, **kwargs):
            self.status_code = status_code
            self.text = kwargs.get('text')
            self.json_data = kwargs.get('json_data')

        def json(self):
            return self.json_data

        @property
        def ok(self):
            return self.status_code < 400

    url = args[0]
    url_segments = urlparse(url).path.split('/')
    event_name = url_segments[2]
    key = url_segments[5]

    # check key
    if key == 'bad_key':  # key is not valid
        return MockResponse(StatusCodes.UNAUTHORIZED.code, StatusCodes.UNAUTHORIZED.reason)
    elif key == 'unauthorized_key':  # permissions not sufficient for action
        return MockResponse(StatusCodes.FORBIDDEN.code, StatusCodes.FORBIDDEN.reason)
    elif key == 'valid_key':
        # key is authorized, check the event_name
        if event_name == 'non-existent_event':
            return MockResponse(StatusCodes.NOT_FOUND.code, StatusCodes.NOT_FOUND.reason)
        elif event_name == 'valid-event_name':
            return MockResponse(StatusCodes.OK.code, StatusCodes.OK.reason)

    return MockResponse(StatusCodes.BAD_REQUEST.code, StatusCodes.BAD_REQUEST.reason)


class IFTTT_UnitTests(unittest.TestCase):

    @mock.patch('app.services.requests.post', side_effect=mocked_requests_post)
    def test_call_trigger_bad_key(self, mock_post):
        ifttt = services.IFTTT(config={'key': 'bad_key'})
        response = ifttt.trigger(event_name='some-event_name')
        self.assertFalse(response.success)

    @mock.patch('app.services.requests.post', side_effect=mocked_requests_post)
    def test_call_trigger_unauthorized_key(self, mock_post):
        ifttt = services.IFTTT(config={'key': 'unauthorized_key'})
        response = ifttt.trigger(event_name='some-event_name')
        self.assertFalse(response.success)

    @mock.patch('app.services.requests.post', side_effect=mocked_requests_post)
    def test_call_trigger_non_existent_event(self, mock_post):
        ifttt = services.IFTTT(config={'key': 'valid_key'})
        response = ifttt.trigger(event_name='non-existent_event')
        self.assertFalse(response.success)

    @mock.patch('app.services.requests.post', side_effect=mocked_requests_post)
    def test_call_trigger_valid_request(self, mock_post):
        ifttt = services.IFTTT(config={'key': 'valid_key'})
        response = ifttt.trigger(event_name='valid-event_name')
        self.assertTrue(response.success)
