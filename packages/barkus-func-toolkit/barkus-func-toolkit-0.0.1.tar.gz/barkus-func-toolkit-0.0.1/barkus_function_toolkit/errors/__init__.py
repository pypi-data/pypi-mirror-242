from pydantic import ValidationError as UnprocessableEntityException

class KnownExceptions:
    pass

class UnauthenticatedException(Exception, KnownExceptions):
    pass
    
class UnauthorizedException(Exception, KnownExceptions):
    pass

def handle_error(exp: Exception, prefix: str, statusCode: int):
    error_dump = repr(exp)
    error_msg = f"{prefix}: {error_dump}"
    print(error_msg)
    return ({'error': error_msg}, statusCode)