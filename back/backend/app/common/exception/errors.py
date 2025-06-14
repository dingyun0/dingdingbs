#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from fastapi import HTTPException
from starlette.background import BackgroundTask

from backend.app.common.response.response_code import CustomCode


class BaseExceptionMixin(Exception):
    code: int

    def __init__(self, *, msg: str = None, data: Any = None, background: BackgroundTask | None = None):
        self.msg = msg
        self.data = data
        # The original background task: https://www.starlette.io/background/
        self.background = background


class HTTPError(HTTPException):
    def __init__(self, *, code: int, msg: Any = None, headers: dict[str, Any] | None = None):
        super().__init__(status_code=code, detail=msg, headers=headers)


class CustomError(Exception):
    def __init__(self, message: str = None):
        self.message = message

    def __str__(self):
        return self.message


class ValidationError(CustomError):
    pass


class RequestError(BaseExceptionMixin):
    code = 400

    def __init__(self, *, msg: str = 'Bad Request', data: Any = None, background: BackgroundTask | None = None):
        super().__init__(msg=msg, data=data, background=background)


class ForbiddenError(CustomError):
    pass


class NotFoundError(CustomError):
    pass


class ServerError(BaseExceptionMixin):
    code = 500

    def __init__(
        self, *, msg: str = 'Internal Server Error', data: Any = None, background: BackgroundTask | None = None
    ):
        super().__init__(msg=msg, data=data, background=background)


class GatewayError(BaseExceptionMixin):
    code = 502

    def __init__(self, *, msg: str = 'Bad Gateway', data: Any = None, background: BackgroundTask | None = None):
        super().__init__(msg=msg, data=data, background=background)


class AuthorizationError(BaseExceptionMixin):
    code = 401

    def __init__(self, *, msg: str = 'Permission denied', data: Any = None, background: BackgroundTask | None = None):
        super().__init__(msg=msg, data=data, background=background)


class TokenError(Exception):
    def __init__(self, message: str = "Token验证失败"):
        self.message = message
        super().__init__(self.message)
