import unittest
import pytest
from barkus_function_toolkit.decorators.main_decorator import main
from unittest.mock import Mock
from typing import Callable, Any
from tests.helpers import ResponseAssertion, raise_validation_error
from barkus_function_toolkit.errors import UnauthenticatedException, UnauthorizedException

class Gilmar:
    def __init__(self, decorator_sut: Callable[[], Callable]):
        self.perform = Mock()
        self.handle = decorator_sut()(self.perform)

class MainDecoratorTestSuite:
    decorator: Callable[[], Callable]

    perform: Mock
    sut: Callable[[Any], Any]

    def decorate(self, perform: Callable) -> Callable:
        ...

    @pytest.fixture(autouse = True)
    def setup_test(self):
        self.perform = Mock()
        self.handle = self.decorate(self.perform)
        yield
  
    def test_should_invoke_perform_with_correct_parameters(self):
        request = Mock()
        
        self.handle(request)

        self.perform.assert_called_once_with(request)

    def test_should_return_ok_on_success(self):
        response = self.handle(Mock())
        ResponseAssertion(response).assertOK()

    def test_should_handle_UnauthenticatedException(self):
        self.perform.side_effect = UnauthenticatedException

        response = self.handle(Mock())
        ResponseAssertion(response).assertUnauthenticated()

    def test_should_handle_UnauthorizedException(self):
        self.perform.side_effect = UnauthorizedException

        response = self.handle(Mock())
        ResponseAssertion(response).assertUnauthorized()

    def test_should_handle_UnprocessableEntityException(self):
        self.perform.side_effect = raise_validation_error

        response = self.handle(Mock())
        print(response)
        ResponseAssertion(response).assertUnprocessableEntity()

class TestMainDecoratorHttp(MainDecoratorTestSuite, unittest.TestCase):
    def decorate(self, perform: Callable) -> Callable:
        return main.http()(perform)

class TestMainDecoratorCloudEvent(MainDecoratorTestSuite, unittest.TestCase):
    def decorate(self, perform: Callable) -> Callable:
        return main.cloud_event()(perform)