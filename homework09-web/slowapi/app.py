import http
import typing as tp
from urllib.parse import parse_qsl
from collections import defaultdict

from slowapi.request import Request
from slowapi.response import Response
from slowapi.router import Route, Router


class SlowAPI:
    def __init__(self):
        self.router = Router()
        self._headers = defaultdict(lambda: str)
        self._query = defaultdict(lambda: str)
        self.middlewares = []

    def __call__(self, environ, start_response):
        # PUT YOUR CODE HERE
        self._fill_h(environ)
        self._fill_q(environ)
        request = Request(
            path=environ.get("PATH_INFO", "").rstrip("/") or "/",
            method=environ.get("REQUEST_METHOD", ""),
            query=self._query,
            headers=self._headers,
            body=environ.get("wsgi.input", ""),
        )
        answer = self.router.resolve(request)
        status = http.HTTPStatus(answer.status)
        start_response(" ".join([str(status.value), status.phrase]))
        if answer.body is None:
            return [b""]
        else:
            return [answer.body.encode()]

    def _fill_h(self, environ, tp.Dict[str, tp.Any]):
        for item in environ:
            if item.startswith("HTTP_"):
                index = item[5:].lower()
                self._headers[index] = environ[item]


    def _fill_q(self, environ, tp.Dict[str, tp.Any]):
        for i, num in parse_qsl(environ.get("QUERY_STRING", "")):
            self._query[i] = num

    def route(self, path=None, method=None, **options):
        # PUT YOUR CODE HERE
        def decorator(func: tp.Callable):
            route = Route(path.rstrip("/"), method, func)
            self.router.add_route(route)
            return func
        return decorator

    def get(self, path=None, **options):
        return self.route(path, method="GET", **options)

    def post(self, path=None, **options):
        return self.route(path, method="POST", **options)
    
    def patch(self, path=None, **options):
        return self.route(path, method="PATCH", **options)

    def put(self, path=None, **options):
        return self.route(path, method="PUT", **options)

    def delete(self, path=None, **options):
        return self.route(path, method="DELETE", **options)

    def add_middleware(self, middleware) -> None:
        self.middlewares.append(middleware)
