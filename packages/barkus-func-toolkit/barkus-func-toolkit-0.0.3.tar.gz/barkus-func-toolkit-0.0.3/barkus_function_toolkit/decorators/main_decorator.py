import functions_framework
from typing import Callable, Any
from typing import TypeVar
from ..errors import \
	UnauthenticatedException,\
	UnauthorizedException,\
	UnprocessableEntityException,\
	handle_error

CallbackType = TypeVar("CallbackType", bound = Callable)

def main_decorator():
	def decorator(perform: CallbackType) -> Callable[[CallbackType], CallbackType]:
		def wrapper(*args, **kwargs):
			try:
				perform(*args, **kwargs)
				return ("Success", 200)
			except UnprocessableEntityException as e:
				return handle_error(e, "Invalid request body", 422)
			except UnauthenticatedException as e:
				return handle_error(e, "Unauthenticated", 403)
			except UnauthorizedException as e:
				return handle_error(e, "Unauthorized", 401)
			except Exception as e:
				return handle_error(e, "An unexpected exception occurred", 500)
		any_wrapper: Any = wrapper
		return any_wrapper
	return decorator

class main:
	@staticmethod
	def cloud_event() -> Callable[[Callable], Callable]:
		"""
		Wraps a function callback with:
			- error handling
			- response parsing

		:example 

		@decorators.main.cloud_event
		def main(request):
			...

		"""
		decorator = main_decorator()
		def wrap(perform: CallbackType) -> CallbackType:
			cb: Any = functions_framework.cloud_event(decorator(perform))
			return cb
		return wrap
	
	@staticmethod
	def http():
		"""
		Wraps a function callback with:
			- error handling
			- response parsing

		:example 

		@decorators.main.http
		def main(request):
			...

		"""
		decorator = main_decorator()
		def wrap(perform: CallbackType) -> CallbackType:
			cb: Any = functions_framework.http(decorator(perform))
			return cb
		return wrap