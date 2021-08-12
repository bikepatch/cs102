import typing as tp

from httpserver import BaseHTTPRequestHandler, HTTPServer

from .request import WSGIRequest
from .response import WSGIResponse


class WSGIServer(HTTPServer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app: tp.Optional[tp.Any] = None

    def set_app(self, app: tp.Any) -> None:
        self.app = app

    def get_app(self) -> tp.Optional[tp.Any]:
        return self.app


class WSGIRequestHandler(BaseHTTPRequestHandler):
    request_klass = WSGIRequest
    response_klass = WSGIResponse

    def handle_request(self, request: WSGIRequest) -> WSGIResponse:
        # сформировать словарь с переменными окружения
        # дополнить словарь информацией о сервере
        # вызвать приложение передав ему словарь с переменными окружения и callback'ом
        # ответ приложения представить в виде байтовой строки
        # вернуть объект класса WSGIResponse
        environ = request.to_environ()
        environ["SERVER_NAME"], environ["SERVER_PORT"] = self.address
        response = WSGIResponse()
        app_response = self.server.app(environ, response.start_response)
        response.body = app_response[0]
        return response

