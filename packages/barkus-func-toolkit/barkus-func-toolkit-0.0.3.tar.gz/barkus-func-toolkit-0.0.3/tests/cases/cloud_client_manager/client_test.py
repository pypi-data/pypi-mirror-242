from typing import Any
import unittest
from unittest.mock import Mock, patch
from barkus_function_toolkit.cloud_client_manager import CloudClientManager as makeSut
import pytest

def reraise(exp: Exception, *args, **kwargs):
    raise exp

class MakeMocks:
    def __init__(self, mocker):
        location = "barkus_function_toolkit.cloud_client_manager"
        self.cache: Mock = mocker.patch(f"{location}.ClientCache")
        self.cache_load: Mock = self.cache.load
        self.cache_failed_import: Mock = self.cache.failed_import

    def _intercept_import(self, pkg: str, value: Any) -> Mock:
        import sys
        sys.modules[pkg] = value
        return value

    def hide_import(self, pkg: str):
        class Ejector:
            def __getattribute__(self, __name: str) -> Any:
                raise ModuleNotFoundError(f"No module named '{pkg}'")
            
        return self._intercept_import(pkg, Ejector())

    def mock_import(self, pkg: str) -> Mock:
        return self._intercept_import(pkg, Mock())

def test_should_only_initialize_firestore_client_when_getter_is_accessed(mocker):
    mocks = MakeMocks(mocker)
    firestore_client = mocks.mock_import('google.cloud.firestore').Client
    sut = makeSut()

    mocks.cache_load.assert_not_called()

    sut.firestore

    mocks.cache_load.assert_called_once_with("firestore", firestore_client)

def test_should_invoke_cache_failed_import_with_ModuleNotFound_when_importing_firestore(mocker):
    mocks = MakeMocks(mocker)
    mocks.cache_failed_import.side_effect = reraise
    
    with pytest.raises(ModuleNotFoundError) as mnf:
        sut = makeSut()
        mocks.hide_import('google.cloud.firestore')
        sut.firestore.batch

    mocks.cache_failed_import.assert_called_once_with(mnf.value, "firestore")
    assert repr(mnf.value) == """ModuleNotFoundError("No module named 'google.cloud.firestore'")"""


def test_should_only_initialize_bigquery_client_when_getter_is_accessed(mocker):
    mocks = MakeMocks(mocker)
    bigquery_client = mocks.mock_import('google.cloud.bigquery').Client
    sut = makeSut()

    mocks.cache_load.assert_not_called()

    sut.bigquery

    mocks.cache_load.assert_called_once_with("bigquery", bigquery_client)

def test_should_invoke_cache_failed_import_with_ModuleNotFound_when_importing_bigquery(mocker):
    mocks = MakeMocks(mocker)
    mocks.cache_failed_import.side_effect = reraise
    
    with pytest.raises(ModuleNotFoundError) as mnf:
        sut = makeSut()
        mocks.hide_import('google.cloud.bigquery')
        sut.bigquery

    mocks.cache_failed_import.assert_called_once_with(mnf.value, "bigquery")
    assert repr(mnf.value) == """ModuleNotFoundError("No module named 'google.cloud.bigquery'")"""

def test_should_only_initialize_pubsub_client_when_getter_is_accessed(mocker):
    mocks = MakeMocks(mocker)
    pubsub_client = mocks.mock_import('google.cloud.pubsub').PublisherClient
    sut = makeSut()

    mocks.cache_load.assert_not_called()

    sut.pubsub

    mocks.cache_load.assert_called_once_with("pubsub", pubsub_client)

def test_should_invoke_cache_failed_import_with_ModuleNotFound_when_importing_pubsub(mocker):
    mocks = MakeMocks(mocker)
    mocks.cache_failed_import.side_effect = reraise
    
    with pytest.raises(ModuleNotFoundError) as mnf:
        sut = makeSut()
        mocks.hide_import('google.cloud.pubsub')
        sut.pubsub

    mocks.cache_failed_import.assert_called_once_with(mnf.value, "pubsub")
    assert repr(mnf.value) == """ModuleNotFoundError("No module named 'google.cloud.pubsub'")"""