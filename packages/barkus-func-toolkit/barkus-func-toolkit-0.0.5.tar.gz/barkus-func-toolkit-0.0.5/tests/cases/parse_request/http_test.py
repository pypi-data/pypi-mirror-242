import unittest
from unittest.mock import Mock
from barkus_function_toolkit.parse_request import http

def make_event(data: str):
    return Mock(data = { "message": { "data": data } })

class TestParseRequestHttp(unittest.TestCase):

    def test_http(self):
        request = Mock()
        request.get_json.return_value = {"key": "value"}
        
        # Call the http function
        result = http(request, Model=dict)

        # Assertions
        self.assertEqual(result, {"key": "value"})
        request.get_json.assert_called_once_with(silent=True)
