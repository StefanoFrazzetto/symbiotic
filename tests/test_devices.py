import pytest
import unittest

from context import devices, services, responses
from pytest_mock import MockerFixture

SERVICE_CALL_SUCCESS = 'mock-success-call'
SERVICE_CALL_FAIL = 'mock-fail-call'


@pytest.fixture
def ifttt_success(mocker: MockerFixture) -> services.IFTTT:
    ifttt_mock = mocker.Mock(spec=services.IFTTT)
    ifttt_mock.trigger.return_value = mocker.Mock(
        success = True,
        message = SERVICE_CALL_SUCCESS
    )
    yield ifttt_mock


@pytest.fixture
def ifttt_fail(mocker: MockerFixture) -> services.IFTTT:
    ifttt_mock = mocker.Mock(spec=services.IFTTT)
    ifttt_mock.trigger.return_value = mocker.Mock(
        success = False,
        message = SERVICE_CALL_FAIL
    )
    yield ifttt_mock


class Test_Unit_SmartDevices(object):

    def test_factory(self, ifttt_success) -> None:
        light_bulb = devices.LightBulb(service=ifttt_success)
        response = light_bulb.switch_on()
        assert response.success, response.message


class Test_Integration_LightBulb(object):

    def test_create_light_bulb(self, ifttt_success) -> None:
        light_bulb = devices.LightBulb(service=ifttt_success)
        assert light_bulb is not None
        assert type(light_bulb) is devices.LightBulb

    def test_light_bulb_switch_on_success(self, ifttt_success) -> None:
        light_bulb = devices.LightBulb(service=ifttt_success)
        response = light_bulb.switch_on()
        assert response.success == True
        assert response.message == SERVICE_CALL_SUCCESS

    def test_light_bulb_switch_on_fail(self, ifttt_fail) -> None:
        light_bulb = devices.LightBulb(service=ifttt_fail)
        response = light_bulb.switch_on()
        assert response.success == False
        assert response.message == SERVICE_CALL_FAIL

    def test_light_bulb_switch_off_success(self, ifttt_success) -> None:
        light_bulb = devices.LightBulb(service=ifttt_success)
        response = light_bulb.switch_off()
        assert response.success == True
        assert response.message == SERVICE_CALL_SUCCESS

    def test_light_bulb_switch_off_fail(self, ifttt_fail) -> None:
        light_bulb = devices.LightBulb(service=ifttt_fail)
        response = light_bulb.switch_off()
        assert response.success == False
        assert response.message == SERVICE_CALL_FAIL
