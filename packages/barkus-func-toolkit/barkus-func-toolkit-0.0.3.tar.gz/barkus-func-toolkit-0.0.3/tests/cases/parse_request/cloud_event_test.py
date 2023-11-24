import unittest
from unittest.mock import Mock, patch
from barkus_function_toolkit.parse_request import cloud_event

def make_event(data: str):
    return Mock(data = { "message": { "data": data } })

class TestParseRequestCloudEvent(unittest.TestCase):

    @patch("barkus_function_toolkit.parse_request.base64.b64decode")
    def test_cloud_event(self, mock_b64decode):
        # Mocking the cloud_event object
        event = Mock()
        event.data = {"message": {"data": "base64_encoded_data"}}

        # Mocking the base64.b64decode function
        mock_b64decode.return_value = b'{"parsed_key": "parsed_value"}'

        # Call the cloud_event function
        result = cloud_event(event, Model=dict)

        # Assertions
        self.assertEqual(result, {"parsed_key": "parsed_value"})
        mock_b64decode.assert_called_once_with("base64_encoded_data")

    def test_parse_cloud_event_data(self):
        event = make_event('eyJmb28iOiAiYmFyIn0=')
        expected_result = {'foo': 'bar'}

        result = cloud_event(event, Model=dict)
    
        self.assertEqual(result, expected_result)
