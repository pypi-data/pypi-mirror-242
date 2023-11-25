from unittest.mock import Mock, ANY
from typing import Any
from barkus_function_toolkit.publish_to_topic import publish_to_topic as sut
from polyfactory.factories import DataclassFactory
from dataclasses import dataclass

@dataclass
class SutPayload:
    project: str 
    topic: str 
    attributes: Any 
      
class Factory(DataclassFactory[SutPayload]):
    __model__ = SutPayload

class Patcher:
    def __init__(self, mocker):
        location = "barkus_function_toolkit.publish_to_topic"
        self.json: Mock = mocker.patch(f"{location}.json")
        self.json_dumps: Mock = self.json.dumps

        self.client: Mock = mocker.patch(f"{location}.CloudClientManager").pubsub
        self.publish:Mock = self.client.publish

def test_should_publish_to_correct_topic(mocker):
    mocks = Patcher(mocker)
    payload = Factory.build(project = "p", topic = "t").__dict__
    
    sut(**payload)

    mocks.publish.assert_called_once_with("projects/p/topics/t", data = ANY)

def test_should_encode_published_data(mocker):
    mocks = Patcher(mocker)
    payload = Factory.build(attributes = "valid_attributes").__dict__

    mocks.json_dumps.return_value.encode.return_value = "encoded_data"
    
    sut(**payload)

    mocks.json_dumps.assert_called_once_with("valid_attributes")

    mocks.publish.assert_called_once_with(ANY, data = 'encoded_data')
