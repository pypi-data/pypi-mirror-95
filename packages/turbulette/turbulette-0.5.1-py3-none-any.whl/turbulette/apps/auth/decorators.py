"""Auth decorators exposing most of the auth logic."""

from datetime import datetime
from typing import Any, Callable

from turbulette.errors import ErrorCode, add_error
from turbulette.utils import is_query

from .core import TokenType, _process_jwt_header, decode_jwt, settings
from .exceptions import JWTInvalidTokenType, JWTNotFresh
from .policy import authorized


def scope_required(func: Callable[..., Any]):
    """Scope decorator.

    Log a user and check if it has the required permissions
    before executing the wrapped function

    If the user successfully has been successfully logged in,
    the user model instance is added to the context dictionary
    with the key ``user``
    """

    @access_token_required
    async def wrapper(obj, info, **kwargs):
        if await authorized(info.context["claims"], info):
            return await func(obj, info, **kwargs)
        if is_query(info):
            add_error(ErrorCode.QUERY_NOT_ALLOWED)
            return None
        add_error(ErrorCode.FIELD_NOT_ALLOWED, info.field_name)
        return None

    return wrapper


def access_token_required(func: Callable[..., Any]):
    """Access token decorator.

    Decorator that require a jwt access token
    before executing the wrapped function

    If the user successfully has been successfully
    logged in, the user model instance is added to
    the context dictionary with the key ``user``
    """

    @_jwt_required(TokenType.ACCESS)
    async def wrapper(obj, info, **kwargs):
        return await func(obj, info, **kwargs)

    return wrapper


def fresh_token_required(func: Callable[..., Any]):
    """Fresh token decorator.

    Decorator that require a fresh jwt access token
    before executing the wrapped function

    If the user successfully has been successfully
    logged in, the user model instance is added to
    the context dictionary with the key ``user``

    The "freshness" is determined by the `JWT_FRESH_DELTA` timedelta setting
    """

    @_jwt_required(TokenType.ACCESS)
    async def wrapper(obj, info, **kwargs):
        if (
            datetime.utcnow() - datetime.utcfromtimestamp(info.context["claims"]["iat"])
        ) > settings.JWT_FRESH_DELTA:
            raise JWTNotFresh()
        return await func(obj, info, **kwargs)

    return wrapper


def refresh_token_required(func: Callable[..., Any]):
    """Refresh token decorator.

    Decorator that require a jwt refresh token
    before executing the wrapped function

    If the user successfully has been successfully
    logged in, the user model instance is added to
    the context dictionary with the key ``user``
    """

    @_jwt_required(TokenType.REFRESH)
    async def wrapper(obj, info, **kwargs):
        return await func(obj, info, **kwargs)

    return wrapper


def _jwt_required(token_type: TokenType):
    """Base decorator for requiring JWT."""

    def wrap(func: Callable[..., Any]):
        async def wrapped_func(obj, info, **kwargs):
            jwt = _process_jwt_header(info.context["request"].headers["authorization"])
            claims = decode_jwt(jwt)[1]
            if TokenType(claims["type"]) is not token_type:
                raise JWTInvalidTokenType(
                    f"The provided JWT is not a {token_type.value} token"
                )
            info.context["claims"] = claims
            return await func(obj, info, **kwargs)

        return wrapped_func

    return wrap
