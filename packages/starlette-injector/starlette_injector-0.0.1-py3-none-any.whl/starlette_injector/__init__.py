import inspect
from contextlib import asynccontextmanager
from contextvars import ContextVar
from functools import wraps
from typing import Any, Dict, Optional, Type

import starlette.routing
from injector import (Binder, Injector, InstanceProvider, Module, Provider,
                      Scope, ScopeDecorator, T, inject, provider)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


def injector_endpoint(func):
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(request: Request):
            injector: Injector = request.app.state.injector
            return await injector.call_with_injection(inject(func))
        return wrapper
    
    @wraps(func)
    def wrapper(request: Request):
        injector: Injector = request.app.state.injector
        return injector.call_with_injection(inject(func))
    return wrapper


class Route(starlette.routing.Route):
    def __init__(self, path, endpoint, *args, **kwargs):
        super().__init__(path, injector_endpoint(endpoint), *args, *kwargs)


_request_cache: ContextVar[Optional[Dict[Type, Any]]] = ContextVar("request_cache", default=None)

def _get_cache() -> Dict[Type, Any]:
    cache = _request_cache.get()
    if cache is None:
        raise RequestScopeError("Request context missing.")
    return cache

class RequestScopeError(ValueError):
    """Raised for RequestScope-related errors."""

class RequestScope(Scope):
    def __init__(self, injector: Injector):
        super().__init__(injector)

    def get(self, key: Type[T], provider: Provider[T]) -> Provider[T]:
        cache = _get_cache()

        if key not in cache:
            cache[key] = provider.get(self.injector)

        return InstanceProvider(cache[key])

    def _enter(self) -> None:
        if _request_cache.get() is not None:
            raise RequestScopeError("Attempting to re-enter request scope context.")
        _request_cache.set({})

    def _exit(self) -> None:
        if _request_cache.get() is None:
            raise RequestScopeError("Attempting to exit request scope context before it was entered.")
        _request_cache.set(None)

    @asynccontextmanager
    async def manager(self, request: Request):
        self._enter()
        # "Seed" the request (cf. https://github.com/google/guice/wiki/CustomScopes).
        _get_cache()[Request] = request
        try:
            yield
        finally:
            self._exit()

request_scope = ScopeDecorator(RequestScope)

class RequestModule(Module):

    @provider
    @request_scope
    def provide_request_id(self) -> Request:
        # The Request should have been populated in RequestMiddleware.
        return _get_cache()[Request]

# It is probably feasible to eliminate RequestMiddleware and enter RequestScope contextmanager
# in injector_endpoint. But that would mean entering the request scope relatively late, i.e. after
# all middleware. By using RequestMiddleware, it would be easier to add injection to middleware in
# the future.
class RequestMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, injector: Injector):
        super().__init__(app)
        self.request_scope = injector.get(RequestScope)

    async def dispatch(self, request, call_next):
        async with self.request_scope.manager(request):
            return await call_next(request)



