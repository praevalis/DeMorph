from fastapi import HTTPException, status

class BadRequestException(HTTPException):
    def __init__(self, detail: str = 'Bad request'):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = 'Unauthorized'):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self, detail: str = 'Access forbidden'):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class NotFoundException(HTTPException):
    def __init__(self, detail: str = 'Resource not found'):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UnprocessableEntityException(HTTPException):
    def __init__(self, detail: str = 'Unprocessable entity'):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class InternalServerException(HTTPException):
    def __init__(self, detail: str = 'Internal server error'):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)