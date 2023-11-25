from tests.helpers.response_assertion import *
from tests.helpers.raise_pydantic_validation_error import *


def assert_exists_in_query(query: str, item, errorMessage: str):
		existsInQuery = item in query
		assert existsInQuery == True, errorMessage