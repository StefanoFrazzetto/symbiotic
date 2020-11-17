import pytest

from context import devices, services, responses
from pytest_mock import MockerFixture

SERVICE_CALL_SUCCESS = 'call success'
SERVICE_CALL_FAIL = 'call failure'


@pytest.fixture
def service_success(mocker: MockerFixture) -> services.BaseService:
    service = mocker.Mock(spec=services.BaseService)
    service.call.return_value = responses.ServiceResponse(
        True, SERVICE_CALL_SUCCESS)
    return service


@pytest.fixture
def service_fail(mocker: MockerFixture) -> services.BaseService:
    service = mocker.Mock(spec=services.BaseService)
    service.call.return_value = responses.ServiceResponse(
        False, SERVICE_CALL_FAIL)
    return service


class LightBulb_IntegrationTests(object):

    def test_create_light_bulb(self, mocker: MockerFixture, service_success: services.BaseService) -> None:
        light_bulb = devices.LightBulb(service=service_success)
        assert light_bulb is not None
        assert type(light_bulb) is devices.LightBulb

    def test_light_bulb_switch_on_success(self, mocker: MockerFixture, service_success: services.BaseService) -> None:
        light_bulb = devices.LightBulb(service=service_success)
        spy = mocker.spy(light_bulb, 'switch_on')
        light_bulb.switch_on()
        assert spy.spy_return.success == True
        assert spy.spy_return.message == SERVICE_CALL_SUCCESS

    def test_light_bulb_switch_on_fail(self, mocker: MockerFixture, service_fail: services.BaseService) -> None:
        light_bulb = devices.LightBulb(service=service_fail)
        spy = mocker.spy(light_bulb, 'switch_on')
        light_bulb.switch_on()
        assert spy.spy_return.success == False
        assert spy.spy_return.message == SERVICE_CALL_FAIL

    def test_light_bulb_switch_off_success(self, mocker: MockerFixture, service_success: services.BaseService) -> None:
        light_bulb = devices.LightBulb(service=service_success)
        spy = mocker.spy(light_bulb, 'switch_off')
        light_bulb.switch_off()
        assert spy.spy_return.success == True
        assert spy.spy_return.message == SERVICE_CALL_SUCCESS

    def test_light_bulb_switch_off_fail(self, mocker: MockerFixture, service_fail: services.BaseService) -> None:
        light_bulb = devices.LightBulb(service=service_fail)
        spy = mocker.spy(light_bulb, 'switch_off')
        light_bulb.switch_off()
        assert spy.spy_return.success == False
        assert spy.spy_return.message == SERVICE_CALL_FAIL
