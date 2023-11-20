from __future__ import annotations

from typing import Any, Union

from quart.globals import (
    _cv_app,
    _cv_request,
    _cv_websocket,
    app_ctx,
    current_app,
    g,
    request as quart_request,
    request_ctx,
    session,
)
from werkzeug.datastructures import MultiDict
from werkzeug.local import LocalProxy

from ._synchronise import sync_with_context


class FlaskRequestProxy(LocalProxy):
    @property
    def data(self) -> bytes:
        return sync_with_context(self._get_current_object().data)

    @property
    def form(self) -> MultiDict:
        return sync_with_context(self._get_current_object().form)

    @property
    def files(self) -> MultiDict:
        return sync_with_context(self._get_current_object().files)

    @property
    def values(self) -> MultiDict:
        return sync_with_context(self._get_current_object().values)

    @property
    def json(self) -> Any:
        return sync_with_context(self._get_current_object().json)

    def get_json(self, *args: Any, **kwargs: Any) -> Any:
        return sync_with_context(self._get_current_object().get_json(*args, **kwargs))

    def get_data(self, *args: Any, **kwargs: Any) -> Union[str, bytes]:
        return sync_with_context(self._get_current_object().get_data(*args, **kwargs))


request = FlaskRequestProxy(lambda: quart_request)


__all__ = (
    "_cv_app",
    "_cv_request",
    "_cv_websocket",
    "app_ctx",
    "current_app",
    "g",
    "request",
    "request_ctx",
    "session",
)
