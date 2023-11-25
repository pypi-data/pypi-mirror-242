class ResponseAssertion:
	def __init__(self, response):
		self.__response = response

	def assert404(self, message: str = ""):
		self.assertAny(message = message, statusCode = 404)

	def assertOK(self, message:str = "", statusCode: int = 200):
		self.assertAny(message = message, statusCode = statusCode)

	def assertError(self, message: str = "", statusCode: int = 500):
		self.assertAny(error = message, statusCode = statusCode)

	def assertServerError(self, message: str = ""):
		self.assertError(message = message, statusCode = 500)

	def assertUnauthenticated(self, message: str = ""):
		self.assertError(message = message, statusCode = 403)

	def assertUnauthorized(self, message: str = ""):
		self.assertError(message = message, statusCode = 401)

	def assertBadRequest(self, message: str = ""):
		self.assertError(message = message, statusCode = 400)

	def assertUnprocessableEntity(self):
		self.assertError(statusCode = 422)

	def assertAny(self, message:str = "", error: str = "", statusCode: int = 0):
		checks = 0
		if statusCode > 0:
			checks = checks + 1
			self.__assertStatusCode(statusCode)
		if len(message) > 0:
			checks = checks + 1
			self.__assertMessage(message)
		if len(error) > 0:
			checks = checks + 1
			self.__assertErrorMessage(error)
		assert checks > 0, f"ResponseAssertion: at least one assertion must be made"


	def __assertErrorMessage(self, expected: str):
		self.__assertMessage({'error': expected})

	def __assertMessage(self, expected: str):
		received = self.__response[0]
		assert received == expected, f"Received response message [{received}] is not equal the message expected [{expected}]"

	def __assertStatusCode(self, expected: int):
		received = self.__response[1]
		assert received == expected, f"Status Code, received [{received}], but should be [{expected}]"