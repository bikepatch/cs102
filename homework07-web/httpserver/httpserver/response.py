import dataclasses
import http.client
import typing as tp


@dataclasses.dataclass
class HTTPResponse:
    status: int
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: bytes = b""

    def to_http1(self) -> bytes:
        status_string = http.client.responses[self.status]
        http1 = (
            f"HTTP/1.1 {self.status} {status_string}\r\n"
            + "\r\n".join(f"{key}: {self.headers[key]}" for key in self.headers)
            + "\r\n\r\n"
        )
        return http1.encode() + self.body
