import dataclasses
import re
import typing as tp

from slowapi.request import Request
from slowapi.response import Response


@dataclasses.dataclass
class Route:
    path: str
    method: str
    func: tp.Callable

    def check_data(self, request):
        if request.method != self.method:
            return False
        split_path = self.path.split("/")
        request_split_path= request.path.split("/")
        if len(split_path) == len(request_split_path):
            for i in range(len(request_split_path)):
                if not split_path[i].startswith("{") and split_path[i].endswith("}"):
                    if split_path[i] != request_split_path[i]:
                        return False
            return True
        return False

    def parse_args(self, request) -> tp.List[str]:
        args = []
        split_path = self.path.split("/")
        request_split_path = request.path.split("/")
        if len(split_path) == len(request_split_path):
            for i in range(len(request_split_path)):
                if split_path[i].startswith("{") and split_path[i].endswith("}"):
                    args.append(request_split_path[i])
        return args

    def handle_route(self, request):
        args = self.parse_args(request)
        return self.func(request, *args)

@dataclasses.dataclass
class Router:
    def __init__(self):
        self.routes: tp.List[Route] = []

    def resolve(self, request: Request) -> Response:
        for route in self.routes:
            if route.check_data(request):
                return route.handle_route(request)
        status = http.HTTPStatus(404)
        response_body = "\n".join([str(status.value), status.phrase, status.description])
        return Response(status.value, {}, response_body)

    def add_route(self, route: Route):
        self.routes.append(route)