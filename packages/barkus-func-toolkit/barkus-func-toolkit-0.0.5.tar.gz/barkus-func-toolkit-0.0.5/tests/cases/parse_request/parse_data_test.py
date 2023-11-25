import unittest
from unittest.mock import Mock, patch
import dacite
from barkus_function_toolkit.parse_request import internal_parse_data

def make_event(data: str):
    return Mock(data = { "message": { "data": data } })

class TestParseRequestInternalParseData(unittest.TestCase):
    @patch('barkus_function_toolkit.parse_request.from_dict')
    @patch('barkus_function_toolkit.parse_request.Config')
    def test_internal_parse_data_calls_from_dict_for_non_dict_model(self, mock_config: Mock, mock_from_dict: Mock):
        from dataclasses import dataclass
        from typing import Literal

        @dataclass
        class Model:
            key: Literal['value']

        data = {'key': 'value'}
        internal_parse_data(data, Model=Model, check_types=False)
        
        mock_config.assert_called_once_with(check_types=False)
        mock_from_dict.assert_called_once_with(Model, data, mock_config.return_value)

    @patch('barkus_function_toolkit.parse_request.from_dict')
    @patch('barkus_function_toolkit.parse_request.Config')
    def test_doesnt_call_from_dict_when_model_is_pydantic(self, mock_config: Mock, mock_from_dict: Mock):
        from pydantic import BaseModel
        from typing import Literal

        class Model(BaseModel):
            key: Literal['value']

        data = {'key': 'value'}
        internal_parse_data(data, Model=Model)
        
        mock_config.assert_not_called()
        mock_from_dict.assert_not_called()

    def test_internal_parse_data_returns_dict_for_dict_model(self):
        data = {'key': 'value'}
        result = internal_parse_data(data, Model=dict)
        self.assertEqual(result, data)


    def test_calls_from_dict_for_non_dict_model_with_correct_values(self):
        from dataclasses import dataclass
        from typing import Literal

        @dataclass
        class Model:
            key: Literal['value']

        data = {'key': 'value'}
        result = internal_parse_data(data, Model=Model, check_types=False)
        
        self.assertEqual(result.__dict__, data)
        self.assertIsInstance(result, Model)