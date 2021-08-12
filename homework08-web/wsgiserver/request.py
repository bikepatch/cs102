import dataclasses
import typing as tp
import io

from httpserver import HTTPRequest

@dataclasses.dataclass
class WSGIRequest(HTTPRequest):
    def to_environ(self) -> tp.Dict[str, tp.Any]:
        environ = {}
        environ["REQUEST_METHOD"] = self.method.decode()
        environ["SCRIPT_NAME"] = ""
        environ["PATH_INFO"] = self.url.decode("utf-8")
        if "?" in self.url.decode():
          environ["QUERY_STRING"] = self.url.decode("utf-8").split("?")[1]
        else:
          environ["QUERY_STRING"] = ""
        environ["CONTENT_TYPE"] = self.headers.get(b"Content-Type", b"").decode()
        environ["CONTENT_LENGTH"] = self.headers.get(b"Content-Length", b"").decode()
        environ["SERVER_NAME"] = self.headers.get(b"Host").split(b":")[0].decode()
        host = self.headers.get(b"host")
        if b":" in host:
          environ["SERVER_PORT"] = host.split(b":")[1].decode()
        else:
          environ["SERVER_PORT"] = ""
        environ["SERVER_PROTOCOL"] = "HTTP/1.1"
        for header in self.headers:
            environ[f"HTTP_{header.decode().upper()}"] = self.headers[header].decode()
        environ["wsgi.version"] = (1, 0)
        if self.url.startswith(b"https"):
          environ["wsgi.url_scheme"] = "https"
        else:
          environ["wsgi.url_scheme"] = "http"
        environ["wsgi.input"] = io.BytesIO(self.body)
        environ["wsgi.errors"] = sys.stderr
        environ["wsgi.multithread"] = True
        environ["wsgi.multiprocess"] = False
        environ["wsgi.run_once"] = True
        return environ
