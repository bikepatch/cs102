from __future__ import annotations

import socket
import typing as tp

from httptools import HttpRequestParser
from httptools.parser.errors import (
    HttpParserError,
    HttpParserCallbackError,
    HttpParserInvalidStatusError,
    HttpParserInvalidMethodError,
    HttpParserInvalidURLError,
    HttpParserUpgrade,
)

from .request import HTTPRequest
from .response import HTTPResponse

from collections import defaultdict

if tp.TYPE_CHECKING:
    from .server import TCPServer

Address = tp.Tuple[str, int]


class BaseRequestHandler:
    def __init__(self, socket: socket.socket, address: Address, server: TCPServer) -> None:
        self.socket = socket
        self.address = address
        self.server = server

    def handle(self) -> None:
        self.close()

    def close(self) -> None:
        self.socket.close()


class EchoRequestHandler(BaseRequestHandler):
    def handle(self) -> None:
        try:
            data = self.socket.recv(1024)
        except (socket.timeout, BlockingIOError):
            pass
        else:
            self.socket.sendall(data)
        finally:
            self.close()


class BaseHTTPRequestHandler(BaseRequestHandler):
    request_http = HTTPRequest
    response_http = HTTPResponse

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parser = HttpRequestParser(self)

        self._url: bytes = b""
        self._headers: tp.DefaultDict[bytes, bytes] = defaultdict()
        self._body: bytes = b""
        self._parsed = False

    def handle(self) -> None:
        request = self.parse_request()
        if request:
            try:
                response = self.handle_request(request)
            except Exception as exc:
                print(f"Got exception - {exc}, returned 500")
                response = self.response_http(status=500, headers={}, body=b"")
        else:
            response = self.response_http(status=400, headers={}, body=b"")
        self.handle_response(response)
        self.close()

    def parse_request(self) -> tp.Optional[HTTPRequest]:
        while self._parsed is not True:
            try:
                info = self.socket.recv(1024)
                if len(info) == 0:
                    break
                self.parser.feed_data(info)
            except socket.timeout:
                print(f"Connection {self.address} timeout")
                break
            except (
                HttpParserError,
                HttpParserCallbackError,
                HttpParserInvalidStatusError,
                HttpParserInvalidMethodError,
                HttpParserInvalidURLError,
                HttpParserUpgrade,
            ) as exc:
                print(f"Parser error {self.address} - {exc}")
                break
        if self._parsed:
            method = self.parser.get_method()
            return self.request_http(
                method=method, url=self._url, headers=self._headers, body=self._body
            )
        return None

    def handle_request(self, request: HTTPRequest, status: int = 405) -> HTTPResponse:
        return self.response_http(status=status, headers={}, body=b"")

    def handle_response(self, response: HTTPResponse) -> None:
        handled_response = response.to_http1()
        self.socket.sendall(handled_response)

    def on_url(self, url: bytes) -> None:
        self._url = url

    def on_header(self, name: bytes, value: bytes) -> None:
        self._headers[name] = value

    def on_body(self, body: bytes) -> None:
        self._body = body

    def on_message_complete(self) -> None:
        self._parsed = True
