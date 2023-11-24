import pytest
from unittest.mock import Mock
from barkus_function_toolkit.errors import UnauthenticatedException, UnauthorizedException
from barkus_function_toolkit.authenticator import Authenticator as MakeSut

class Context:
    def __init__(self, api_token, request_token):
        self.api_token = api_token
        self.request_token = request_token

        self.request = Mock()
        self.request_headers_get: Mock = self.request.headers.get

        self.request_headers_get.return_value = request_token

        self.sut = MakeSut(AUTH_TOKEN = api_token)

def test_valid_authentication():
    api_token = "valid_token"
    request_token = "valid_token"

    ctx = Context(api_token, request_token)

    ctx.sut.authenticate(ctx.request)
    ctx.request_headers_get.assert_called_once_with(ctx.sut.header_key)

def test_missing_token():
    api_token = "valid_token"
    request_token = None

    ctx = Context(api_token, request_token)
    
    # Call the authenticate function and expect UnauthenticatedException
    with pytest.raises(UnauthenticatedException):
        ctx.sut.authenticate(ctx.request)

def test_invalid_request_token():
    api_token = "valid_token"
    request_token = "invalid_token"

    ctx = Context(api_token, request_token)
    
    # Call the authenticate function and expect UnauthorizedException
    with pytest.raises(UnauthorizedException):
        ctx.sut.authenticate(ctx.request)

def test_invalid_api_token():
    from pydantic import ValidationError

    # Call the authenticate function and expect UnauthorizedException
    with pytest.raises(ValidationError):
        MakeSut(AUTH_TOKEN=None)
