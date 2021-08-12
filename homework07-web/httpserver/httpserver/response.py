import dataclasses
import http
import typing as tp


@dataclasses.dataclass
class HTTPResponse:
    status: int
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: bytes = b""

    def to_http1(self) -> bytes:
        status_string = (
            "HTTP/1.1 " + str(self.status) + " " + http.client.responses[self.status] + "\r\n"
        ).encode()
        headers_str = b""
        for key in self.headers.keys():
            headers_str += (key + ": " + self.headers[key] + "\r\n").encode()
        headers_str += b"\r\n"
        http1 = status_string + headers_str + self.body
        return http1
