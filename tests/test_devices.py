import pytest
from unittest import TestCase

from app.devices.base import LightBulb
from app.web.services import IFTTT
from pytest_mock import MockerFixture

SERVICE_CALL_SUCCESS = 'mock-success-call'
SERVICE_CALL_FAIL = 'mock-fail-call'


@pytest.fixture(scope='function')
def ifttt_success(request, mocker: MockerFixture) -> IFTTT:
    ifttt_mock = mocker.Mock(spec=IFTTT)
    ifttt_mock.trigger.return_value = mocker.Mock(
        success=True,
        message=SERVICE_CALL_SUCCESS
    )
    # set a class attribute on the invoking test context
    request.cls.ifttt = ifttt_mock


@pytest.fixture(scope='function')
def ifttt_fail(request, mocker: MockerFixture) -> IFTTT:
    ifttt_mock = mocker.Mock(spec=IFTTT)
    ifttt_mock.trigger.return_value = mocker.Mock(
        success=False,
        message=SERVICE_CALL_FAIL
    )
    # set a class attribute on the invoking test context
    request.cls.ifttt = ifttt_mock


class Test_Unit_SmartDevices(TestCase):

    @pytest.mark.usefixtures('ifttt_success')
    def test_factory(self) -> None:
        light_bulb = LightBulb(service=self.ifttt)
        response = light_bulb.switch_on()
        assert response.success, response.message


class Test_Integration_LightBulb(TestCase):

    @pytest.mark.usefixtures('ifttt_success')
    def test_create_light_bulb(self) -> None:
        light_bulb = LightBulb(service=self.ifttt)
        assert light_bulb is not None
        assert type(light_bulb) is LightBulb

    @pytest.mark.usefixtures('ifttt_success')
    def test_light_bulb_switch_on_success(self) -> None:
        light_bulb = LightBulb(service=self.ifttt)
        response = light_bulb.switch_on()
        assert response.success is True
        assert response.message == SERVICE_CALL_SUCCESS

    @pytest.mark.usefixtures("ifttt_fail")
    def test_light_bulb_switch_on_fail(self) -> None:
        light_bulb = LightBulb(service=self.ifttt)
        response = light_bulb.switch_on()
        assert response.success is False
        assert response.message == SERVICE_CALL_FAIL

    @pytest.mark.usefixtures('ifttt_success')
    def test_light_bulb_switch_off_success(self) -> None:
        light_bulb = LightBulb(service=self.ifttt)
        response = light_bulb.switch_off()
        assert response.success is True
        assert response.message == SERVICE_CALL_SUCCESS

    @pytest.mark.usefixtures("ifttt_fail")
    def test_light_bulb_switch_off_fail(self) -> None:
        light_bulb = LightBulb(service=self.ifttt)
        response = light_bulb.switch_off()
        assert response.success is False
        assert response.message == SERVICE_CALL_FAIL
