import mimetypes
import pathlib
import datetime
import os
import typing as tp
from urllib.parse import unquote, urlparse

from httpserver import BaseHTTPRequestHandler, HTTPRequest, HTTPResponse, HTTPServer


def url_normalize(path: str) -> str:
    if path.startswith("."):
        path = "/" + path
    while "../" in path:
        path1 = path.find("/..")
        path2 = path.rfind("/", 0, p1)
        if path2 != -1:
            path = path[:path2] + path[path1 + 3 :]
        else:
            path = path.replace("/..", "", 1)
    path = path.replace("/./", "/")
    path = path.replace("/.", "")
    path = path.replace("%20", " ")
    return path


class StaticHTTPRequestHandler(BaseHTTPRequestHandler):
    @tp.no_type_check
    def handle_request(self, request: HTTPRequest, **kwargs: tp.Dict[str, str]) -> HTTPResponse:
        # NOTE: https://tools.ietf.org/html/rfc3986
        # NOTE: echo -n "GET / HTTP/1.0\r\n\r\n" | nc localhost 5000
        content: bytes = b"Method Not Allowed"
        status: int = 405
        default_headers = {
            "Date": str(datetime.datetime.now()),
            "Server": "Server",
            "Content-Length": str(len(content)),
            "Content-Type": str,
            "Allow": "GET, HEAD",
        }
        content_type: tp.Optional[str] = None
        if request.method == b"GET" or request.method == b"HEAD":
            status = 200
            url = urlparse(url_normalize(request.url.decode()))
            default_url_path = url.path
            if url.path.endswith("/"):
                default_url_path += "index.html"
            path = pathlib.Path(str(server.document_root.absolute()) + default_url_path)
            if os.path.exists(path) and os.path.isfile(path):
                try:
                    with open(path, "rb") as f:
                        content = f.read()
                    content_type, _ = mimetypes.guess_type(path)
                    print(path)
                    print("\n")
                    print(content_type)
                    print("\n")
                except OSError as os_exc:
                    print(f"Tried to get ...{path[:10]}, got {os_exc}. 404.")
                    status = 404
                except Exception as exc:
                    print(f"Tried to get ...{path[:10]}, got {exc}. 500 Internal error.")
                    status = 500
            else:
                status = 404
                print("File not found or is not a file. 404")
            print("flag1")
            if request.method == b"HEAD":
                content = b""
                print("flag2")
            print("flag3")
            default_headers["Content-Length"] = str(len(content))
            print("flag4")
            default_headers["Content-Type"] = "text/html" if not content_type else content_type
            print("flag5")
            return self.response_http(status=status, headers=default_headers, body=content)
        print("flag6")
        return self.response_http(status=status, headers=default_headers, body=b"")


class StaticServer(HTTPServer):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = 5,
        request_handler_cls: tp.Type[StaticHTTPRequestHandler] = StaticHTTPRequestHandler,
        document_root: pathlib.Path = pathlib.Path("."),
    ) -> None:
        super().__init__(
            host=host,
            port=port,
            backlog_size=backlog_size,
            max_workers=max_workers,
            timeout=timeout,
            request_handler_cls=request_handler_cls,
        )
        self.document_root = document_root


if __name__ == "__main__":
    document_root = pathlib.Path("static") / "root"
    server = StaticServer(
        timeout=60,
        document_root=document_root,
        request_handler_cls=StaticHTTPRequestHandler,
    )
    server.serve_forever()
